
resource "google_compute_instance" "one-enabled" {
  name         = "one-enabled"
  machine_type = "n1-standard-1"
  zone         = "us-west1-a"
  project     = "dev-for-tests"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11-bullseye-v20210916"
    }
  }

  // Local SSD disk
  scratch_disk {
    interface = "SCSI"
  }

  network_interface {
    network = "default"
  }

  shielded_instance_config {
    enable_secure_boot = true
    enable_vtpm = true
    enable_integrity_monitoring = true
  }
  allow_stopping_for_update = true
}

