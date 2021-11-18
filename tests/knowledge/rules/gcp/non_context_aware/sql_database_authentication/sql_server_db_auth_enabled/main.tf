provider "google" {
  project     = "dev-tomer"
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-073" {
  name             = "test-instance-073"
  database_version = "SQLSERVER_2017_STANDARD"
  region           = "us-west1"
  root_password    = "donthardcodepasswords3v3r"

  settings {
    tier = "db-custom-1-3840"
    database_flags {
      name = "contained database authentication"
      value = "on"
    }
  }
  deletion_protection = false
}

resource "google_sql_database_instance" "test-074" {
  name             = "test-instance-074"
  database_version = "SQLSERVER_2017_WEB"
  region           = "us-west1"
  root_password    = "donthardcodepasswords3v3r"

  settings {
    tier = "db-custom-1-3840"
  }
  deletion_protection = false
}
