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

resource "google_compute_target_ssl_proxy" "default" {
  name             = "test-proxy"
  backend_service  = google_compute_backend_service.default.id
  ssl_certificates = [google_compute_ssl_certificate.default.id]
}

resource "google_compute_ssl_policy" "ssl_policy" {
  name    = "ssl-policy"
  profile = "MODERN"
  # self_link
}

resource "google_compute_ssl_certificate" "default" {
  name        = "default-cert"
  private_key = tls_private_key.test.private_key_pem
  certificate = tls_self_signed_cert.test.cert_pem
}

resource "google_compute_backend_service" "default" {
  name          = "backend-service"
  protocol      = "SSL"
  health_checks = [google_compute_health_check.default.id]
}

resource "google_compute_health_check" "default" {
  name               = "health-check"
  check_interval_sec = 1
  timeout_sec        = 1
  tcp_health_check {
    port = "443"
  }
}
