terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
}

provider "azurerm" {
  features {}
}

locals {
  resource_prefix = "cr2282"
  environment = "Tests"
}

resource "azurerm_security_center_subscription_pricing" "example" {
  tier          = "Standard"
  resource_type = "SqlServers"
}
