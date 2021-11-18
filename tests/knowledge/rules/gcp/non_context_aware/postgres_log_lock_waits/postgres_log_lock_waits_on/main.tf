provider "google" {
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-035" {
  name             = "test-instance-035"
  database_version = "POSTGRES_9_6"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
    database_flags {
      name = "log_lock_waits"
      value = "on"
    }
  }
  deletion_protection = false
}
