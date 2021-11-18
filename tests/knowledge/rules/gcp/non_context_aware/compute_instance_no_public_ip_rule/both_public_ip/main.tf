resource "google_compute_address" "static1" {
  name = "ipv4-address1"
}

resource "google_compute_address" "static2" {
  name = "ipv4-address2"
}

resource "google_compute_instance" "gce-pub-01" {
  name         = "gce-pub-01"
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
    subnetwork = "default"
    access_config {
      nat_ip = google_compute_address.static1.address
    }
  }
}

resource "google_compute_instance" "gce-pub-02" {
  name         = "gce-pub-02"
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
    subnetwork = "default"
    access_config {
      nat_ip = google_compute_address.static2.address
    }
  }
}
