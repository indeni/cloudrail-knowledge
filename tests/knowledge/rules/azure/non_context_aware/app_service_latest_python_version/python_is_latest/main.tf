provider "azurerm" {
  subscription_id = "230613d8-3b34-4790-b650-36f31045f19a"
  features {}
}

locals {
  resource_prefix = "cr2152py39"
  environment = "Tests"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_app_service_plan" "svcplanconsumption" {
  name                = "${local.resource_prefix}-service-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

resource "azurerm_app_service" "my-service-app" {
  name = "${local.resource_prefix}-serviceapp"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  app_service_plan_id        = azurerm_app_service_plan.svcplanconsumption.id

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
  }

  site_config {
    linux_fx_version = "Python|3.9"
  }
}
