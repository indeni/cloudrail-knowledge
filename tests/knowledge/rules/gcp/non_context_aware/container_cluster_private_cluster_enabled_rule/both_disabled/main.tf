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

  private_cluster_config {
    enable_private_nodes = true
    enable_private_endpoint = false
    master_ipv4_cidr_block = "172.16.0.32/28"
  }
  networking_mode = "VPC_NATIVE"
  ip_allocation_policy {
    cluster_ipv4_cidr_block = "/16"
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
