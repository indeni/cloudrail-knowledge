module "endpoints_sg_test" {
  source              = "terraform-aws-modules/security-group/aws//modules/web"
  version             = "3.17.0"
  name                = "endpoints-sg"
  description         = "Security group for Endpoints"
  vpc_id              = module.serverlessProduction.vpc_id
  ingress_cidr_blocks = module.serverlessProduction.public_subnets_cidr_blocks
}

resource "aws_vpc_endpoint" "test" {
  count             = length(local.interface_endpoint_services)
  vpc_id            = module.serverlessProduction.vpc_id
  service_name      = local.interface_endpoint_services[count.index]
  vpc_endpoint_type = "Interface"
  subnet_ids        = module.serverlessProduction.private_subnets

  security_group_ids = [
    module.endpoints_sg_test.this_security_group_id,
  ]
}
