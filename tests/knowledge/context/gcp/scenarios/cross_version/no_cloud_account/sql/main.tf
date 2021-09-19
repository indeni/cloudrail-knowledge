resource "google_sql_database_instance" "master" {
  name             = "my-sql-instance"
  database_version = "POSTGRES_11"
  region           = "us-central1"
  deletion_protection = false

  settings {
    tier = "db-f1-micro"
  }
}
