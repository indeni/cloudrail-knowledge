provider "google-beta" {
  credentials = file("../../account.json")
  project     = "dev-joe-coniglio"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster5" {
  provider = google-beta
  name               = "gke-cluster-005"
  location           = "us-west1-a"
  initial_node_count = 3
  pod_security_policy_config {
    enabled = true
  }
}

resource "google_container_cluster" "cluster6" {
  provider = google-beta
  name               = "gke-cluster-006"
  location           = "us-west1-a"
  initial_node_count = 3
  pod_security_policy_config {
    enabled = false
  }
}
