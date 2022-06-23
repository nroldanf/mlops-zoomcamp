FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim
# Install dependencies
RUN python3 -m pip install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system --python 3 --deploy
# Copy the predict script
COPY predict.py predict.py
ENTRYPOINT python3 predict.py --date=$DATE