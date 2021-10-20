################################################################################
# ECS SERVICE
################################################################################
resource "aws_ecs_service" "ecs_service_2" {
  name            = "${local.name}-ECSService2"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_definition_2.arn
  launch_type     = "EC2"
  desired_count   = local.ecs_instances_service_2

  network_configuration {
    subnets         = module.vpcB.private_subnets
    security_groups = [aws_security_group.ecs_security_group_2.id]
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.ecs_lb_tg_2.arn
    container_name   = "fargate-app_2"
    container_port   = 80
  }
}

################################################################################
# ECS TASK DEFINITION
################################################################################
resource "aws_ecs_task_definition" "ecs_task_definition_2" {
  family                   = "${local.name}-b"
  task_role_arn            = aws_iam_role.ecs_task_role_2.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution_role_2.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["EC2"]
  cpu                      = "256"
  memory                   = "512"
  container_definitions    = <<DEFINITION
[
  {
    "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "${aws_cloudwatch_log_group.ecs_container_cloudwatch_loggroup_2.name}",
            "awslogs-region": "${data.aws_region.current.name}",
            "awslogs-stream-prefix": "/aws/ecs"
          }
        },
    "cpu":0,
    "dnsSearchDomains":[],
    "dnsServers":[],
    "dockerLabels":{},
    "dockerSecurityOptions":[],
    "essential":true,
    "extraHosts":[],
    "image": "nginx:latest",
    "links":[],
    "mountPoints":[],
    "name": "fargate-app_2",
    "portMappings":[
      {
        "containerPort": 80,
        "hostPort":80,
        "protocol": "tcp"
      }
    ],
    "ulimits":[],
    "volumesFrom":[],
    "environment": [
        {"name": "REGION", "value": "${data.aws_region.current.name}"},
        {"name": "S3_BUCKET", "value": "${aws_s3_bucket.ecs_source_s3bucket_2.bucket}"},
        {"name": "STREAM_NAME", "value": "${aws_kinesis_stream.ecs_kinesis_stream_2.name}"}
    ]
  }
]
DEFINITION
}

################################################################################
# SECURITY GROUP
################################################################################
resource "aws_security_group" "ecs_security_group_2" {
  name        = "${local.name}-ECSSecurityGroup_2"
  description = "ECS Allowed Ports for Service 2"
  vpc_id      = module.vpcB.vpc_id
}

resource "aws_security_group_rule" "ecs_security_group_2_rule_inbound" {
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 81
  to_port           = 81
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.ecs_security_group_2.id
}

resource "aws_security_group_rule" "ecs_security_group_2_rule_outbound" {
  type              = "egress"
  protocol          = "-1"
  from_port         = 0
  to_port           = 0
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.ecs_security_group_2.id
}

################################################################################
# IAM
################################################################################
resource "aws_iam_role" "ecs_task_role_2" {
  name = "${local.name}-ECS-Task-Role_2"

  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "ecs-tasks.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_2_s3_attachment" {
  role       = aws_iam_role.ecs_task_role_2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy" "ecs_task_role_2_s3_attachment_policy" {
  name   = "${local.name}-ECS-Task-Role-Policy_2"
  role   = aws_iam_role.ecs_task_role_2.id
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
       {
            "Effect": "Allow",
            "Action": [
                "s3:put*",
                "s3:get*",
                "s3:list*"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role" "ecs_task_execution_role_2" {
  name = "${local.name}-ECS-TaskExecution-Role_2"

  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "ecs-tasks.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs-task-execution-role-2-policy-attachment" {
  role       = aws_iam_role.ecs_task_execution_role_2.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

################################################################################
# CLOUDWATCH
################################################################################
resource "aws_cloudwatch_log_group" "ecs_container_cloudwatch_loggroup_2" {
  name = "${local.name}-cloudwatch-log-group_2"
}

resource "aws_cloudwatch_log_stream" "ecs_container_cloudwatch_logstream_2" {
  name           = "${local.name}-cloudwatch-log-stream_2"
  log_group_name = aws_cloudwatch_log_group.ecs_container_cloudwatch_loggroup_2.name
}

################################################################################
# S3
################################################################################
resource "aws_s3_bucket" "ecs_source_s3bucket_2" {
  acl = "private"
}

resource "aws_s3_bucket" "ecs_target_s3bucket_2" {
  acl = "private"
}

################################################################################
# KINESIS
################################################################################
resource "aws_kinesis_stream" "ecs_kinesis_stream_2" {
  name             = "${local.name}-stream_2"
  shard_count      = 1
  retention_period = 48

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]
}

resource "aws_kinesis_firehose_delivery_stream" "ecs_kinesis_firehosedelivery_stream_2" {
  name        = "${local.name}-firehose-delivery-stream_2"
  destination = "s3"

  kinesis_source_configuration {
    role_arn           = aws_iam_role.ecs_firehose_delivery_role_2.arn
    kinesis_stream_arn = aws_kinesis_stream.ecs_kinesis_stream_2.arn
  }
  s3_configuration {
    role_arn   = aws_iam_role.ecs_firehose_delivery_role_2.arn
    bucket_arn = aws_s3_bucket.ecs_target_s3bucket_2.arn
    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = aws_cloudwatch_log_group.ecs_container_cloudwatch_loggroup_2.name
      log_stream_name = aws_cloudwatch_log_stream.ecs_container_cloudwatch_logstream_2.name
    }
  }
}

resource "aws_iam_role" "ecs_firehose_delivery_role_2" {
  name = "${local.name}-firehose-delivery-Role_2"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "firehose.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs_delivery_role_kinesis_attachment_2" {
  role       = aws_iam_role.ecs_firehose_delivery_role_2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonKinesisReadOnlyAccess"
}


resource "aws_iam_role_policy" "ecs_firehose_delivery_role_policy_2" {
  name = "FargateTaskNotificationAccessPolicy_2"
  role = aws_iam_role.ecs_firehose_delivery_role_2.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:GetLogEvents",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:put*",
                "s3:get*",
                "s3:list*"
            ],
            "Resource": "*"
        },
         {
            "Effect": "Allow",
            "Action": [
                "kinesis:DescribeStream",
                "kinesis:GetRecords"
            ],
            "Resource": [
                "${aws_kinesis_stream.ecs_kinesis_stream_2.arn}"
            ]
        }
    ]
}
EOF
}
