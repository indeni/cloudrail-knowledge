
resource "google_compute_instance" "gce-def-01" {
  project     = "dev-for-tests"

  service_account {
    scopes = ["cloud-platform"]
  }

  name         = "gce-def-01"
  machine_type = "n1-standard-1"
  zone         = "us-west1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  // Local SSD disk
  scratch_disk {
    interface = "SCSI"
  }

  network_interface {
    network = "default"
  }
}

resource "google_compute_instance" "gce-def-02" {
  project     = "dev-for-tests"

  service_account {
    scopes = ["cloud-platform"]
  }

  name         = "gce-def-02"
  machine_type = "n1-standard-1"
  zone         = "us-west1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  // Local SSD disk
  scratch_disk {
    interface = "SCSI"
  }
 
  network_interface {
    network = "default"
  }
}
