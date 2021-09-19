resource "aws_rds_cluster" "test" {
  skip_final_snapshot = true
  master_username = "asdfasdf"
  master_password = "asdf1234!!"
}