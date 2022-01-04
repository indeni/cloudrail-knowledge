resource "google_compute_network" "default" {
  name = "default-network"
}

resource "google_compute_firewall" "example_allow_ssh" {
  name          = "example-allow-ssh"
  network       = google_compute_network.default.name
  direction     = "INGRESS"
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}
