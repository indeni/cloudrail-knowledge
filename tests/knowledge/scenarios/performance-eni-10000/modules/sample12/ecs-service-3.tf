################################################################################
# ECS SERVICE
################################################################################
resource "aws_ecs_service" "ecs_service_3" {
  name            = "${local.nameB}-ECSService3"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_definition_3.arn
  launch_type     = "FARGATE"
  desired_count   = local.ecs_instances_service_3

  network_configuration {
    subnets         = module.vpcB.private_subnets
    security_groups = [aws_security_group.ecs_security_group_3.id]
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.ecs_lb_tg_3.arn
    container_name   = "fargate-app_3"
    container_port   = 82
  }
}

################################################################################
# ECS TASK DEFINITION
################################################################################
resource "aws_ecs_task_definition" "ecs_task_definition_3" {
  family                   = "test"
  task_role_arn            = aws_iam_role.ecs_task_role_3.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution_role_3.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  container_definitions    = <<DEFINITION
[
  {
    "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "${aws_cloudwatch_log_group.ecs_container_cloudwatch_loggroup_3.name}",
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
    "name": "fargate-app_3",
    "portMappings":[
      {
        "containerPort": 82,
        "hostPort":82,
        "protocol": "tcp"
      }
    ],
    "ulimits":[],
    "volumesFrom":[],
    "environment": [
        {"name": "REGION", "value": "${data.aws_region.current.name}"},
        {"name": "S3_BUCKET", "value": "${aws_s3_bucket.ecs_source_s3bucket_3.bucket}"},
        {"name": "STREAM_NAME", "value": "${aws_kinesis_stream.ecs_kinesis_stream_3.name}"}
    ]
  }
]
DEFINITION
}

################################################################################
# SECURITY GROUP
################################################################################
resource "aws_security_group" "ecs_security_group_3" {
  name        = "${local.nameB}-ECSSecurityGroup_3"
  description = "ECS Allowed Ports for Service 3"
  vpc_id      = module.vpcB.vpc_id
}

resource "aws_security_group_rule" "ecs_security_group_3_rule_inbound" {
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 82
  to_port           = 82
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.ecs_security_group_3.id
}

resource "aws_security_group_rule" "ecs_security_group_3_rule_outbound" {
  type              = "egress"
  protocol          = "-1"
  from_port         = 0
  to_port           = 0
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.ecs_security_group_3.id
}

################################################################################
# IAM
################################################################################
resource "aws_iam_role" "ecs_task_role_3" {
  name = "${local.nameB}-ECS-Task-Role_3"

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

resource "aws_iam_role_policy_attachment" "ecs_task_role_3_s3_attachment" {
  role       = aws_iam_role.ecs_task_role_3.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy" "ecs_task_role_3_s3_attachment_policy" {
  name   = "${local.nameB}-ECS-Task-Role-Policy_3"
  role   = aws_iam_role.ecs_task_role_3.id
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

resource "aws_iam_role" "ecs_task_execution_role_3" {
  name = "${local.nameB}-ECS-TaskExecution-Role_3"

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

resource "aws_iam_role_policy_attachment" "ecs-task-execution-role-3-policy-attachment" {
  role       = aws_iam_role.ecs_task_execution_role_3.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

################################################################################
# CLOUDWATCH
################################################################################
resource "aws_cloudwatch_log_group" "ecs_container_cloudwatch_loggroup_3" {
  name = "${local.nameB}-cloudwatch-log-group_3"
}

resource "aws_cloudwatch_log_stream" "ecs_container_cloudwatch_logstream_3" {
  name           = "${local.nameB}-cloudwatch-log-stream_3"
  log_group_name = aws_cloudwatch_log_group.ecs_container_cloudwatch_loggroup_3.name
}

################################################################################
# S3
################################################################################
resource "aws_s3_bucket" "ecs_source_s3bucket_3" {
  acl = "private"
}

resource "aws_s3_bucket" "ecs_target_s3bucket_3" {
  acl = "private"
}

################################################################################
# KINESIS
################################################################################
resource "aws_kinesis_stream" "ecs_kinesis_stream_3" {
  name             = "${local.name}-stream_3"
  shard_count      = 1
  retention_period = 48

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]
}

resource "aws_kinesis_firehose_delivery_stream" "ecs_kinesis_firehosedelivery_stream_3" {
  name        = "${local.name}-firehose-delivery-stream_3"
  destination = "s3"

  kinesis_source_configuration {
    role_arn           = aws_iam_role.ecs_firehose_delivery_role_3.arn
    kinesis_stream_arn = aws_kinesis_stream.ecs_kinesis_stream_3.arn
  }
  s3_configuration {
    role_arn   = aws_iam_role.ecs_firehose_delivery_role_3.arn
    bucket_arn = aws_s3_bucket.ecs_target_s3bucket_3.arn
    cloudwatch_logging_options {
      enabled         = true
      log_group_name  = aws_cloudwatch_log_group.ecs_container_cloudwatch_loggroup_3.name
      log_stream_name = aws_cloudwatch_log_stream.ecs_container_cloudwatch_logstream_3.name
    }
  }
}

resource "aws_iam_role" "ecs_firehose_delivery_role_3" {
  name = "${local.name}-firehose-delivery-Role_3"

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

resource "aws_iam_role_policy_attachment" "ecs_delivery_role_kinesis_attachment_3" {
  role       = aws_iam_role.ecs_firehose_delivery_role_3.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonKinesisReadOnlyAccess"
}


resource "aws_iam_role_policy" "ecs_firehose_delivery_role_policy_3" {
  name = "FargateTaskNotificationAccessPolicy_3"
  role = aws_iam_role.ecs_firehose_delivery_role_3.id

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
                "${aws_kinesis_stream.ecs_kinesis_stream_3.arn}"
            ]
        }
    ]
}
EOF
}
