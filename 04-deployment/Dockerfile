FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim
# Install dependencies
RUN apt-get update && apt-get install -y curl unzip
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
RUN python3 -m pip install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
# Don't create a python environment
RUN pipenv install --system --python 3 --deploy
# Copy the predict script
COPY predict.py predict.py
ENTRYPOINT python3 predict.py --date=$DATE --aws_profile=$AWS_PROFILE --bucket=$BUCKET