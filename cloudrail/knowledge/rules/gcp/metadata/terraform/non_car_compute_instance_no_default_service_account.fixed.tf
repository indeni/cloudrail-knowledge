resource "google_service_account" "new_service_account" {
  account_id   = "new_service_account"
  display_name = "New Service Account"
}

resource "google_compute_instance" "default_service_account_test" {
  name         = "default-service-account-test"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "default"
  }

  service_account {
    email  = google_service_account.new_service_account.email
    scopes = ["cloud-platform"]
  }

}
