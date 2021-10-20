
provider "aws" {
  region = "us-east-1"
}

locals {
  test_description = "resource (ECS) is using a SG with port 22 allowed - all built with modules"
  test_name        = "PublicAccessSecurityGroupsPort test - use case 6"
  cidr_block       = "10.10.0.0/16"
}

module "vpc_example_complete-vpc" {
  source  = "terraform-aws-modules/vpc/aws//examples/complete-vpc"
}

module "ssh_security_group" {
  source = "terraform-aws-modules/security-group/aws//modules/ssh"
  vpc_id = module.vpc_example_complete-vpc.vpc_id
  name = "somename"
  ingress_cidr_blocks = ["0.0.0.0/0"]
}

module "ecs_cluster" {
  source = "infrablocks/ecs-cluster/aws"

  vpc_id = module.vpc_example_complete-vpc.vpc_id
  subnet_ids = module.vpc_example_complete-vpc.public_subnets
  region = "us-east-1"
  security_groups = [module.ssh_security_group.this_security_group_id]

  component = "important-component"
  deployment_identifier = "production"

  cluster_name = "services"
  cluster_instance_ssh_public_key_path = "./main.tf"
  cluster_instance_type = "t2.small"

  cluster_minimum_size = 2
  cluster_maximum_size = 10
  cluster_desired_capacity = 4
}

module "ecs_service" {
  source = "infrablocks/ecs-service/aws"

  vpc_id = module.vpc_example_complete-vpc.vpc_id
  region = "us-east-1"

  component = "important-component"
  deployment_identifier = "production"

  service_name = "web-app"
  service_image = "images/web-app:0.3.1"
  service_port = "8000"
  service_command = ["node", "blah"]

  service_desired_count = "3"
  service_deployment_maximum_percent = "50"
  service_deployment_minimum_healthy_percent = "200"

  service_elb_name = "elb-service-web-app"

  service_role = "arn:aws:iam::151388205202:role/service-task-role"

  service_volumes = [
    {
      name = "data"
    }
  ]

  ecs_cluster_id = module.ecs_cluster.cluster_id
  ecs_cluster_service_role_arn = "arn:aws:iam::151388205202:role/cluster-service-role-web-app"
}

//network_configuration {
//    subnets = [aws_subnet.main-public-subnet.id]
//    security_groups = [aws_security_group.sg.id]
//    assign_public_ip = true
//  }
