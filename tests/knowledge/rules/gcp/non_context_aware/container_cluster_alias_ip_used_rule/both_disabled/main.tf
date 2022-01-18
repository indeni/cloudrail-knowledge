provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster3" {
  name               = "gke-cluster-003"
  location           = "us-west1-a"
  initial_node_count = 3
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block = "10.0.0.0/8"
    }
  }
}

resource "google_container_cluster" "cluster4" {
  name               = "gke-cluster-004"
  location           = "us-west1-a"
  initial_node_count = 3
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block = "10.0.0.0/8"
    }
  }
}
