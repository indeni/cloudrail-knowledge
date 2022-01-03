resource "google_compute_address" "static" {
  name = "ipv4-address"
}

resource "google_compute_instance" "no_public_ip_test" {
  name         = "no-public-ip-test"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.static.address
    }
  }
}
