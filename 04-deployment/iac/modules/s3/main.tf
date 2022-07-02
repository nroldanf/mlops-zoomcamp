resource "aws_s3_bucket" "model_bucket" {
  bucket = var.bucket_name

  tags = {
    Name = "mlops-zoomcamp"
  }
}
