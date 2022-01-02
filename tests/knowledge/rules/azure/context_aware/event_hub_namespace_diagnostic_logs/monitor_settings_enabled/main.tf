
locals {
  resource_prefix = "cr2386"
  environment = "Tests"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_storage_account" "storacc" {
  name                     = "${local.resource_prefix}hubstacc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_eventhub_namespace" "example" {
  name                = "${local.resource_prefix}eventhubnamespace"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Basic"
  capacity            = 1

}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "example"
  target_resource_id = azurerm_eventhub_namespace.example.id
  storage_account_id = azurerm_storage_account.storacc.id

  log {
    category = "ArchiveLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days = 0
    }
  }
  log {
    category = "OperationalLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days = 0
    }
  }
  log {
    category = "AutoScaleLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days = 0
    }
  }
  log {
    category = "KafkaCoordinatorLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days = 0
    }
  }
  log {
    category = "KafkaUserErrorLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days = 0
    }
  }
  log {
    category = "EventHubVNetConnectionEvent"
    enabled  = true
    retention_policy {
      enabled = true
      days = 0
    }
  }
  log {
    category = "CustomerManagedKeyUserLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days = 0
    }
  }

  metric {
    category = "AllMetrics"
    enabled = true
    retention_policy {
      enabled = true
      days = 0
    }
  }
}
