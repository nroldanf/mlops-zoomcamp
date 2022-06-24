from typing import List, Tuple
import logging
import argparse
import pickle
import requests
import boto3
import botocore
import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

logging.basicConfig(
    format='%(asctime)s %(levelname)-s:%(name)s: %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S',
)

logger = logging.getLogger(__name__)

def parse():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--date', type=str, help='Date', required=True)
    parser.add_argument('--aws_profile', type=str, help='AWS Profile to use credentials.', default="default")
    parser.add_argument('--bucket', type=str, help='S3 bucket to store the output file with predictions.', required=True)
    args = parser.parse_args()
    return args

def load_model(model_path: str) -> Tuple[DictVectorizer, LinearRegression]:
    logger.info('Loading model...')
    with open(model_path, 'rb') as f_in:
        dv, lr = pickle.load(f_in)
    return dv, lr

def download_file(url: str, filename: str):
    logger.info(f"Downloading file from {url}...")
    try:
        response = requests.get(url)
    except Exception as error:
        raise f"Couldn't download the file from url {url} {error}"
    with open(filename, "wb") as f:
        f.write(response.content)

def read_data(filename: str, categorical: List[str]) -> pd.DataFrame:
    logger.info("Reading data from %s" % filename)
    df = pd.read_parquet(filename)
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def get_predictions(dv: DictVectorizer, lr, df: pd.DataFrame, categorical: List[str]) -> np.ndarray:
    dicts = df[categorical].to_dict(orient="records")
    X_val = dv.transform(dicts)
    logger.info("Making predictions...")
    y_pred = lr.predict(X_val)
    logger.info(f"The mean predicted duration is {np.mean(y_pred)}")
    return y_pred

def save_output(df: pd.DataFrame, date: str, y_pred: np.ndarray, filename: str) -> None:
    logger.info("Saving output...")
    df_result = df.copy(deep=True)
    year = int(date[0:4])
    month = int(date[5:7])
    df_result["ride_id"] = f'{year:04d}/{month:02d}_' + df_result.index.astype('str')
    df_result["predictions"] = y_pred
    df_result.drop(df_result.columns.difference(["ride_id", "predictions"]), 1, inplace=True)
    df_result.to_parquet(
        filename,
        engine='pyarrow',
        compression=None,
        index=False
    )
    
def upload_s3(filename: str, aws_profile: str, bucket: str) -> None:
    logging.info("Uploading output file to S3 bucket...")
    session = boto3.session.Session(profile_name=aws_profile)
    s3 = session.client("s3")
    try:
        s3.upload_file(filename, bucket, filename)
    except botocore.exceptions.ClientError as err:
        raise err
    
def main():
    args = parse()
    date = args.date 
    aws_profile = args.aws_profile
    bucket = args.bucket
    categorical = ['PUlocationID', 'DOlocationID']
    model_path = "model.bin"
    output_filename = "results_data_deployment.parquet"
    year = date[0:4]
    month = date[5:7]
    url = f"https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year}-{month}.parquet"
    filename = f"fhv_tripdata_{year}-{month}.parquet"
    download_file(url,filename)
    df = read_data(filename, categorical)
    dv, lr = load_model(model_path)
    y_pred = get_predictions(dv, lr, df, categorical)
    save_output(df, date, y_pred, output_filename)
    upload_s3(output_filename, aws_profile, bucket)
    logging.info("Finished.")
    
if __name__ == '__main__':
    main()