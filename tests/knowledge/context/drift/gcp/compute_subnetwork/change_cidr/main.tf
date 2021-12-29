resource "google_compute_subnetwork" "subnet-logging3" {
  name          = "log-test-subnetwork-3"
  ip_cidr_range = "10.3.0.0/24"
  region        = "us-central1"
  network       = google_compute_network.vpc-network-2.id
}
resource "google_compute_network" "vpc-network-2" {
  name                    = "vpc-network-2"
  auto_create_subnetworks = false
}