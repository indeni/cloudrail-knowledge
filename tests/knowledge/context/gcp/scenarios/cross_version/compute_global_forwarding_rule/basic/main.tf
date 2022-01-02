
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
  port_name   = "http"
  protocol    = "HTTP"
  timeout_sec = 10
}

resource "google_compute_url_map" "test" {
  name            = "test-url-map"
  description     = "a description"
  default_service = google_compute_backend_service.test.id
}

resource "google_compute_ssl_policy" "test" {
  name            = "test-ssl-policy"
  profile         = "MODERN"
  min_tls_version = "TLS_1_2"
}

resource "google_compute_target_https_proxy" "test" {
  name             = "test-proxy"
  url_map          = google_compute_url_map.test.id
  ssl_certificates = [google_compute_ssl_certificate.test.id]
  ssl_policy       = google_compute_ssl_policy.test.id
}

resource "google_compute_global_forwarding_rule" "https-forwarding" {
  name                  = "test-global-https-forwarding-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL"
  port_range            = "443"
  target                = google_compute_target_https_proxy.test.id
}

resource "google_compute_backend_service" "test-ssl" {
  name        = "test-ssl-backend-service"
  protocol    = "SSL"
  timeout_sec = 10
}

resource "google_compute_target_ssl_proxy" "test" {
  name             = "test-ssl-proxy"
  ssl_certificates = [google_compute_ssl_certificate.test.id]
  ssl_policy       = google_compute_ssl_policy.test.id
  backend_service  = google_compute_backend_service.test-ssl.id
}

resource "google_compute_global_forwarding_rule" "ssl-forwarding" {
  name                  = "test-global-ssl-forwarding-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL"
  port_range            = "443"
  target                = google_compute_target_ssl_proxy.test.id
}
