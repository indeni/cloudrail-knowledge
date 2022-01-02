
resource "google_dns_managed_zone" "example-zone" {
  name        = "example-zone-04"
  dns_name    = "example-01235.com."
  description = "DNS Zone with RSASHA256"
  project     = "dev-for-tests"

  dnssec_config {
    default_key_specs {
      algorithm = "rsasha256"
      key_length = 2048
      key_type = "zoneSigning"
      kind = "dnsKeySpec"
    }
    default_key_specs {
      algorithm = "rsasha256"
      key_length = 2048
      key_type = "keySigning"
      kind = "dnsKeySpec"
    }
    kind = "managedZoneDnsSecConfig"
    non_existence = "nsec"
    state = "on"
  }
}

