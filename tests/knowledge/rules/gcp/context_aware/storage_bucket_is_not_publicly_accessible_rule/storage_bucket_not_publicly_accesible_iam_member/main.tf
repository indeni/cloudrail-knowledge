provider "google" {
  project     = "dev-for-tests"
  region      = "us-central-1"
}

resource "google_service_account" "custom" {
  account_id   = "customserviceaccountid"
  display_name = "My Custom Service Account"
}

resource "google_storage_bucket" "test-bucket" {
  name          = "test-bucket-jjfhz7854"
  location      = "EU"
  force_destroy = true
}

resource "google_storage_bucket_iam_member" "member" {
  bucket = google_storage_bucket.test-bucket.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.custom.email}"
}
