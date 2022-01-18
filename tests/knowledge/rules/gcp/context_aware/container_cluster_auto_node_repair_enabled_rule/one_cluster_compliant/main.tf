provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster5" {
  name               = "gke-cluster-005"
  location           = "us-west1-a"
  initial_node_count = 3
  release_channel {
    channel = "UNSPECIFIED"
  }
}

resource "google_container_cluster" "cluster6" {
  name               = "gke-cluster-006"
  location           = "us-west1-a"
  initial_node_count = 3
}

resource "google_container_node_pool" "cluster5_nodepool_1" {
  name       = "my-node-pool"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster5.name
  node_count = 1

  management {
    auto_repair = true
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "cluster5_nodepool_2" {
  name       = "my-node-pool-2"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster5.name
  node_count = 1

  management {
    auto_repair = false
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "cluster6_nodepool_1" {
  name       = "my-node-pool"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster6.name
  node_count = 1

  management {
    auto_repair = true
    auto_upgrade = true
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "cluster6_nodepool_2" {
  name       = "my-node-pool-2"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster6.name
  node_count = 1

  management {
    auto_repair = true
    auto_upgrade = true
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}
