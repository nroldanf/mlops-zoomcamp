import json

import boto3

kinesis = boto3.client("kinesis", endpoint_url="http://localhost:4566")
prediction_event = {
    "model": "ride_duration_prediction_model",
    "version": "123",
    "prediction": {"ride_duration": 18.16894572640533, "ride_id": 256},
}

response = kinesis.put_record(
    StreamName="ride_predictions_mlops-zoomcamp-week4",
    Data=json.dumps(prediction_event),
    PartitionKey=str(prediction_event["prediction"]["ride_id"]),
)

print(response)
