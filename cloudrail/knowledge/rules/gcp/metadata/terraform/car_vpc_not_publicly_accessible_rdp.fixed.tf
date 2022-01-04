resource "google_compute_network" "default" {
  name = "default-network"
}

resource "google_compute_firewall" "example_allow_rdp" {
  name          = "example-allow-rdp"
  network       = google_compute_network.default.name
  direction     = "INGRESS"
  source_ranges = "10.1.0.4/32"
  allow {
    protocol = "tcp"
    ports    = ["3389"]
  }
}
