resource "google_sql_database_instance" "instance" {
  name             = "example-instance"
  region           = "us-central1"
  database_version = "MYSQL_5_7"

  settings {
    tier = "db-f1-micro"
  }
}
