provider "azurerm" {
  features {}
}

locals {
  resource_prefix = "cr2315"
  environment = "Tests"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_storage_account" "storacc" {
  name                     = "${local.resource_prefix}batchstacc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_batch_account" "example" {
  name                 = "${local.resource_prefix}batch"
  resource_group_name  = azurerm_resource_group.rg.name
  location             = azurerm_resource_group.rg.location
  pool_allocation_mode = "BatchService"
  storage_account_id   = azurerm_storage_account.storacc.id
}


resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "example"
  target_resource_id = azurerm_batch_account.example.id
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