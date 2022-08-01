import os
import subprocess
from datetime import datetime
import pandas as pd

def dt(hour, minute, second=0):
    return datetime(2021, 1, 1, hour, minute, second)

def main():
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (1, 1, dt(1, 2, 0), dt(2, 2, 1)),        
    ]
    columns = ['PUlocationID', 'DOlocationID', 'pickup_datetime', 'dropOff_datetime']
    df = pd.DataFrame(data, columns=columns)
    # save test data
    S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL')
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
    }
    year = 2021
    month = 1
    default_input_pattern = f'https://raw.githubusercontent.com/alexeygrigorev/datasets/master/nyc-tlc/fhv/fhv_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    input_file = input_pattern.format(year=year, month=month)
    print(input_file)
    df.to_parquet(
        input_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )
    process = subprocess.Popen(
        ["python", "batch.py", f"--year={year:04d}", f"--month={month:02d}"],
        shell=False,
    )
    process.wait()
    

if __name__ == '__main__':
    main()