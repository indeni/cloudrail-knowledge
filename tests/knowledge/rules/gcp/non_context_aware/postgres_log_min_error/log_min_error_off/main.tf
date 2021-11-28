provider "google" {
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-031" {
  name             = "test-instance-031"
  database_version = "POSTGRES_9_6"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
    database_flags {
      name = "log_min_error_statement"
      value = "INFO"
    }
  }
  deletion_protection = false
}
