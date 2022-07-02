resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "test_lambda" {
  # If the file is not in the current working directory you will need to include a 
  # path.module in the filename.

  function_name = "lambda_function_name"
  image_uri     = var.image_uri
  package_type  = "Image"
  role          = aws_iam_role.iam_for_lambda.arn

  environment {
    variables = {
      SOURCE_STREAM_NAME = var.source_stream_name
      OUTPUT_STREAM_NAME = var.output_stream_name
      MODEL_BUCKET       = var.model_bucket
    }
  }
  timeout = 180
}