# includes providers directly installed from
# terraform registry by default
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.2.0"
  backend "s3" {
    bucket  = "nrf-terraform"
    key     = "terraform.tfstate"
    region  = "us-east-1"
    profile = "nicolas-devops"
    encrypt = true
  }
}

provider "aws" {
  region  = var.region
  profile = var.aws_profile
}

data "aws_caller_identity" "current_identity" {}

# Local values are like a function's temporary local variables.
locals {
  account_id                 = data.aws_caller_identity.current_identity.account_id
  project_id                 = "mlops-zoomcamp-week4"
  lambda_function_local_path = "../lambda_function.py"
  docker_image_local_path    = "../Dockerfile"
  ecr_repo_name              = "stream_model_duration_${local.project_id}"
  source_stream_name         = "ride_events_${local.project_id}"
  output_stream_name         = "ride_predictions_${local.project_id}"
  model_bucket               = "nrf-mlflow"
  mlflow_run_id              = "66679dc47de544cdae3289642deb8eb5"
}

# it can be useful to compare Terraform modules to function definitions
# Input variables are like function arguments.
module "ecr_image" {
  source                     = "./modules/ecr"
  ecr_repo_name              = local.ecr_repo_name
  account_id                 = local.account_id
  region                     = var.region
  lambda_function_local_path = local.lambda_function_local_path
  docker_image_local_path    = local.docker_image_local_path
}

module "source_kinesis_stream" {
  source           = "./modules/kinesis"
  stream_name      = local.source_stream_name
  retention_period = 48
  shard_count      = 2
}

module "lambda_function" {
  source             = "./modules/lambda"
  image_uri          = module.ecr_image.image_uri
  model_bucket       = local.model_bucket
  mlflow_run_id      = local.mlflow_run_id
  source_stream_name = local.source_stream_name
  source_stream_arn  = module.source_kinesis_stream.stream_arn
}
