provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_service_account" "new_service_account1" {
  account_id   = "non-default-svc-001"
  display_name = "Non Default Service Account"
}

resource "google_container_cluster" "cluster5" {
  name               = "gke-cluster-005"
  location           = "us-west1-a"
  initial_node_count = 3
  node_config {
    service_account = google_service_account.new_service_account1.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

resource "google_container_cluster" "cluster6" {
  name               = "gke-cluster-006"
  location           = "us-west1-a"
  initial_node_count = 3
}
