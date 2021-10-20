provider "google" {
  project     = "cloudrail-test-proj-001"
  region      = "us-west1"
}

locals {
  allowednetworks = ["8.8.4.0/24", "35.198.0.0/16", "107.178.192.0/18"]
}

resource "google_sql_database_instance" "cloudsql-open-02" {
  name             = "open-instance-02"
  database_version = "POSTGRES_11"
  region           = "us-west1"

  settings {
    ip_configuration {
      dynamic "authorized_networks" {
        for_each = local.allowednetworks
        iterator = allowednetworks

        content {
          name  = "allowednetworks-${allowednetworks.key}"
          value = allowednetworks.value
        }
      }
    }
    tier = "db-f1-micro"
  }
  deletion_protection = false
}
