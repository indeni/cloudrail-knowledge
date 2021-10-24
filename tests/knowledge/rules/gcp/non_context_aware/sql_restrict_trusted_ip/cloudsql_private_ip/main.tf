provider "google" {
  project     = "cloudrail-test-proj-001"
  region      = "us-west1"
}

provider "google-beta" {
  project     = "cloudrail-test-proj-001"
  region      = "us-west1"
}

resource "google_compute_network" "private_network" {
  provider = google-beta

  name = "private-network"
}

resource "google_compute_global_address" "private_ip_address" {
  provider = google-beta

  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.private_network.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  provider = google-beta

  network                 = google_compute_network.private_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

resource "google_sql_database_instance" "cloudsql-closed" {
  name             = "closed-instance"
  database_version = "POSTGRES_11"
  region           = "us-west1"
  depends_on = [google_service_networking_connection.private_vpc_connection]
  settings {
    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.private_network.id
    }
    tier = "db-f1-micro"
  }
  deletion_protection = false
}
