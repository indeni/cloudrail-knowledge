resource "google_sql_database_instance" "example" {
  name             = "example-instance"
  database_version = "MYSQL_5_7"
  settings {
    tier = "db-f1-micro"
    ip_configuration {
        require_ssl = true
    }
  }
}
