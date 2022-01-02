provider "google" {
  project     = "dev-for-tests"
  region      = "us-central-1"
}
### Bucket ###
resource "google_storage_bucket" "default" {
  name          = "dereban"
  location      = "EU"
  force_destroy = true

  uniform_bucket_level_access = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }
  cors {
    origin          = ["http://indeni.com"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}
### Bucket IAM Binding ###
resource "google_storage_bucket_iam_binding" "binding" {
  bucket = google_storage_bucket.default.name
  role = "roles/storage.admin"
  members = [
    "user:maksym.d@indeni.com",
  ]

  condition {
    title       = "expires_after_2021_12_31"
    description = "Expiring at midnight of 2021-12-31"
    expression  = "request.time < timestamp(\"2020-01-01T00:00:00Z\")"
  }
}