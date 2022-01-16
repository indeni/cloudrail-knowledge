
resource "google_container_cluster" "cluster5" {
  name               = "gke-cluster-005"
  location           = "us-west1-a"
  initial_node_count = 3
}

resource "google_container_cluster" "cluster6" {
  name               = "gke-cluster-006"
  location           = "us-west1-a"
  initial_node_count = 3
  workload_identity_config {
    workload_pool = "dev-for-tests.svc.id.goog"
  }
  node_config {
    workload_metadata_config {
      mode = "GCE_METADATA"
    }
  }
}
