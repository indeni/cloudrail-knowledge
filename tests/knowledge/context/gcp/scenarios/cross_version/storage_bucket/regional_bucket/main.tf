provider "google" {
    region = "US-WEST1"
}

resource "google_storage_bucket" "test-bucket" {
  name          = "test-bucket-3777"
  location      = "US-WEST1"
  storage_class = "REGIONAL"
  uniform_bucket_level_access = true
}