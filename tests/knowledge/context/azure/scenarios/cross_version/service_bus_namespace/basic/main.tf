
locals {
  resource_prefix = "cr3688"
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

resource "azurerm_servicebus_namespace" "example" {
  name                = "${local.resource_prefix}-servicebus-namespace"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Basic"
  capacity            = 0
  zone_redundant      = false

  tags = {
    environment = "production"
  }
}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "example"
  target_resource_id = azurerm_servicebus_namespace.example.id
  storage_account_id = azurerm_storage_account.storacc.id

  log {
    category = "OperationalLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 31
    }
  }
  log {
    category = "VNetAndIPFilteringLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 31
    }
  }
  metric {
    category = "AllMetrics"
    enabled  = false
    retention_policy {
      enabled = false
    }
  }
}
