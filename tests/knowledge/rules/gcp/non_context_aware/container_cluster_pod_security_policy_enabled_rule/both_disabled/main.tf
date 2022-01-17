provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster3" {
  provider           = google-beta
  project            = "dev-for-tests"
  location           = "us-west1-a"
  name               = "gke-cluster-003"
  initial_node_count = 3
  pod_security_policy_config {
    enabled = false
  }
}

resource "google_container_cluster" "cluster4" {
  provider           = google-beta
  project            = "dev-for-tests"
  name               = "gke-cluster-004"
  location           = "us-west1-a"
  initial_node_count = 3
}
