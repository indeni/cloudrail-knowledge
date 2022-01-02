provider "google" {
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-032" {
  name             = "test-instance-032"
  database_version = "POSTGRES_13"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
    database_flags {
      name = "log_connections"
      value = "off"
    }
  }
  deletion_protection = false
}
