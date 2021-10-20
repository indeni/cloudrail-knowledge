output "gateway_public_ip" {
  description = "Public IP associated with Gateway external interface"
  value       = aws_eip.public.public_ip
}
