provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster1" {
  name               = "gke-cluster-001"
  location           = "us-west1-a"
  initial_node_count = 3

  networking_mode = "VPC_NATIVE"
  ip_allocation_policy {
    cluster_ipv4_cidr_block = "/16"
  }
}
resource "google_container_cluster" "cluster2" {
  name               = "gke-cluster-002"
  location           = "us-west1-a"
  initial_node_count = 3

  networking_mode = "VPC_NATIVE"
  ip_allocation_policy {
    cluster_ipv4_cidr_block = "/16"
  }
}
