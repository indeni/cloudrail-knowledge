provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

provider "google-beta" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

# Load Balancer resources
resource "google_compute_forwarding_rule" "default" {
  name		= "rdp-forwarding"
  provider	= google-beta
  target	= google_compute_target_pool.default.self_link
  load_balancing_scheme	= "EXTERNAL"
  port_range	= "3389"
}

resource "google_compute_target_pool" "default" {
  provider	= google-beta
  name		= "default-tp"
  instances	= [google_compute_instance.restricted-rdp.self_link]
  health_checks	= google_compute_http_health_check.default.*.name
}

resource "google_compute_http_health_check" "default" {
  name		= "lb-check"
  provider	= google-beta
  request_path	= "/check"
  port		= 9999
  check_interval_sec	= 1
  timeout_sec	= 1
}

# Compute instance resources
resource "google_compute_instance" "restricted-rdp" {
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
}

# Unrestricted RDP
resource "google_compute_firewall" "rdp_from_anywhere" {
  name    = "rdp-from-anywhere"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["3389"]
  }
  
  source_ranges = ["0.0.0.0/0"]
  target_tags = ["rdp-from-anywhere"]
}
