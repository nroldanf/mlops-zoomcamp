# Model Deployment

Ask yourself:
- Need to have predictions inmediately or can wait for them (day or weeks)?

## Batch Offline Deployment

- Run regularly against batches of data (e.g. daily, weekly, etc)
- Have some sort of DB with the data.
- Have a (scoring) job running that host the model inside of it (e.g. AWS Batch, ECS)
- Apply the model to all the data from a previous interval/batch.
- Write the predictions to another DB.
- Other applications use those predictions.
- For applications where is not necessarily to know a result inmediately.

## Online Deployment

Model is always available, up and running all the time.

### Web Service

- Web service that contains the model, gets the data in request and send prediction back on a response.
- Backend talks to the web service that host the model.
- Needs to be up and running all the time.
- 1 to 1 relationship: there is a connection kept alive while processing the request.
- For applications where the use needs the result inmediately.

### Streaming

- There are **producers** and **consumers**.
- Producers pushes some events to an event stream/broker.
- Consumers fetch data from the event stream and then do something the data (multiple models) consume the data.
- Then, consumers can also send their predictions to another event stream/broker.
- Producers send events but doesn't actually wait/expect for a result.
- 1 to many or many to many relationship.

E.g. Content moderation (e.g. Youtube videos, Twitch Streaming). Copyright violation, NSFW, Violence, etc.

## Homework

### Terraform

Initialize terraform (installs providers plugin from terraform registry)
```
terraform init
```

Format configuration files for readability and consistency.
```
terraform fmt
```

Validates terraform configuration.
```
terraform validate
```

Creates and updates infrastructure according to Terraform configuration. First, prints out the execution plan which describes actions Terraform will take.
```
terraform apply
```

Inspect state:
```
terraform show
```

### Docker

Build the image:
```
docker build -t mlopz-zoomcamp:hw4 .
```

Execute the script as depicted below:
```
docker run --rm -v ~/.aws:/root/.aws \
    -e DATE="2021-03-01" \
    -e AWS_PROFILE="nicolas-devops" \
    -e BUCKET="mlops-zoomcamp-nicolas" \
    mlops-zoomcamp:hw4
```
