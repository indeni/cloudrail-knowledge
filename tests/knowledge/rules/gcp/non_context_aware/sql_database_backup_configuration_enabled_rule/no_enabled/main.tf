provider "google" {
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-081" {
  name             = "test-instance-081"
  database_version = "MYSQL_5_6"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
  }
  deletion_protection = false
}

resource "google_sql_database_instance" "test-082" {
  name             = "test-instance-082"
  database_version = "MYSQL_8_0"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
  }
  deletion_protection = false
}
