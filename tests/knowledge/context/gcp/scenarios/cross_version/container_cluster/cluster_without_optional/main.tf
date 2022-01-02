resource "google_container_cluster" "cluster" {
    name = "kuber-2"
    network = "default"
    remove_default_node_pool = true
    location = "us-central1-a"
    enable_shielded_nodes = false
    initial_node_count = 2
    ip_allocation_policy {
        cluster_ipv4_cidr_block = "10.2.0.0/20"
    }
}
resource "google_container_node_pool" "add_cluster" {
    name = "node-cluster-2"
    location = "us-central1"
    cluster = google_container_cluster.cluster.id
    node_count = 2

    node_config {
        preemptible = true
        machine_type = "e2-medium"
        disk_size_gb = "30"
    }
}