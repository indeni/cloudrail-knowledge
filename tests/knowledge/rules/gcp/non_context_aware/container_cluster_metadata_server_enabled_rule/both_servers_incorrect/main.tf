provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster3" {
  name               = "gke-cluster-003"
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

resource "google_container_cluster" "cluster4" {
  name               = "gke-cluster-004"
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
