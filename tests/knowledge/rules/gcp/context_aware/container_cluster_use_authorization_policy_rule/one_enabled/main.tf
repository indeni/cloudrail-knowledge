provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_binary_authorization_policy" "policy" {
  default_admission_rule {
    evaluation_mode = "ALWAYS_DENY"
    enforcement_mode = "ENFORCED_BLOCK_AND_AUDIT_LOG"
  }
}

resource "google_container_cluster" "cluster7" {
  name               = "gke-cluster-007"
  location           = "us-west1-a"
  initial_node_count = 3
  enable_binary_authorization = true
}

resource "google_container_cluster" "cluster8" {
  name               = "gke-cluster-008"
  location           = "us-west1-a"
  initial_node_count = 3
}
