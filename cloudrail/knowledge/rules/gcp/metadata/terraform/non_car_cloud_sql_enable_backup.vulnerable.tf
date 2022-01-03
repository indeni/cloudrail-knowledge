resource "google_sql_database_instance" "backup-config-test" {
  name             = "backup-config-test"
  database_version = "POSTGRES_11"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"
  }
}
