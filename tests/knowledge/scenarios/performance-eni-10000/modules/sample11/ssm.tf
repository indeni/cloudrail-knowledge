resource "aws_ssm_parameter" "param1" {
  name  = "${local.nameA}-param1"
  type  = "String"
  value = "param1"
}

resource "aws_ssm_parameter" "param2" {
  name  = "${local.nameA}-param2"
  type  = "String"
  value = "param2"
}

resource "aws_ssm_parameter" "param3" {
  name  = "${local.nameA}-param3"
  type  = "String"
  value = "param3"
}

resource "aws_ssm_parameter" "param4" {
  name  = "${local.nameA}-param4"
  type  = "SecureString"
  value = "param4"
}

resource "aws_ssm_parameter" "param5" {
  name  = "${local.nameA}-param5"
  type  = "SecureString"
  value = "param5"
}

resource "aws_vpc_endpoint" "ssm" {
  vpc_id            = module.vpcA.vpc_id
  service_name      = "com.amazonaws.${data.aws_region.current.name}.ssm"
  vpc_endpoint_type = "Interface"
  subnet_ids        = module.vpcA.private_subnets

  security_group_ids = [
    module.vpcA.default_security_group_id,
  ]
}
