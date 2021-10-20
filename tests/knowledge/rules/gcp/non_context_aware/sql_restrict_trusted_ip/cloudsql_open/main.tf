provider "google" {
  project     = "cloudrail-test-proj-001"
  region      = "us-west1"
}

locals {
  allowednetworks = ["0.0.0.0/0"]
}

resource "google_sql_database_instance" "cloudsql-open" {
  name             = "open-instance"
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
