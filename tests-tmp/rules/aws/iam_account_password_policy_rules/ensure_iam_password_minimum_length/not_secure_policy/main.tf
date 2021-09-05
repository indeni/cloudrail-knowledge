provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_user" "iam_user_1" {
  name = "iam_user_1"

}

resource "aws_iam_user_login_profile" "athena_user_1" {
  user = aws_iam_user.iam_user_1.name
  pgp_key = "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"
}


resource "aws_iam_account_password_policy" "strict" {
  minimum_password_length        = 8
  require_lowercase_characters   = true
  require_numbers                = true
  require_uppercase_characters   = true
  require_symbols                = true
  allow_users_to_change_password = true
  max_password_age               = 180
}