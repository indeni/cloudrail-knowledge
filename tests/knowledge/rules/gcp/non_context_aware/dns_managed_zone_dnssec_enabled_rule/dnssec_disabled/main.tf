provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "google_dns_managed_zone" "example-zone" {
  name        = "example-zone"
  dns_name    = "example-0000.com."
  description = "DNS Zone without DNSSEC"
}
