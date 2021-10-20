variable "vpc_id" {
  description = "VPC ID to deploy CloudGuard gateway"
  type        = string
}

variable "name" {
  description = "Tag to identify all resources under this VPC"
  type        = string
}

variable "environment" {
  description = "Tag to identify environment type under this VPC"
  type        = string
}

variable "public_subnet_id" {
  description = "ID of the public subnet"
  type        = string
}

variable "private_subnet_id" {
  description = "ID of the private subnet"
  type        = string
}

variable "public_nacl" {
  description = "ID of the Network ACL associated with public subnet"
  type        = string
}

variable "private_nacl" {
  description = "ID of the Network ACL associated with private subnet"
  type        = string
}

variable "chkp_mgmt_subnet" {
  description = "CIDR address range for the Chkp Management Server"
  type        = string
}

variable "chkp_management_security_group" {
  description = "Security Group ID associated with CHKP Management Server"
  type        = string
}

variable "gateway_name" {
  description = "Name of the Checkpoint CloudGuard Gateway"
  type        = string
}

variable "image_id" {
  description = "AMI for Checkpoint CloudGuard Gateway"
  type        = string
}

variable "instance_type" {
  description = "Instance type for Checkpoint CloudGuard Gateway"
  type        = string
}

variable "key_name" {
  description = "SSH Key pair name to manage Checkpoint CloudGuard Gateway"
  type        = string
}

variable "shell" {
  description = "Select the shell mode: /etc/cli.sh, /bin/bash, /bin/csh, /bin/tcsh"
  type        = string
  default     = "/etc/cli.sh"
}

variable "password_hash" {
  description = "Admin user's password hash (use command 'openssl passwd -1 PASSWORD' to get the PASSWORD's hash)"
  type        = string
}

variable "asn" {
  description = "The ASN that identifies the routing domain for the Security Gateways"
  type        = string
  default     = "65000"
}

variable "sic_key" {
  description = "The SIC key to create trusted connections between CHKP components"
  type        = string
}

variable "allow_upload_download" {
  description = "Automatically download Blade Contracts and other important data"
  type        = bool
  default     = false
}

variable "management_server" {
  description = "The name that represents the Security Management Server in the automatic provisioning configuration"
  type        = string
  default     = ""
}

variable "configuration_template" {
  description = "A name of a gateway configuration template in the automatic provisioning configuration"
  type        = string
  default     = ""
}

variable "control_gateway_over_private_or_public_address" {
  description = "Determines if the gateways are provisioned using their private or public address"
  type        = string
  default     = "private"
}
