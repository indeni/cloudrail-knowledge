
resource "aws_default_network_acl" "default" {
  default_network_acl_id = "acl-017afdbe80a556293"

  subnet_ids = ["subnet-096b9991973ef234f"]

  ingress {
    protocol   = -1
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  tags = {
    TerraformTag = "TerraformValue"
  }
}