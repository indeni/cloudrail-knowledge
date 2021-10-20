provider "google" {
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

provider "google-beta" {
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

resource "google_compute_network" "private_network" {
  name = "private-network"
}

resource "google_compute_network" "private_network_2" {
  name = "private-network-2"
}

resource "google_compute_global_address" "private_ip_1" {
  provider = google-beta

  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.private_network.id
}

resource "google_compute_global_address" "private_ip_2" {
  provider = google-beta

  name          = "private-ip-address-2"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.private_network_2.id
}

resource "google_service_networking_connection" "private_vpc_conn_1" {
  provider = google-beta

  network                 = google_compute_network.private_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_1.name]
}

resource "google_service_networking_connection" "private_vpc_conn_2" {
  provider = google-beta

  network                 = google_compute_network.private_network_2.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_2.name]
}

resource "google_sql_database_instance" "test-021" {
  name             = "test-instance-021"
  database_version = "MYSQL_5_6"
  region           = "us-west1"

  depends_on = [google_service_networking_connection.private_vpc_conn_1]

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.private_network.id
    }
  }
  deletion_protection = false
}

resource "google_sql_database_instance" "test-022" {
  name             = "test-instance-022"
  database_version = "MYSQL_8_0"
  region           = "us-west1"

  depends_on = [google_service_networking_connection.private_vpc_conn_2]

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.private_network_2.id
    }
  }
  deletion_protection = false
}
