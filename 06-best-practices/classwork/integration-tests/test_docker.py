import json
import requests
from deepdiff import DeepDiff

event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49630081666084879290581185630324770398608704880802529282",
                "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDI1NgogICAgfQ==",
                "approximateArrivalTimestamp": 1654161514.132
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49630081666084879290581185630324770398608704880802529282",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::143108597168:role/lambda_for_kinesis",
            "awsRegion": "eu-east-1",
            "eventSourceARN": "arn:aws:kinesis:us-east-1:143108597168:stream/ride_events_mlops-zoomcamp-week4"
        }
    ]
}

url = "http://localhost:8080/2015-03-31/functions/function/invocations"
actual_response = requests.post(url, json=event).json()

print(json.dumps(actual_response, indent=2))

expected_response = {
    "predictions": [
            {
                "model": "ride_duration_prediction_model", 
                "version": "123", 
                "prediction": {
                    "ride_duration": 18.2, 
                    "ride_id": 256
                }
            }
        ]
    }

diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f"diff: {diff}")

assert "types_changed" not in diff
assert "values_changed" not in diff
