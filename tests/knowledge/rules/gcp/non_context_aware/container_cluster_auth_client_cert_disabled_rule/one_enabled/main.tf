provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster5" {
  name               = "gke-cluster-005"
  location           = "us-west1-a"
  initial_node_count = 3
}
resource "google_container_cluster" "cluster6" {
  name               = "gke-cluster-006"
  location           = "us-west1-a"
  initial_node_count = 3
  master_auth {
    client_certificate_config {
      issue_client_certificate = true
    }
  }
}
