resource "google_storage_default_object_access_control" "bucket_access_rule" {
  bucket = google_storage_bucket.bucket.name
  role   = "READER"
  entity = "allUsers"
}

resource "google_storage_bucket" "bucket" {
  name     = "example-bucket"
  location = "US"
}
