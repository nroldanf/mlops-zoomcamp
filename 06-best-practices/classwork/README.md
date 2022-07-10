# Best practices

## Testing with PyTest

- Unit tests should cover small functionalities, like functions or methods.

Build the image:
```bash
docker build -t stream-model-duration:v2 .
```

To test the docker container locally:
```bash
docker run -it --rm \
    -v ~/.aws:/root/.aws \
    -v $(pwd)/model:/app/model \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_events_mlops-zoomcamp-week4" \
    -e RUN_ID="123" \
    -e AWS_DEFAULT_REGION="us-east-1" \
    -e MODEL_BUCKET="nrf-mlflow" \
    -e EXPERIMENT_ID="1" \
    -e MODEL_LOCATION="/app/model/" \
    stream-model-duration:v2
```

Then send this event to `http://localhost:8080/2015-03-31/functions/function/invocations`:
```JSON
{
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
```

To run the unit tests:
```
pytest tests
```

- Test should be as independent as possible
- Should be fast (don't want to go to S3 and download the model)
- A mock is something that looks like the actual thing but it's not, it's used for test purposes

To deploy the infrastructure:
```
terraform init
terraform plan --file-var dev.tfvars
terraform apply --file-var dev.tfvars
```

To download the model from s3 for the integration tests:
```
aws s3 --profile <aws-named-profile-name> s3 cp --recursive <s3-mlflow-model-path> <local-path>
```

Previous command exit code:
```
echo $?
```

To test AWS locally, in this case, kinesis, we use localstack. First starting the docker container:
```bash
docker-compose up kinesis
```

To test `aws cli` pointing to localstack local url:
```bash
aws --endpoint-url=http://localhost:4566 \
    kinesis list-streams
``` 

```bash
aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name ride_predictions \
    --shard-count 1
``` 

## Linting and formatting

```
pylint <file>
pylint --recursive=y <directory>
```

```
black --diff --color --verbose <dir>
black <dir>
```

```
isort --diff --check <dir>
isort <dir>
```

## Questions for office hours

- What happens when my model is too big and can't fit into my repo for the integration tests?