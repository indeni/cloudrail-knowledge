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
### Bucket IAM Policy ###
data "google_iam_policy" "admin" {
  binding {
    role = "roles/storage.admin"
    members = [
      "allAuthenticatedUsers"
    ]
  }
}

resource "google_storage_bucket_iam_policy" "policy" {
  bucket = google_storage_bucket.default.name
  policy_data = data.google_iam_policy.admin.policy_data
}
