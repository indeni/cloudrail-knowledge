resource "google_container_cluster" "example" {
  name     = "example-gke-cluster"
  location = "us-central1"
  initial_node_count       = 3
}
