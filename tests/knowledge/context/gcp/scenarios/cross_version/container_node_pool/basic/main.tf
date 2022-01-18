
resource "google_container_cluster" "cluster6" {
  name               = "gke-cluster-006"
  location           = "us-west1-a"
  initial_node_count = 3
}

resource "google_container_node_pool" "cluster6_nodepool_1" {
  cluster    = google_container_cluster.cluster6.name
  location           = "us-west1-a"

  management {
    auto_repair = true
    auto_upgrade = true
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
    disk_size_gb = 10
    gcfs_config {
      enabled = false
      }
    disk_type = "pd-standard"
    image_type = "COS_CONTAINERD"
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 2
  }

}
