resource "google_compute_ssl_policy" "example_ssl" {
  name            = "example-ssl-policy"
  min_tls_version = "TLS_1_0"
  profile         = "COMPATIBLE"
}
