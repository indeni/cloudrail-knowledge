resource "google_compute_network" "default" {
  name = "default-network"
}

resource "google_compute_firewall" "example_allow_rdp" {
  name      = "example-allow-rdp"
  network   = google_compute_network.default.name
  direction = "INGRESS"
  allow {
    protocol = "tcp"
    ports    = ["3389"]
  }
}
