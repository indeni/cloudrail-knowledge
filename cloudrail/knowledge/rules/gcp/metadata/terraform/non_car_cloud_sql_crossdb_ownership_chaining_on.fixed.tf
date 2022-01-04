resource "google_sql_database_instance" "master" {
  name             = "master-instance"
  database_version = "SQLSERVER_2019_STANDARD"
  region           = "us-central1"

  settings {
    database_flags {
      name  = "cross db ownership chaining"
      value = "off"
    }
  }
}
