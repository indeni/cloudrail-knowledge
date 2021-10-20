data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

resource "aws_instance" "publicA" {
  count                  = local.projects["serverlessProduction"].num_ec2_instances
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t2.micro"
  iam_instance_profile   = aws_iam_instance_profile.publicA[count.index].id
  subnet_id              = module.serverlessProduction.public_subnets[0]
  vpc_security_group_ids = [module.ec2_sg_serverlessProduction[count.index].this_security_group_id]

  user_data = <<-EOF
    #!/bin/bash
    sudo yum update -y
    sudo yum install httpd -y
    sudo systemctl enable httpd
    sudo systemctl start httpd
    echo "<html><body><div>Hello, world!</div></body></html>" > /var/www/html/index.html
    EOF
}

resource "aws_iam_instance_profile" "publicA" {
  count = local.projects["serverlessProduction"].num_ec2_instances
  name  = "publicA-${count.index}"
  role  = aws_iam_role.publicA[count.index].name
}

resource "aws_iam_role" "publicA" {
  count = local.projects["serverlessProduction"].num_ec2_instances
  name  = "publicA-${count.index}"
  path  = "/"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}

resource "aws_instance" "publicB" {
  count                  = local.projects["serverlessProduction"].num_ec2_instances
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t2.micro"
  iam_instance_profile   = aws_iam_instance_profile.publicB[count.index].id
  subnet_id              = module.serverlessProduction.public_subnets[1]
  vpc_security_group_ids = [module.ec2_sg_serverlessProduction[count.index].this_security_group_id]

  user_data = <<-EOF
    #!/bin/bash
    sudo yum update -y
    sudo yum install httpd -y
    sudo systemctl enable httpd
    sudo systemctl start httpd
    echo "<html><body><div>Hello, world!</div></body></html>" > /var/www/html/index.html
    EOF
}

resource "aws_iam_instance_profile" "publicB" {
  count = local.projects["serverlessProduction"].num_ec2_instances
  name  = "publicB-${count.index}"
  role  = aws_iam_role.publicA[count.index].name
}

resource "aws_iam_role" "publicB" {
  count = local.projects["serverlessProduction"].num_ec2_instances
  name  = "publicB-${count.index}"
  path  = "/"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}

# Private EC2 instance using public instance profile
resource "aws_instance" "privateA" {
  count                  = local.projects["serverlessProduction"].num_ec2_instances
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t2.micro"
  iam_instance_profile   = aws_iam_instance_profile.publicA[count.index].id
  subnet_id              = module.serverlessProduction.private_subnets[0]
  vpc_security_group_ids = [module.ec2_sg_serverlessProduction[count.index].this_security_group_id]

  user_data = <<-EOF
    #!/bin/bash
    sudo yum update -y
    sudo yum install httpd -y
    sudo systemctl enable httpd
    sudo systemctl start httpd
    echo "<html><body><div>Hello, world!</div></body></html>" > /var/www/html/index.html
    EOF
}

# Private EC2 instance using public instance profile
resource "aws_instance" "privateB" {
  count                  = local.projects["serverlessProduction"].num_ec2_instances
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t2.micro"
  iam_instance_profile   = aws_iam_instance_profile.publicB[count.index].id
  subnet_id              = module.serverlessProduction.public_subnets[1]
  vpc_security_group_ids = [module.ec2_sg_serverlessProduction[count.index].this_security_group_id]

  user_data = <<-EOF
    #!/bin/bash
    sudo yum update -y
    sudo yum install httpd -y
    sudo systemctl enable httpd
    sudo systemctl start httpd
    echo "<html><body><div>Hello, world!</div></body></html>" > /var/www/html/index.html
    EOF
}
