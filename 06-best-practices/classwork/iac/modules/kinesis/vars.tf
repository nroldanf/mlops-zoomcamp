variable "stream_name" {
  type        = string
  description = "Kinesis stream name"
}

variable "shard_count" {
  type        = string
  description = "Kinesis stream shard count"
}

variable "retention_period" {
  type        = string
  description = "Kinesis stream retention period"
}
