locals {
  resource_prefix = "cr2282"
  environment = "Tests"
}

resource "azurerm_security_center_subscription_pricing" "example" {
  tier          = "Free"
  resource_type = "ContainerRegistry"
}
