#!/usr/bin/env bash

cd "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
export PREDICTIONS_STREAM_NAME="ride_predictions_mlops-zoomcamp-week4"

docker build -t ${LOCAL_IMAGE_NAME} ..

TMPDIR=/private$TMPDIR docker-compose up -d

sleep 1

aws --endpoint-url=http://localhost:4566/ \
    kinesis create-stream \
    --stream-name ${PREDICTIONS_STREAM_NAME} \
    --shard-count 1

sleep 1

python3 test_docker.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker-compose down