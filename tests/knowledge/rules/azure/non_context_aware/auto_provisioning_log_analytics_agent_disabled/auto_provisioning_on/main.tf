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
  resource_prefix = "cr2279"
  environment = "Tests"
}

resource "azurerm_security_center_auto_provisioning" "example" {
  auto_provision = "On"
}
