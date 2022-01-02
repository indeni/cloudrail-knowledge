provider "google" {
  region      = "us-west1"
}

resource "google_sql_database_instance" "test-063" {
  name             = "test-instance-063"
  database_version = "SQLSERVER_2017_STANDARD"
  region           = "us-west1"
  root_password    = "donthardcodepasswords3v3r"

  settings {
    tier = "db-custom-1-3840"
    database_flags {
      name = "cross db ownership chaining"
      value = "on"
    }
  }
  deletion_protection = false
}
