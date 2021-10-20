resource "aws_vpc_peering_connection" "mgmt-middle" {
  vpc_id      = module.mgmt.vpc_id
  peer_vpc_id = module.middle.vpc_id
  auto_accept = true

  tags = {
    Name = "mgmt-middle"
  }
}

resource "aws_vpc_peering_connection" "mgmt-back" {
  vpc_id      = module.mgmt.vpc_id
  peer_vpc_id = module.back.vpc_id
  auto_accept = true

  tags = {
    Name = "mgmt-back"
  }
}

resource "aws_vpc_peering_connection" "middle-back" {
  vpc_id      = module.middle.vpc_id
  peer_vpc_id = module.back.vpc_id
  auto_accept = true

  tags = {
    Name = "middle-back"
  }
}

# Routes from VPC MGMT to VPC MIDDLE

resource "aws_route" "mgmt-to-middle-00" {
  route_table_id            = module.mgmt.private_route_table_ids[0]
  destination_cidr_block    = module.middle.private_subnets_cidr_blocks[0]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-middle.id
}

resource "aws_route" "mgmt-to-middle-01" {
  route_table_id            = module.mgmt.private_route_table_ids[0]
  destination_cidr_block    = module.middle.private_subnets_cidr_blocks[1]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-middle.id
}

resource "aws_route" "mgmt-to-middle-02" {
  route_table_id            = module.mgmt.private_route_table_ids[0]
  destination_cidr_block    = module.middle.private_subnets_cidr_blocks[2]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-middle.id
}

resource "aws_route" "mgmt-to-middle-10" {
  route_table_id            = module.mgmt.private_route_table_ids[1]
  destination_cidr_block    = module.middle.private_subnets_cidr_blocks[0]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-middle.id
}

resource "aws_route" "mgmt-to-middle-11" {
  route_table_id            = module.mgmt.private_route_table_ids[1]
  destination_cidr_block    = module.middle.private_subnets_cidr_blocks[1]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-middle.id
}

resource "aws_route" "mgmt-to-middle-12" {
  route_table_id            = module.mgmt.private_route_table_ids[1]
  destination_cidr_block    = module.middle.private_subnets_cidr_blocks[2]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-middle.id
}

# Routes from VPC MGMT to VPC BACKOFFICE

resource "aws_route" "mgmt-to-back-00" {
  route_table_id            = module.mgmt.private_route_table_ids[0]
  destination_cidr_block    = module.back.private_subnets_cidr_blocks[0]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-back.id
}

resource "aws_route" "mgmt-to-back-01" {
  route_table_id            = module.mgmt.private_route_table_ids[0]
  destination_cidr_block    = module.back.private_subnets_cidr_blocks[1]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-back.id
}

resource "aws_route" "mgmt-to-back-02" {
  route_table_id            = module.mgmt.private_route_table_ids[0]
  destination_cidr_block    = module.back.private_subnets_cidr_blocks[2]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-back.id
}

resource "aws_route" "mgmt-to-back-10" {
  route_table_id            = module.mgmt.private_route_table_ids[1]
  destination_cidr_block    = module.back.private_subnets_cidr_blocks[0]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-back.id
}

resource "aws_route" "mgmt-to-back-11" {
  route_table_id            = module.mgmt.private_route_table_ids[1]
  destination_cidr_block    = module.back.private_subnets_cidr_blocks[1]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-back.id
}

resource "aws_route" "mgmt-to-back-12" {
  route_table_id            = module.mgmt.private_route_table_ids[1]
  destination_cidr_block    = module.back.private_subnets_cidr_blocks[2]
  vpc_peering_connection_id = aws_vpc_peering_connection.mgmt-back.id
}
