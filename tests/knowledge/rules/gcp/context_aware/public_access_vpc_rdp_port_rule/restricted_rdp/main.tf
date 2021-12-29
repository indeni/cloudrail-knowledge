provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_compute_address" "static" {
  name = "ipv4-address"
}

resource "google_compute_instance" "restricted-rdp" {
  name         = "restricted-gce"
  machine_type = "n1-standard-1"
  zone         = "us-west1-a"
  tags         = ["rdp-from-home"]

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

resource "google_compute_firewall" "deny-rdp" {
  name    = "deny-rdp-for-all"
  network = "default"
  priority = 15

  deny {
    protocol = "tcp"
    ports    = ["3389"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags = ["deny-rdp-for-all"]
}

resource "google_compute_firewall" "allow-specific-rdp" {
  name    = "rdp-from-home"
  network = "default"
  priority = 10

  allow {
    protocol = "tcp"
    ports    = ["3389"]
  }
  
  # Define this IP as a single /32 address
  source_ranges = ["1.2.3.4/32"]
  target_tags = ["rdp-from-home"]
}
