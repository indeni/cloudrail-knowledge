provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster3" {
  name               = "gke-cluster-003"
  location           = "us-west1-a"
  initial_node_count = 3
  release_channel {
    channel = "UNSPECIFIED"
  }
}

resource "google_container_cluster" "cluster4" {
  name               = "gke-cluster-004"
  location           = "us-west1-a"
  initial_node_count = 3
  release_channel {
    channel = "UNSPECIFIED"
  }
}

resource "google_container_node_pool" "cluster3_nodepool_1" {
  name       = "my-node-pool"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster3.name
  node_count = 1

  management {
    auto_repair = false
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "cluster3_nodepool_2" {
  name       = "my-node-pool-2"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster3.name
  node_count = 1

  management {
    auto_repair = false
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "cluster4_nodepool_1" {
  name       = "my-node-pool"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster4.name
  node_count = 1

  management {
    auto_repair = false
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "cluster4_nodepool_2" {
  name       = "my-node-pool-2"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster4.name
  node_count = 1

  management {
    auto_repair = false
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}
