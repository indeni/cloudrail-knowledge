output "chkp_management_security_group" {
  description = "Security Group ID associated with the chkp mgmt server"
  value       = aws_security_group.management.id
}
