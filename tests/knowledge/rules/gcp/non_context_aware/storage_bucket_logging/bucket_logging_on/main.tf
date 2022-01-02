provider "google" {
  project     = "dev-tomer"
  region      = "us-west1"
}

resource "google_storage_bucket" "log-bucket-example" {
  name          = "log-bucket-example"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  logging {
    log_bucket = "my-log-bucket"
  }
}