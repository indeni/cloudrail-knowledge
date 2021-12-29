provider "google" {
    region = "eu-central2"
}

resource "google_storage_bucket" "test-bucket" {
  name          = "test-bucket-3767"
  location      = "EU"
}