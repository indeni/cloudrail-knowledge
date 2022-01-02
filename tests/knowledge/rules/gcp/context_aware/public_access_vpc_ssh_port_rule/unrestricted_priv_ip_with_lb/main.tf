provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

# Load Balancer resources
resource "google_compute_forwarding_rule" "default" {
  name		= "ssh-forwarding"
  provider	= google-beta
  target	= google_compute_target_pool.default.self_link
  load_balancing_scheme	= "EXTERNAL"
  port_range	= "22"
  project     = "dev-for-tests"
  region = "us-west1"
}

resource "google_compute_target_pool" "default" {
  provider	= google-beta
  name		= "default-tp"
  instances	= [google_compute_instance.restricted-ssh.self_link]
  health_checks	= google_compute_http_health_check.default.*.name
  region = "us-west1"
  project     = "dev-for-tests"
}

resource "google_compute_http_health_check" "default" {
  name		= "lb-check"
  provider	= google-beta
  request_path	= "/check"
  port		= 9999
  check_interval_sec	= 1
  timeout_sec	= 1
  project     = "dev-for-tests"
}

# Compute instance resources
resource "google_compute_instance" "restricted-ssh" {
  name         = "restricted-gce"
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
  
  # No public IP
  network_interface {
    subnetwork = "default"
  }

  # Note - you can add ssh public key in a `metadata` field here or in the UI
}

# Unrestricted SSH
resource "google_compute_firewall" "ssh_from_anywhere" {
  name    = "ssh-from-anywhere"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  
  source_ranges = ["0.0.0.0/0"]
  target_tags = ["ssh-from-anywhere"]
}
