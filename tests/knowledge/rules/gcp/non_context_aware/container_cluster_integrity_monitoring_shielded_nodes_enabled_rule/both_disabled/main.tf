provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster3" {
  name               = "gke-cluster-003"
  location           = "us-west1-a"
  initial_node_count = 3
  node_config {
    shielded_instance_config {
      enable_integrity_monitoring = false
    }
  }
}

resource "google_container_cluster" "cluster4" {
  name               = "gke-cluster-004"
  location           = "us-west1-a"
  initial_node_count = 3
  node_config {
    shielded_instance_config {
      enable_integrity_monitoring = false
    }
  }
}
