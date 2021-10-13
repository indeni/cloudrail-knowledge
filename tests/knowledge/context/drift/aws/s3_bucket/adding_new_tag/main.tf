
resource "aws_s3_bucket" "a" {
  acl = "private"

  versioning { # Disabled in live env
    enabled = true
  }

  server_side_encryption_configuration { # Disabled in live env
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Name        = "BucketA"
    Environment = "Dev"
  }
}


resource "aws_s3_bucket" "b" {
  acl = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = { # Added new tag in live env
    Name        = "BucketB"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "c" {
  acl = "private"

  versioning {
    enabled = true # Disabled in live env
  }


  tags = {
    Name        = "BucketC"
    Environment = "Dev"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}

# Changed default security group in live env
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  tags = {
    Name = "HelloWorld"
  }
}
