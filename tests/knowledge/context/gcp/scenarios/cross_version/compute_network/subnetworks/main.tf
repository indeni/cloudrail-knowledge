resource "google_compute_subnetwork" "subnet-logging5" {
  name          = "log-test-subnetwork-5"
  ip_cidr_range = "10.5.0.0/24"
  region        = "us-central1"
  network       = google_compute_network.vpc-network-3.id

  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}
resource "google_compute_subnetwork" "subnet-logging6" {
  name          = "log-test-subnetwork-6"
  ip_cidr_range = "10.6.0.0/24"
  region        = "us-central1"
  network       = google_compute_network.vpc-network-3.id
    log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}
resource "google_compute_network" "vpc-network-3" {
  name                    = "vpc-network-3"
  auto_create_subnetworks = false
}