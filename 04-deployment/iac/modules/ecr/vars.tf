variable "ecr_repo_name" {
  type = string
}

variable "ecr_image_tag" {
  type    = string
  default = "latest"
}

variable "account_id" {
  type    = string
}
