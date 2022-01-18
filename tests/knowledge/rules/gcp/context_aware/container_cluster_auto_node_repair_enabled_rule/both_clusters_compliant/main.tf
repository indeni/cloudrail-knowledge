provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_container_cluster" "cluster1" {
  name               = "gke-cluster-001"
  location           = "us-west1-a"
  initial_node_count = 3
  release_channel {
    channel = "UNSPECIFIED"
  }
}

resource "google_container_cluster" "cluster2" {
  name               = "gke-cluster-002"
  location           = "us-west1-a"
  initial_node_count = 3
  release_channel {
    channel = "UNSPECIFIED"
  }
}

resource "google_container_node_pool" "cluster1_nodepool_1" {
  name       = "my-node-pool"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster1.name
  node_count = 1

  management {
    auto_repair = true
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "cluster1_nodepool_2" {
  name       = "my-node-pool-2"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster1.name
  node_count = 1

  management {
    auto_repair = true
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "cluster2_nodepool_1" {
  name       = "my-node-pool"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster2.name
  node_count = 1

  management {
    auto_repair = true
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}

resource "google_container_node_pool" "cluster2_nodepool_2" {
  name       = "my-node-pool-2"
  location   = "us-west1-a"
  cluster    = google_container_cluster.cluster2.name
  node_count = 1

  management {
    auto_repair = true
  }

  node_config {
    preemptible  = true
    machine_type = "e2-small"
  }
}
