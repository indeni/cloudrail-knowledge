
resource "google_compute_instance" "test-instance" {
  name         = "test-instance"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "default"

    access_config {}
  }

  service_account {
    scopes = ["cloud-platform"]
  }
}
