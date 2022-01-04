resource "google_compute_network" "default" {
  name = "default-network"
}

resource "google_compute_firewall" "example_allow_ssh" {
  name          = "example-allow-ssh"
  network       = google_compute_network.default.name
  direction     = "INGRESS"
  source_ranges = "10.1.0.4/32"
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}
