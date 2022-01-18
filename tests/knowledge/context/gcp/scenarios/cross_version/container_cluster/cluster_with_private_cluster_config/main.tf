resource "google_container_cluster" "cluster5" {
  name               = "gke-cluster-005"
  location           = "us-west1-a"
  initial_node_count = 3

  master_authorized_networks_config {
    cidr_blocks {
      cidr_block = "10.0.0.0/8"
    }
  }

  private_cluster_config {
    enable_private_nodes = true
    enable_private_endpoint = true
    master_ipv4_cidr_block = "172.16.2.32/28"
  }
  networking_mode = "VPC_NATIVE"
  ip_allocation_policy {
    cluster_ipv4_cidr_block = "/16"
  }
}
resource "google_container_cluster" "cluster6" {
  name               = "gke-cluster-006"
  location           = "us-west1-a"
  initial_node_count = 3

  master_authorized_networks_config {
    cidr_blocks {
      cidr_block = "10.0.0.0/8"
    }
  }
}
