resource "aws_cloudwatch_log_group" "log" {
  name = "${local.nameA}-cloudwatch-log-group_1"
}

resource "aws_cloudwatch_log_stream" "stream" {
  name           = "${local.nameA}-cloudwatch-log-stream_1"
  log_group_name = aws_cloudwatch_log_group.log.name
}


resource "aws_vpc_endpoint" "cloudwatch" {
  vpc_id            = module.vpcA.vpc_id
  service_name      = "com.amazonaws.${data.aws_region.current.name}.logs"
  vpc_endpoint_type = "Interface"
  subnet_ids        = module.vpcA.private_subnets

  security_group_ids = [
    module.vpcA.default_security_group_id,
  ]
}
