variable "enable_oslogin" {
  type = map(string)
  default = {
      "server-1" = "TRUE"
      "server-2" = "FALSE"
  }
}
resource "google_compute_instance" "foo-instance" {
  for_each = var.enable_oslogin
  name         = "test${each.key}"
  machine_type = "f1-micro"
  zone         = "us-central1-a"
  metadata = {
    enable-oslogin = each.value
  }
    boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11-bullseye-v20210916"
    }
  }
  network_interface {
    subnetwork = "default"
  }
}