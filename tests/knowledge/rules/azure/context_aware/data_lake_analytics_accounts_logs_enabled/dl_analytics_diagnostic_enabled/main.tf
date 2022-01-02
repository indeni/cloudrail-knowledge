provider "azurerm" {
  features {}
}

locals {
  resource_prefix = "cr2373"
  environment = "Tests"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_storage_account" "storacc" {
  name                     = "${local.resource_prefix}dlstacc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_data_lake_store" "dls" {
  name                = "${local.resource_prefix}datalakestore"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

}

resource "azurerm_data_lake_analytics_account" "dla" {
  name                = "${local.resource_prefix}datalakeanalytics"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  default_store_account_name = azurerm_data_lake_store.dls.name
}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "example"
  target_resource_id = azurerm_data_lake_analytics_account.dla.id
  storage_account_id = azurerm_storage_account.storacc.id

  log {
    category = "AuditEvent"
    enabled  = true
    retention_policy {
      enabled = true
      days = 400
    }
  }
  metric {
    category = "AllMetrics"
    enabled = false
    retention_policy {
      enabled = false
    }
  }
}
