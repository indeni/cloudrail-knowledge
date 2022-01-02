resource "google_compute_firewall" "default" {
  name    = "test-firewall"
  network = google_compute_network.default.name
  allow {
    protocol = "tcp"
    ports    = ["80", "8080", "1000-2000"]
  }
  direction = "INGRESS"
  source_ranges = ["192.168.12.34/32"]

  source_tags = ["web"]
}

resource "google_compute_network" "default" {
  name = "vpc-test"
}
output "rule_name" {
    value = google_compute_firewall.default.name
}