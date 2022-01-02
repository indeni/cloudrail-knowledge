provider "google" {
  project     = "dev-for-tests"
  region      = "us-central-1"
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
resource "google_compute_target_https_proxy" "https_proxy" {
  name             = "test-proxy"
  url_map          = google_compute_url_map.url_map.id
  ssl_certificates = [google_compute_ssl_certificate.ssl_certificate.id]
  ssl_policy = google_compute_ssl_policy.ssl_policy.name
}
resource "google_compute_ssl_policy" "ssl_policy" {
  name    = "ssl-policy"
  profile = "MODERN"
}
resource "google_compute_ssl_certificate" "ssl_certificate" {
  name        = "my-certificate"
  private_key = tls_private_key.test.private_key_pem
  certificate = tls_self_signed_cert.test.cert_pem
}
resource "google_compute_url_map" "url_map" {
  name        = "url-map"
  default_service = google_compute_backend_service.backend_service.id
  host_rule {
    hosts        = ["test.com"]
    path_matcher = "allpaths"
  }
  path_matcher {
    name            = "allpaths"
    default_service = google_compute_backend_service.backend_service.id
    path_rule {
      paths   = ["/*"]
      service = google_compute_backend_service.backend_service.id
    }
  }
}
resource "google_compute_backend_service" "backend_service" {
  name        = "backend-service"
  port_name   = "http"
  protocol    = "HTTP"
  timeout_sec = 10
  health_checks = [google_compute_http_health_check.health_check.id]
}
resource "google_compute_http_health_check" "health_check" {
  name               = "http-health-check"
  request_path       = "/"
  check_interval_sec = 1
  timeout_sec        = 1
}