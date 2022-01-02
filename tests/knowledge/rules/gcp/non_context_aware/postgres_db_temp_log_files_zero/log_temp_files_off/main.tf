provider "google" {
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-051" {
  name             = "test-instance-051"
  database_version = "POSTGRES_9_6"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
    database_flags {
      name = "log_temp_files"
      value = 0
    }
  }
  deletion_protection = false
}

