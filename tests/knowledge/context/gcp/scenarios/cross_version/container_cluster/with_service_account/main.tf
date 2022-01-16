
resource "google_service_account" "new_service_account1" {
  account_id   = "non-default-svc-001"
  display_name = "Non Default Service Account"
}

resource "google_container_cluster" "cluster1" {
  name               = "gke-cluster-001"
  location           = "us-west1-a"
  initial_node_count = 3
}

resource "google_container_cluster" "cluster2" {
  name               = "gke-cluster-002"
  location           = "us-west1-a"
  initial_node_count = 3
  node_config {
    service_account = google_service_account.new_service_account1.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
