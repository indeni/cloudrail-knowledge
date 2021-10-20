provider "google" {
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-019" {
  name             = "test-instance-019"
  database_version = "MYSQL_5_6"
  region           = "us-west1"


  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = true
    }
  }
  deletion_protection = false
}

resource "google_sql_database_instance" "test-020" {
  name             = "test-instance-020"
  database_version = "MYSQL_8_0"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = true
    }
  }
  deletion_protection = false
}
