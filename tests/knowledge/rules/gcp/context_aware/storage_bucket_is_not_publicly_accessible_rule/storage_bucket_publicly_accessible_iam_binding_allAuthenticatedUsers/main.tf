provider "google" {
  project     = "dev-for-tests"
  region      = "us-central-1"
}

resource "google_storage_bucket" "test-bucket" {
  name          = "test-bucket-jjfhz7854"
  location      = "EU"
  force_destroy = true
}

resource "google_storage_bucket_iam_binding" "binding" {
  bucket = google_storage_bucket.test-bucket.name
  role   = "roles/storage.admin"
  members = [
    "allAuthenticatedUsers",
  ]
}
