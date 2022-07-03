variable "ecr_repo_name" {
  type = string
}

variable "ecr_image_tag" {
  type    = string
  default = "latest"
}

variable "account_id" {
  type = string
}

variable "region" {
  type = string
}

variable "lambda_function_local_path" {
  type = string
}

variable "docker_image_local_path" {
  type = string
}
