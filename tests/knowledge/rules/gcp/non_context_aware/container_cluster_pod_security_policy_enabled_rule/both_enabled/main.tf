provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster1" {
  provider           = google-beta
  project            = "dev-for-tests"
  name               = "gke-cluster-001"
  location           = "us-west1-a"
  initial_node_count = 3
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block = "10.0.0.0/8"
    }
  }
  pod_security_policy_config {
    enabled = true
  }
}

resource "google_container_cluster" "cluster2" {
  provider           = google-beta
  project            = "dev-for-tests"
  name               = "gke-cluster-002"
  location           = "us-west1-a"
  initial_node_count = 3
  master_authorized_networks_config {
    cidr_blocks {
      cidr_block = "10.0.0.0/8"
    }
  }
  pod_security_policy_config {
    enabled = true
  }
}
