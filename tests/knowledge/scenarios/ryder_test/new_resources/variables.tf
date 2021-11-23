variable "environment" {
  type        = string
  description = "Name of the environment"
  default     = "development"
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy resources in"
  default     = "us-east-1"
}

variable "ec2_subnet_id" {
  type        = string
  description = "Subnet ID to put the EC2 instance in"
  default = "subnet-09956738"
}
