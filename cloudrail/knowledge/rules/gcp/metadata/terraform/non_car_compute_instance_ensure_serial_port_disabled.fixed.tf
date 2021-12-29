resource "google_compute_instance" "example" {
  name         = "example-compute-instance"
  machine_type = "n2-standard-2"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  metadata = {
    serial-port-enable = false
  }

}
