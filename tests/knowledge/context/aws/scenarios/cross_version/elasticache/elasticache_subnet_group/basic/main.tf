
resource "aws_vpc" "foo" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "tf-test"
  }
}

resource "aws_subnet" "foo" {
  vpc_id            = aws_vpc.foo.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "tf-test"
  }
}

resource "aws_elasticache_subnet_group" "bar" {
  name       = "tf-test-cache-subnet"
  subnet_ids = [aws_subnet.foo.id]
}

