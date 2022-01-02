
provider "google" {
  project     = "dev-for-tests"
  region      = "us-central-1"
}

resource "google_compute_subnetwork" "subnet-logging1" {
  name          = "log-test-subnetwork-1"
  ip_cidr_range = "10.1.0.0/24"
  region        = "us-central1"
  network       = google_compute_network.vpc-network-1.id

  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}
resource "google_compute_subnetwork" "subnet-logging2" {
  name          = "log-test-subnetwork-2"
  ip_cidr_range = "10.2.0.0/24"
  region        = "us-central1"
  network       = google_compute_network.vpc-network-1.id
}
resource "google_compute_network" "vpc-network-1" {
  name                    = "vpc-network-1"
  auto_create_subnetworks = false
}