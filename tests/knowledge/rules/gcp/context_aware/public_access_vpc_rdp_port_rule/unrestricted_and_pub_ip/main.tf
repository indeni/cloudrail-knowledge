provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_compute_address" "static" {
  name = "ipv4-address"
}

resource "google_compute_instance" "unrestricted-rdp" {
  name         = "unrestricted-gce"
  machine_type = "n1-standard-1"
  zone         = "us-west1-a"
  tags         = ["rdp-from-anywhere"]

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
    subnetwork = "default"
    access_config {
      nat_ip = google_compute_address.static.address
    }
  }
}

resource "google_compute_firewall" "default" {
  name    = "rdp-from-anywhere"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["3389"]
  }
  
  source_ranges = ["0.0.0.0/0"]
  target_tags = ["rdp-from-anywhere"]
}
