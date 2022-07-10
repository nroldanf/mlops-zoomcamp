# In practice, the Image build-and-push step is handled separately by the CI/CD pipeline and not the IaC script.
# Therefore, it can be any base image to bootstrap the lambda config, unrelated to your Inference service on ECR
resource "null_resource" "ecr_image" {
  triggers = {
    python_file = md5(file(var.lambda_function_local_path))
    docker_file = md5(file(var.docker_image_local_path))
  }

  provisioner "local-exec" {
    command = <<EOF
             docker logout public.ecr.aws
             aws --profile nicolas-devops ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${var.account_id}.dkr.ecr.${var.region}.amazonaws.com
             cd ../
             docker build -t ${aws_ecr_repository.repo.repository_url}:${var.ecr_image_tag} .
             docker push ${aws_ecr_repository.repo.repository_url}:${var.ecr_image_tag}
         EOF
  }
}

// Wait for the image to be created, before lambda config runs
data "aws_ecr_image" "lambda_image" {
  depends_on = [
    null_resource.ecr_image
  ]
  repository_name = var.ecr_repo_name
  image_tag       = var.ecr_image_tag
}

resource "aws_ecr_repository" "repo" {
  name                 = var.ecr_repo_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
  tags = {
    Name = "mlops-zoomcamp"
  }
}
