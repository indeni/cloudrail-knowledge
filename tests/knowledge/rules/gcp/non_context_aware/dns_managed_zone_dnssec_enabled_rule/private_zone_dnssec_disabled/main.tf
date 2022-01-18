provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_dns_managed_zone" "example-zone" {
  name        = "example-zone"
  dns_name    = "example-0000.com."
  description = "Private DNS Zone without DNSSEC"
  visibility = "private"

  private_visibility_config {
    networks {
      network_url = google_compute_network.network-1.id
    }
    networks {
      network_url = google_compute_network.network-2.id
    }
  }
}

resource "google_compute_network" "network-1" {
  name                    = "network-1"
  auto_create_subnetworks = false
}

resource "google_compute_network" "network-2" {
  name                    = "network-2"
  auto_create_subnetworks = false
}

