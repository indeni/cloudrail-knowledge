data "google_project" "project" {
  project_id = "dev-for-tests"
}

resource "google_service_account" "custom" {
  account_id   = "customserviceaccountid"
  display_name = "My Custom Service Account"
}

resource "google_compute_instance" "test-instance" {
  name         = "test-instance"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "default"

    access_config {}
  }

  service_account {
    email  = google_service_account.custom.email
    scopes = ["compute-ro", "storage-ro"]
  }
}
