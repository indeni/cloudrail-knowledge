data "aws_vpc" "selected" {
  id = "vpc-0bb120e294ef53f94"
}


resource "aws_default_route_table" "example" {
  default_route_table_id = data.aws_vpc.selected.main_route_table_id

  route = [
    {
      cidr_block = "10.0.1.0/24"
      gateway_id = "igw-0117762a7c52abc7b",
      destination_prefix_list_id = null,
      egress_only_gateway_id = null,
      instance_id = null,
      ipv6_cidr_block = null,
      nat_gateway_id = null,
      network_interface_id = null,
      transit_gateway_id = null,
      vpc_endpoint_id = null,
      vpc_peering_connection_id = null
    }
  ]

  tags = {
    TerraformTag = "TerraformValue"
  }
}