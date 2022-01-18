
resource "google_container_cluster" "cluster5" {
  name               = "gke-cluster-005"
  location           = "us-west1-a"
  initial_node_count = 3
  node_config {
    metadata = {
      disable-legacy-endpoints = "true"
      some_test = "true"
    }
  }
}

resource "google_container_cluster" "cluster6" {
  name               = "gke-cluster-006"
  location           = "us-west1-a"
  initial_node_count = 3
  node_config {
    metadata = {
      disable-legacy-endpoints = "false"
    }
  }
}
