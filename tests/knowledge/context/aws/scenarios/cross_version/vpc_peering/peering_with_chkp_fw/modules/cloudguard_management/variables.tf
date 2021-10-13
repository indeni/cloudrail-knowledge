variable "vpc_id" {
  description = "VPC ID to deploy CloudGuard Management Server"
  type        = string
}

variable "subnet_id" {
  description = "ID of the subnet for Checkpoint Management Server"
  type        = string
}

variable "public_nacl" {
  description = "ID of the Network ACL associated with CHKP Management Server"
  type        = string
}

variable "name" {
  description = "Tag to identify all resources under this VPC"
  type        = string
}

variable "instance_type" {
  description = "Instance type for Checkpoint Management Server"
  type        = string
}

variable "image_id" {
  description = "AMI for Checkpoint Management Server"
  type        = string
}

variable "management_name" {
  description = "Name of the Checkpoint Management Server"
  type        = string
}

variable "hostname" {
  description = "Checkpoint Management Server Hostname"
  type        = string
  default     = "mgmt-aws"
}

variable "key_name" {
  description = "SSH Key pair name to manage Checkpoint Management Server"
  type        = string
}

variable "password_hash" {
  description = "Admin user's password hash (use command 'openssl passwd -1 PASSWORD' to get the PASSWORD's hash)"
  type        = string
}


variable "enable_instance_connect" {
  description = "Ec2 Instance Connect is not supported with versions prior to R80.40"
  type        = string
  default     = ""
}

variable "allow_upload_download" {
  description = "Automatically download Blade Contracts and other important data"
  type        = bool
  default     = false
}

variable "chkp_tag" {
  description = "The tag is used by the Security Management Server to automatically provision the Security Gateways. Must be up to 12 alphanumeric characters and unique for each environment"
  type        = string
}

variable "admin_subnet" {
  description = "IP address range allowed to manage the Checkpoint Mgmt Server"
  type        = list(string)
}

variable "gateways_addresses" {
  description = "CloudGuard gateways management subnet (private interfaces)"
  type        = list(string)
}

variable "ntp1" {
  description = "Primary NTP server"
  type        = string
  default     = "169.254.169.123"
}

variable "ntp2" {
  description = "Secondary NTP server"
  type        = string
  default     = "0.pool.ntp.org"
}

variable "shell" {
  description = "Select the shell mode: /etc/cli.sh, /bin/bash, /bin/csh, /bin/tcsh"
  type        = string
  default     = "/etc/cli.sh"
}

variable "sic_key" {
  description = "The SIC key to create trusted connections between CHKP components"
  type        = string
}
