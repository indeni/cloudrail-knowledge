data "google_project" "project" {
  project_id = "dev-for-tests"
}

resource "google_compute_instance" "gce-def-03" {
  project     = "dev-for-tests"

  service_account {
    email  = "${data.google_project.project.number}-compute@developer.gserviceaccount.com"
    scopes = ["cloud-platform"]
  }

  name         = "gce-def-03"
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

resource "google_service_account" "new_service_account2" {
  project     = "dev-for-tests"
  account_id   = "non-default-svc-002"
  display_name = "Non Default Service Account"
}

resource "google_compute_instance" "gce-no-def-01" {
  project     = "dev-for-tests"

  service_account {
    email  = google_service_account.new_service_account2.email
    scopes = ["cloud-platform"]
  }

  name         = "gce-no-def-01"
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
