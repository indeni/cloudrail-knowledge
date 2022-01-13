provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}


resource "google_container_cluster" "cluster1" {
  name               = "gke-cluster-001"
  location           = "us-west1-a"
  initial_node_count = 3
  node_config {
    shielded_instance_config {
      enable_secure_boot = true
    }
  }
}

resource "google_container_cluster" "cluster2" {
  name               = "gke-cluster-002"
  location           = "us-west1-a"
  initial_node_count = 3
  node_config {
    shielded_instance_config {
      enable_secure_boot = true
    }
  }
}
