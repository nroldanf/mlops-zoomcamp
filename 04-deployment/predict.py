from typing import List
import argparse
import pickle
import wget
import pandas as pd
import numpy as np

def parse():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--date', type=str, help='Date')
    args = parser.parse_args()
    return args

def load_model(model_path: str):
    with open(model_path, 'rb') as f_in:
        dv, lr = pickle.load(f_in)
    return dv, lr

def read_data(filename: str, categorical: List[str]) -> pd.DataFrame:
    df = pd.read_parquet(filename)
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def get_predictions(dv, lr, df: pd.DataFrame, categorical: List[str]) -> np.ndarray:
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    print(f"The mean predicted duration is {np.mean(y_pred)}")
    return y_pred

def prepare_output(df: pd.DataFrame, date: str, y_pred: np.ndarray):
    df_result = df.copy(deep=True)
    year = int(date[0:4])
    month = int(date[5:7])
    
    df_result["ride_id"] = f'{year:04d}/{month:02d}_' + df_result.index.astype('str')
    df_result["predictions"] = y_pred
    df_result.drop(df_result.columns.difference(["ride_id", "predictions"]), 1, inplace=True)
    df_result.to_parquet(
        "results_data_deployment.parquet",
        engine='pyarrow',
        compression=None,
        index=False
    )
    
def main():
    args = parse()
    date = args.date 
    categorical = ['PUlocationID', 'DOlocationID']
    model_path = "model.bin"
    year = date[0:4]
    month = date[5:7]
    
    url = f"https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year}-{month}.parquet"
    # https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_2021-02.parquet
    print(url)
    filename = wget.download(url, out=f"fhv_tripdata_{year}-{month}.parquet")
    #filename = f"../data/fhv_tripdata_{year}-{month}.parquet"
    df = read_data(filename, categorical)
    
    dv, lr = load_model(model_path)
    y_pred = get_predictions(dv, lr, df, categorical)
    prepare_output(df, date, y_pred)
    
    
if __name__ == '__main__':
    main()