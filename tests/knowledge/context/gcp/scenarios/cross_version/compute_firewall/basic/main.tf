locals {
  prefix_name = "crtest"

}

resource "google_compute_network" "vpc_network" {
  name = "${local.prefix_name}-vpc"
}

resource "google_compute_firewall" "firewall1" {
  name               = "${local.prefix_name}firewall1"
  description        = "Creates firewall rule targeting tagged instances"
  network            = google_compute_network.vpc_network.name
  destination_ranges = ["8.8.8.8"]
  direction          = "EGRESS"

  allow {
    protocol = "tcp"
    ports    = ["80", "8080", "1000-2000"]
  }

  log_config {
    metadata = "INCLUDE_ALL_METADATA"
  }

}

resource "google_compute_firewall" "firewall2" {
  name          = "${local.prefix_name}firewall2"
  description   = "Creates firewall rule targeting tagged instances"
  network       = google_compute_network.vpc_network.name
  source_ranges = ["8.8.8.8"]
  direction     = "INGRESS"

  deny {
    protocol = "esp"
  }

  log_config {
    metadata = "EXCLUDE_ALL_METADATA"
  }

}
