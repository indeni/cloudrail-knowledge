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

resource "azurerm_storage_account" "storacc" {
  name                     = "${local.resource_prefix}funapptstsa"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_app_service_plan" "svcplanconsumption" {
  name                = "${local.resource_prefix}-service-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  #kind                = "FunctionApp"
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

resource "azurerm_function_app" "functionapp" {
  name = "${local.resource_prefix}-functionapp"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  app_service_plan_id        = azurerm_app_service_plan.svcplanconsumption.id
  storage_account_name       = azurerm_storage_account.storacc.name
  storage_account_access_key = azurerm_storage_account.storacc.primary_access_key
  version                    = "~3"
  os_type                    = "linux"

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
  }

  site_config {
    linux_fx_version = "Python|3.9"
  }
}
