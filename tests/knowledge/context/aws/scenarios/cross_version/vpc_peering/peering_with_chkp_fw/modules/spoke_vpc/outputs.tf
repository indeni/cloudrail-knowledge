output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.vpc.id
}

output "subnet_id" {
  description = "Subnet ID"
  value       = aws_subnet.subnet.id
}
