provider "google" {
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-083" {
  name             = "test-instance-083"
  database_version = "MYSQL_5_6"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
    backup_configuration {
      enabled = true
      start_time = "000:00:00"
    }
  }
  deletion_protection = false
}

resource "google_sql_database_instance" "test-084" {
  name             = "test-instance-084"
  database_version = "MYSQL_8_0"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
  }
  deletion_protection = false
}

