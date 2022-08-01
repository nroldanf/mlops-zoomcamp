#!/usr/bin/env python
# coding: utf-8

from typing import List
import argparse
import os
import pickle
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--year",
        default=2021,
        type=int,
        help="Year"
    )
    parser.add_argument(
        "--month",
        default=1,
        type=int,
        help="Month"
    )
    args = parser.parse_args()
    return args

def get_input_path(year, month):
    default_input_pattern = f'https://raw.githubusercontent.com/alexeygrigorev/datasets/master/nyc-tlc/fhv/fhv_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)

def get_output_path(year, month):
    default_output_pattern = f's3://nrf-nyc-duration/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)

def read_data(filename: str, storage_options: dict=None):
    df = pd.read_parquet(filename, storage_options=storage_options)
    return df

def save_data(df, filepath, options):
    df.to_parquet(
        filepath,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )

def prepare_data(df: pd.DataFrame, categorical: List[str]):
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def main(year: int, month: int):
    input_file = get_input_path(year, month)
    print(input_file)
    output_file = get_output_path(year, month)
    S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL')
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
    }
    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)
    categorical = ['PUlocationID', 'DOlocationID']
    df = read_data(input_file, options)
    df = prepare_data(df, categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)    
    print('predicted mean duration:', y_pred.mean())
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred
    save_data(df_result, output_file, options)
    return df_result

if __name__ == "__main__":
    args = parse_args()
    main(args.year, args.month)