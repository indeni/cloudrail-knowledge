locals {
  default_subnet_list = tolist(data.aws_subnet_ids.default.ids)
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id
}

data "aws_kms_key" "by_alias" {
  key_id = "alias/aws/fsx"
}

resource "aws_directory_service_directory" "test" {
  name     = "corp.notexample.com"
  password = "SuperSecretPassw0rd"
  edition  = "Standard"
  type     = "MicrosoftAD"

  vpc_settings {
    vpc_id = data.aws_vpc.default.id

    subnet_ids = [
      local.default_subnet_list[0],
      local.default_subnet_list[1]
    ]
  }
}

resource "aws_fsx_windows_file_system" "test" {
  storage_capacity    = 32
  subnet_ids          = [local.default_subnet_list[0]]
  throughput_capacity = 8
  active_directory_id = aws_directory_service_directory.test.id
  kms_key_id          = data.aws_kms_key.by_alias.arn

}
