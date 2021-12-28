resource "google_sql_database_instance" "master" {
  name             = "master-instance"
  database_version = "SQLSERVER_2017_STANDARD"
  region           = "us-central1"

}
