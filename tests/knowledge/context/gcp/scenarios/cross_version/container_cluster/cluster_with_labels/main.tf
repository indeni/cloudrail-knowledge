resource "google_container_cluster" "cluster" {
    name = "kuber"
    network = "default"
    remove_default_node_pool = true
    location = "us-central1-a"
master_authorized_networks_config {
  cidr_blocks {
    cidr_block = "0.0.0.0/0"
    display_name = "office" 
  }
}
    enable_shielded_nodes = true
    initial_node_count = 2
    authenticator_groups_config {
        security_group = "gke-security-groups@indeni.com"
    }
    ip_allocation_policy {
        cluster_ipv4_cidr_block = "10.1.0.0/20"
    }

    resource_labels = {
      foo_1 = "bar_1"
    }
}
resource "google_container_node_pool" "add_cluster" {
    name = "node-cluster"
    location = "us-central1"
    cluster = google_container_cluster.cluster.id
    node_count = 2

    node_config {
        preemptible = true
        machine_type = "e2-medium"
        disk_size_gb = "30"
    }
}