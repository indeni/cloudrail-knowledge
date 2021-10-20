locals {
  resource_prefix = "crddtest"
  environment     = "Tests"
}

resource "azurerm_security_center_auto_provisioning" "example" {
  auto_provision = "On"
}
