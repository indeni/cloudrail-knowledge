locals {
  iam_groups_number = 10
  iam_users_number  = 50

  prefix = "com.amazonaws.${data.aws_region.current.name}"
  interface_endpoint_services = [
    "aws.sagemaker.${data.aws_region.current.name}.notebook",
    "aws.sagemaker.${data.aws_region.current.name}.studio",
    "${local.prefix}.access-analyzer",
    "${local.prefix}.acm-pca",
    "${local.prefix}.airflow.api",
    "${local.prefix}.airflow.env",
    "${local.prefix}.airflow.ops",
    "${local.prefix}.application-autoscaling",
    "${local.prefix}.appmesh-envoy-management",
    "${local.prefix}.appstream.api",
    "${local.prefix}.appstream.streaming",
    "${local.prefix}.aps-workspaces",
    "${local.prefix}.athena",
    "${local.prefix}.auditmanager",
    "${local.prefix}.autoscaling",
    "${local.prefix}.autoscaling-plans",
    "${local.prefix}.awsconnector",
    "${local.prefix}.braket",
    "${local.prefix}.cassandra",
    "${local.prefix}.clouddirectory",
    "${local.prefix}.cloudformation",
    "${local.prefix}.cloudtrail",
    "${local.prefix}.codeartifact.api",
    "${local.prefix}.codeartifact.repositories",
    "${local.prefix}.codebuild",
    "${local.prefix}.codebuild-fips",
    "${local.prefix}.codecommit",
    "${local.prefix}.codecommit-fips",
    "${local.prefix}.codedeploy",
    "${local.prefix}.codedeploy-commands-secure",
    "${local.prefix}.codeguru-profiler",
    "${local.prefix}.codeguru-reviewer",
    "${local.prefix}.codepipeline",
    "${local.prefix}.codestar-connections.api",
    "${local.prefix}.config",
    "${local.prefix}.databrew",
    "${local.prefix}.dataexchange",
    "${local.prefix}.datasync",
    "${local.prefix}.ebs",
    "${local.prefix}.ec2",
    "${local.prefix}.ec2messages",
    "${local.prefix}.ecr.api",
    "${local.prefix}.ecr.dkr",
    "${local.prefix}.ecs",
    "${local.prefix}.ecs-agent",
    "${local.prefix}.ecs-telemetry",
    "${local.prefix}.elasticbeanstalk",
    "${local.prefix}.elasticbeanstalk-health",
    "${local.prefix}.elasticfilesystem",
    "${local.prefix}.elasticfilesystem-fips",
    "${local.prefix}.elasticloadbalancing",
    "${local.prefix}.elasticmapreduce",
    "${local.prefix}.emr-containers",
    "${local.prefix}.events",
    "${local.prefix}.execute-api",
    "${local.prefix}.fis",
    "${local.prefix}.git-codecommit",
    "${local.prefix}.git-codecommit-fips",
    "${local.prefix}.glue",
    "${local.prefix}.imagebuilder",
    "${local.prefix}.iotsitewise.api",
    "${local.prefix}.iotsitewise.data",
    "${local.prefix}.kendra",
    "${local.prefix}.kinesis-firehose",
    "${local.prefix}.kinesis-streams",
    "${local.prefix}.kms",
    "${local.prefix}.license-manager",
    "${local.prefix}.license-manager-fips",
    "${local.prefix}.logs",
    "${local.prefix}.macie2",
    "${local.prefix}.monitoring",
    "${local.prefix}.rds",
    "${local.prefix}.rds-data",
    "${local.prefix}.redshift",
    "${local.prefix}.redshift-fips",
    "${local.prefix}.rekognition",
    "${local.prefix}.rekognition-fips",
    "${local.prefix}.s3",
    "${local.prefix}.sagemaker.api",
    "${local.prefix}.sagemaker.featurestore-runtime",
    "${local.prefix}.sagemaker.runtime",
    "${local.prefix}.sagemaker.runtime-fips",
    "${local.prefix}.secretsmanager",
    "${local.prefix}.servicecatalog",
    "${local.prefix}.sms",
    "${local.prefix}.sms-fips",
    "${local.prefix}.sns",
    "${local.prefix}.sqs",
    "${local.prefix}.ssm",
    "${local.prefix}.ssmmessages",
    "${local.prefix}.states",
    "${local.prefix}.storagegateway",
    "${local.prefix}.sts",
    "${local.prefix}.synthetics",
    "${local.prefix}.textract",
    "${local.prefix}.textract-fips",
    "${local.prefix}.transcribe",
    "${local.prefix}.transcribestreaming",
    "${local.prefix}.workspaces",
  ]

  projects = {
    serverlessProduction = {
      cidr_block        = "10.10.0.0/16",
      public_subnets    = ["10.10.0.0/24", "10.10.1.0/24"],
      private_subnets   = ["10.10.10.0/24", "10.10.11.0/24", "10.10.12.0/24", "10.10.13.0/24"],
      num_lambdas       = 57,
      num_ec2_instances = 20,
      num_rds_instances = 12,
    },
    serverlessStaging = {
      cidr_block        = "10.20.0.0/16",
      public_subnets    = ["10.20.0.0/24", "10.20.1.0/24"],
      private_subnets   = ["10.20.10.0/24", "10.20.11.0/24", "10.20.12.0/24", "10.20.13.0/24"],
      num_lambdas       = 50,
      num_rds_instances = 12,
    },
    serverlessTesting = {
      cidr_block        = "10.30.0.0/16",
      public_subnets    = ["10.30.0.0/24", "10.30.1.0/24"],
      private_subnets   = ["10.30.10.0/24", "10.30.11.0/24", "10.30.12.0/24", "10.30.13.0/24"],
      num_lambdas       = 26,
      num_rds_instances = 6,
    }
  }
}

data "aws_region" "current" {}

data "aws_availability_zones" "available" {
  state = "available"
}

module "serverlessProduction" {
  source             = "terraform-aws-modules/vpc/aws"
  version            = "2.77.0"
  cidr               = local.projects["serverlessProduction"].cidr_block
  azs                = data.aws_availability_zones.available.names
  private_subnets    = local.projects["serverlessProduction"].private_subnets
  public_subnets     = local.projects["serverlessProduction"].public_subnets
  enable_nat_gateway = false
  enable_vpn_gateway = false
}

module "serverlessStaging" {
  source             = "terraform-aws-modules/vpc/aws"
  version            = "2.77.0"
  cidr               = local.projects["serverlessStaging"].cidr_block
  azs                = data.aws_availability_zones.available.names
  private_subnets    = local.projects["serverlessStaging"].private_subnets
  public_subnets     = local.projects["serverlessStaging"].public_subnets
  enable_nat_gateway = false
  enable_vpn_gateway = false
}

module "serverlessTesting" {
  source             = "terraform-aws-modules/vpc/aws"
  version            = "2.77.0"
  cidr               = local.projects["serverlessTesting"].cidr_block
  azs                = data.aws_availability_zones.available.names
  private_subnets    = local.projects["serverlessTesting"].private_subnets
  public_subnets     = local.projects["serverlessTesting"].public_subnets
  enable_nat_gateway = false
  enable_vpn_gateway = false
}

module "ec2_sg_serverlessProduction" {
  count               = local.projects["serverlessProduction"].num_ec2_instances
  source              = "terraform-aws-modules/security-group/aws//modules/web"
  version             = "3.17.0"
  name                = "ec2-sg"
  description         = "Security group for EC2"
  vpc_id              = module.serverlessProduction.vpc_id
  ingress_cidr_blocks = ["0.0.0.0/0"]
}
