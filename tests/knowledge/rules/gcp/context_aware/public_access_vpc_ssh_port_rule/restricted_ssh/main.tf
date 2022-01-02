provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_compute_address" "static" {
  name = "ipv4-address"
}

resource "google_compute_network" "vpc_network" {
  name                    = "vpc-network"
  auto_create_subnetworks = true
  mtu                     = 1460
}

resource "google_compute_instance" "restricted-ssh" {
  name         = "restricted-gce"
  machine_type = "n1-standard-1"
  zone         = "us-west1-a"
  tags         = ["ssh-from-home"]

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
    subnetwork = "vpc-network"
    access_config {
      nat_ip = google_compute_address.static.address
    }
  }
  depends_on = [google_compute_network.vpc_network]
}

resource "google_compute_firewall" "default" {
  name    = "ssh-from-home"
  network = "vpc-network"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  
  # Define this IP as a single /32 address
  source_ranges = ["1.2.3.4/32"]
  target_tags = ["ssh-from-home"]

depends_on = [google_compute_network.vpc_network]
}
