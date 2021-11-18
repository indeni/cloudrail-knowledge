provider "google" {
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-079" {
  name             = "test-instance-079"
  database_version = "MYSQL_5_6"
  region           = "us-west1"


  settings {
    tier = "db-f1-micro"
    backup_configuration {
      enabled = true
      start_time = "00:00"
    }
  }
  deletion_protection = false
}

resource "google_sql_database_instance" "test-080" {
  name             = "test-instance-080"
  database_version = "MYSQL_8_0"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
    backup_configuration {
      enabled = true
      start_time = "00:00"
    }
  }
  deletion_protection = false
}
