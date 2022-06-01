# Experiment tracking

- __Experiment__: process of buolding an ML model (i.e. training, hpo, etc.)
- __Experiment run__: each trial of an ML experiment.
- __Run artifact__: any file associated with a run.
- __Metadata__: hyperparameters and all info that serve as inputs.

## What is experiment tracking?

Process of keeping track of all the relevant information from an ML experiment.

- Source code / Version (commit hash)
- Environment
- Data
- Hyperparameters
- Metrics

## Why is so important?

- __Reproducibility__: To be able to reproduce the same result.
- __Organization__: Important when working in a team with multiple people.
- __Optimization__: Optimize the ML model in an organized way.

## Way of doing experiment tracking

- Spreadsheet
    - __Error prone__ -> copy and paste
    - __No standard format__
    - __Visibility and collaboration__

Here where MLFlow tracking comes.

## MLFlow

Open source platform for the machine learning lifecycle.

In practice can be installed using pip and comes with different modules:
- Tracking
- Models
- Model Registry
- Projects

### Tracking experiments with mlflow

Allows you to organize your experiments into __runs__ and keep track of:

- __Paremeters__: hyperparameters, path to training data, etc.
- __Metrics__: evaluations metrics
- __Metadata__: paths, tags to filter runs.
- __Artifacts__: Visualizartions, dataset (doesn't scale...)
- __Models__: serialized model.

Along with this, MLFlow automatically logs:

- Source code
- Version of the code (git commit)
- Start and end time
- Author

### How to run MLFlow?

Start a gunicorn server with the UI.
```
mlflow ui
```

All artifacts and metadata will be saved in sqlite (one of the alternatives for the backedn store)
```
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## Model Management

Besides __experiment tracking__ it covers:
- Model versioning
- Model deployment
- Scaling hardware

## Model Registry

From the tracking server __register__ the models when are ready for production into a __model registry__ (staging, production, archive). The model registry is not in charge of deploying any model, so in order to actually deploy a model you need to add a CI/CD tool.

Possible states of a model within MLFlow model registry are:
- Staging
- Production
- Archived

Using model tracking tool with model registry tool, allows to have __model lineage__ and know how the artifact inside the registry was generated.
