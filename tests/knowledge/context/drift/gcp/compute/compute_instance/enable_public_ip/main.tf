provider "google" {
  region      = "us-central1"
}

resource "google_compute_instance" "drift_resource" {
   name = "drift-name"
   machine_type = "n1-standard-1"
   zone = "us-central1-a"
   boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

    network_interface {
    network = "default"
  }

}
output "name_vm" {
    value = google_compute_instance.drift_resource.name
}
