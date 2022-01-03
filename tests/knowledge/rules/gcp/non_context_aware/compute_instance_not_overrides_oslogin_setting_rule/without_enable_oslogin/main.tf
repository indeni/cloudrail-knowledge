provider "google" {
  project     = "dev-for-tests"
  region = "us-central1"
}

variable "enable_oslogin" {
  type = map(string)
  default = {
      "server-3" = "dont use"
      "server-4" = "dont use"
  }
}
resource "google_compute_instance" "foo-instance" {
  for_each = var.enable_oslogin
  name         = each.key
  machine_type = "f1-micro"
  zone         = "us-central1-a"
    boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11-bullseye-v20210916"
    }
  }
  network_interface {
    subnetwork = "default"
  }
}