provider "google" {
  project     = "dev-for-tests"
  region      = "us-west1"
}

resource "tls_private_key" "test" {
  algorithm = "RSA"
}

resource "tls_self_signed_cert" "test" {
  key_algorithm   = "RSA"
  private_key_pem = tls_private_key.test.private_key_pem

  subject {
    common_name  = "example.com"
    organization = "ACME Examples, Inc"
  }

  validity_period_hours = 100

  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "server_auth",
  ]
}

resource "google_compute_ssl_certificate" "test" {
  name        = "my-certificate"
  private_key = tls_private_key.test.private_key_pem
  certificate = tls_self_signed_cert.test.cert_pem
}

resource "google_compute_backend_service" "test" {
  name        = "test-backend-service"
  protocol    = "SSL"
  timeout_sec = 10
}

resource "google_compute_ssl_policy" "test" {
  name            = "test-ssl-policy"
  profile         = "MODERN"
  min_tls_version = "TLS_1_0"
}

resource "google_compute_target_ssl_proxy" "test" {
  name             = "test-ssl-proxy"
  ssl_certificates = [google_compute_ssl_certificate.test.id]
  ssl_policy       = google_compute_ssl_policy.test.id
  backend_service  = google_compute_backend_service.test.id
}

resource "google_compute_global_forwarding_rule" "default" {
  name                  = "test-global-forwarding-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL"
  port_range            = "443"
  target                = google_compute_target_ssl_proxy.test.id
}
