variable "cidr_block" {
  description = "The CIDR block for the VPC, must be in form x.x.x.x/16-28"
  type        = string
}

variable "subnet_cidr" {
  description = "The CIDR block for the Subnet, must be in form x.x.x.x/16-28"
  type        = string
}


variable "name" {
  description = "Name to be used as identifier on all resources"
  type        = string
}

variable "environment" {
  description = "Specify the environment type (dev, stage, prod)"
  type        = string
}

variable "app_name" {
  description = "Identifier of VPC app resources"
  type        = string
}

variable "provisioning_tag_value" {
  description = "Tag value for CHKP autoprovisioning"
  type        = string
}

variable "instance_image" {
  description = "AMI ID"
  type        = string
}

variable "instance_type" {
  description = "Instance type"
  type        = string
}

variable "key_name" {
  description = "SSH key name"
  type        = string
}

variable "admin_subnet" {
  description = "IP address range allowed to manage instances"
  type        = string
}

variable "spoke_service_access" {
  description = "IP address range allowed into this spoke"
  type        = string
}
