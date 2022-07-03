# Model Monitoring

## Problems with ML models

- Input features distribution can change (data drift)
- Target function can change itself (concept drift)
- How to preparte for the model degradation? > By monitoring

## Monitoring

Standard things to monitor for a model in production

- Service health
    - does it work?
- Model performance
    - how it performs?
    - did anything break?
    - metrics depend of the problem statement (classification, regression, recommenders, etcs)
    - ideally, have inmediate feedback
- Data quality and integrity
- Data and concept drift

More things to look at:

- Performance by segment: for example, new users, or user for specific regions.
- Model bias/fairness: for sensitive service in medicine and social applications
- Outliers: if each individual error cost a lot
- Explainability: if you have to share information about the decision you took.

## How to monitor?

- Calculation block after specific steps of the pipelines (e.g. with airflow or prefect)
- Log data into sql/nosql database
- Add visualization layer, each time you get a new batch of data (evidently allow to generate reports on html format)
- To calculate how the service operates in real time with dashboards and alerts can use Prometheus + Graphana
- Even if i have online service, is recommended to monitor in batch
    - it makes for data drift; no need to update after each new row, rather, collect some batch of data and then calculate drift

## Architecture (batch and online)

1. MongoDB: To store the predictions
2. Monitoring Service: Will send metrics in prometheus readable format
    - Prometheus DB: Can frequently pulls data from the application. With a client library in Python. DB is optimize for time series data.
    - Graphana: Directly integrated with Prometheus. Can create very nice visualizations, and configure alerts.
3. Batch monitoring
    - Prefect flow: calculate model profiles with evidently and send back to mongoDB (send input, preds, target and send back profiles).
    - HTML report with evidently
4. Dockerfiles for every service.
    - 