resource "google_compute_network" "new-network" {
  project     = "dev-for-tests"
  name                    = "new-network"
  auto_create_subnetworks = true
  routing_mode            = "GLOBAL"
  delete_default_routes_on_create = true
  mtu                     = 1460
}
