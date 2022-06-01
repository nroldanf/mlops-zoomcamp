import argparse
import os
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import mlflow

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("homework-autolog")
# enable autolog
mlflow.sklearn.autolog() # disable=True

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def run(data_path):

    max_depth = 10
    random_state = 0

    # with mlflow.start_run():

    #     mlflow.set_tag("developer", "nicolas")
    #     mlflow.log_param("train_data_path", "train.pkl")
    #     mlflow.log_param("valid_data_path", "valid.pkl")
        
    #     mlflow.log_param("max_depth", max_depth)
    #     mlflow.log_param("random_state", random_state)

    with mlflow.start_run():

        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_valid, y_valid = load_pickle(os.path.join(data_path, "valid.pkl"))

        rf = RandomForestRegressor(max_depth=max_depth, random_state=random_state)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_valid)

        rmse = mean_squared_error(y_valid, y_pred, squared=False)
    
        # mlflow.log_metric("rmse", rmse)
        
        # Log model as an artifact
        # mlflow.log_artifact(local_path="artifacts/mymodel.pkl", artifact_path="models_pickle/")
        
        # Log preprocessor as an artifact
        # mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor/")
        
        # Log model using log_model method
        # mlflow.sklearn.log_model(rf, artifact_path="models_mlflow/")
        
        # Access the model using different flavors: python func or native object from library (e.g. scikit learn object)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        default="./output",
        help="the location where the processed NYC taxi trip data was saved."
    )
    args = parser.parse_args()

    run(args.data_path)