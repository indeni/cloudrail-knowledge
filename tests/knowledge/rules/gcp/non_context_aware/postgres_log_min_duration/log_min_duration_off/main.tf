provider "google" {
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-059" {
  name             = "test-instance-059"
  database_version = "POSTGRES_9_6"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
    database_flags {
      name = "log_min_duration_statement"
      value = -1
    }
  }
  deletion_protection = false
}
