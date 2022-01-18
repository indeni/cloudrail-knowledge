provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster1" {
  name               = "gke-cluster-001"
  location           = "us-west1-a"
  initial_node_count = 3
  workload_identity_config {
    workload_pool = "dev-for-tests.svc.id.goog"
  }
  node_config {
    workload_metadata_config {
      mode = "GKE_METADATA"
    }
  }
}

resource "google_container_cluster" "cluster2" {
  name               = "gke-cluster-002"
  location           = "us-west1-a"
  initial_node_count = 3
  workload_identity_config {
    workload_pool = "dev-for-tests.svc.id.goog"
  }  
  node_config {
    workload_metadata_config {
      mode = "GKE_METADATA"
    }
  }
}
