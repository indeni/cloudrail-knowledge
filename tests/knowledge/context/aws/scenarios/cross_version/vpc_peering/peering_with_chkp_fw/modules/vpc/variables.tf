variable "create_igw" {
  description = "Flag to control de creation of IGW"
  type        = bool
  default     = true
}

variable "create_public_subnets" {
  description = "Flag to control de creation of public subnets"
  type        = bool
  default     = true
}

variable "create_private_subnets" {
  description = "Flag to control de creation of private subnets"
  type        = bool
  default     = true
}

variable "cidr_block" {
  description = "The CIDR block for the VPC must be in form x.x.x.x/16-28"
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

variable "az_public_subnet" {
  description = "Mappping AZ to public subnet"
  type        = map(map(string))
  default     = {}
}

variable "az_private_subnet" {
  description = "Mappping AZ to private subnet"
  type        = map(map(string))
  default     = {}
}

variable "app_names" {
  description = "List of app names in order to create NACL for each"
  type        = list(string)
  default     = []
}
