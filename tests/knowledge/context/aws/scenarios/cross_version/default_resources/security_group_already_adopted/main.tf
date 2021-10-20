resource "aws_default_security_group" "default" {
  vpc_id = "vpc-0bb120e294ef53f94"

  egress = [
    {
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = [
        "0.0.0.0/0"],
      description = null,
      ipv6_cidr_blocks = null,
      prefix_list_ids = null,
      security_groups = null,
      self = null
    }
  ]

  tags = {
    TerraformTag = "TerraformValue"
  }
}