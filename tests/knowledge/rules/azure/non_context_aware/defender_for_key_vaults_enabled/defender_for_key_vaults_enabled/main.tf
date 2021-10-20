provider "azurerm" {
  subscription_id = "230613d8-3b34-4790-b650-36f31045f19a"
  features {}
}

locals {
  resource_prefix = "cr2465"
  environment = "Tests"
}

resource "azurerm_security_center_subscription_pricing" "example" {
  tier          = "Standard"
  resource_type = "KeyVaults"
}
