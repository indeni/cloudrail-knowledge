provider "google" {
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

resource "google_compute_instance" "can-fwd-03" {
  name         = "can-fwd-03"
  machine_type = "n1-standard-1"
  zone         = "us-west1-a"
  can_ip_forward = true

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

resource "google_compute_instance" "can-fwd-04" {
  name         = "can-fwd-04"
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
