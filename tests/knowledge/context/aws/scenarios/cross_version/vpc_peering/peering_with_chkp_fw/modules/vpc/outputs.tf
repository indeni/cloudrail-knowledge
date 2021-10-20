output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.vpc.id
}

output "public_subnets" {
  description = "List of public subnets IDs"
  value       = values(aws_subnet.public)[*].id
}

output "private_subnets" {
  description = "List of private subnets"
  value       = values(aws_subnet.private)[*].id
}

output "public_nacl" {
  description = "NACL ID attached to public subnets"
  value       = aws_network_acl.public[*].id
}

output "private_nacl" {
  description = "List of NACL IDs attached to private subnets"
  value       = aws_network_acl.private[*].id
}

output "public_route_table" {
  description = "Public route table Id"
  value       = length(aws_route_table.public) > 0 ? aws_route_table.public[0].id : ""
}

output "private_route_table" {
  description = "Private route table Id"
  value       = length(aws_route_table.private) > 0 ? aws_route_table.private[0].id : ""
}
