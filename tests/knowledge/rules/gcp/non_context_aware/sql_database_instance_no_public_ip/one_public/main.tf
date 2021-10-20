provider "google" {
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

provider "google-beta" {
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

resource "google_compute_network" "private_network_4" {
  name = "private-network-4"
}


resource "google_compute_global_address" "private_ip_4" {
  provider = google-beta

  name          = "private-ip-address-4"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.private_network_4.id
}

resource "google_service_networking_connection" "private_vpc_conn_4" {
  provider = google-beta

  network                 = google_compute_network.private_network_4.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_4.name]
}

resource "google_sql_database_instance" "test-025" {
  name             = "test-instance-025"
  database_version = "MYSQL_5_6"
  region           = "us-west1"

  depends_on = [google_service_networking_connection.private_vpc_conn_4]

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.private_network_4.id
    }
  }
  deletion_protection = false
}

resource "google_sql_database_instance" "test-026" {
  name             = "test-instance-026"
  database_version = "MYSQL_8_0"
  region           = "us-west1"

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = true
    }
  }
  deletion_protection = false
}

