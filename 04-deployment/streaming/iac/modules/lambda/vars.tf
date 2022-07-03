variable "image_uri" {
  description = "ECR image uri"
}

variable "model_bucket" {
  description = "Name of the bucket"
}

variable "source_stream_name" {
  type        = string
  description = "Source Kinesis Data Streams stream name"
}

variable "source_stream_arn" {
  type        = string
  description = "Source Kinesis Data Streams stream arn"
}

variable "mlflow_run_id" {
  type        = string
  description = "Mlflow experiment run id"
}
