provider "google" {
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

resource "google_compute_instance" "can-fwd-06" {
  name         = "can-fwd-06"
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

resource "google_compute_instance" "can-fwd-07" {
  name         = "can-fwd-07"
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
