provider "google" {
  project     = "dev-for-tests"
  region      = "us-central-1"
}
### Bucket ###
resource "google_storage_bucket" "default" {
  name          = "dereban"
  location      = "US"
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
# ### Bucket IAM Member ###
resource "google_storage_bucket_iam_member" "member" {
  bucket = google_storage_bucket.default.name
  role = "roles/storage.admin"
  member = "user:maksym.d@indeni.com"

  condition {
    title       = "expires_after_2019_12_31"
    description = "Expiring at midnight of 2019-12-31"
    expression  = "request.time < timestamp(\"2020-01-01T00:00:00Z\")"
  }
}

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