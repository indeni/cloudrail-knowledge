
resource "google_dns_managed_zone" "test" {
  name        = "test-zone"
  dns_name    = "testing.example.com."
  description = "Example DNS managed zone for cloudrail"
  project     = "dev-for-tests"

  dnssec_config {
    state         = "on"
    non_existence = "nsec3"

    default_key_specs {
      algorithm  = "rsasha256"
      key_length = 2048
      key_type   = "zoneSigning"
    }

    default_key_specs {
      algorithm  = "rsasha512"
      key_length = 2048
      key_type   = "keySigning"
    }
  }
}
