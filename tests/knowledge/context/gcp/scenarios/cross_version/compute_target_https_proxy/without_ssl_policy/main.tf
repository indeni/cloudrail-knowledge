provider "google" {
  project     = "dev-for-tests"
  region      = "us-central-1"
}
resource "google_compute_target_https_proxy" "default" {
  name             = "test-proxy"
  url_map          = google_compute_url_map.default.id
  ssl_certificates = [google_compute_ssl_certificate.default.id]
}
resource "google_compute_ssl_certificate" "default" {
  name        = "my-certificate"
  private_key = file("../ssl_cert/privke.key")
  certificate = file("../ssl_cert/cert.crt")
}
resource "google_compute_url_map" "default" {
  name        = "url-map"
  default_service = google_compute_backend_service.default.id
  host_rule {
    hosts        = ["test.com"]
    path_matcher = "allpaths"
  }
  path_matcher {
    name            = "allpaths"
    default_service = google_compute_backend_service.default.id
    path_rule {
      paths   = ["/*"]
      service = google_compute_backend_service.default.id
    }
  }
}
resource "google_compute_backend_service" "default" {
  name        = "backend-service"
  port_name   = "http"
  protocol    = "HTTP"
  timeout_sec = 10
  health_checks = [google_compute_http_health_check.default.id]
}
resource "google_compute_http_health_check" "default" {
  name               = "http-health-check"
  request_path       = "/"
  check_interval_sec = 1
  timeout_sec        = 1
}