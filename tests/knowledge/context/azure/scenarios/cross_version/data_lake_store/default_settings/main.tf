
locals {
  test_name = "cr3682"
}
resource "azurerm_resource_group" "example" {
  name     = "${local.test_name}-rg"
  location = "West Europe"
}

resource "azurerm_storage_account" "example" {
  name                     = "${local.test_name}dlstacc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_data_lake_store" "datalake-store" {
  name                     = "${local.test_name}datalakesto"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location


  identity {
    type = "SystemAssigned"
  }

}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "${local.test_name}diag"
  target_resource_id = azurerm_data_lake_store.datalake-store.id
  storage_account_id = azurerm_storage_account.example.id

  log {
    category = "Audit"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 31
    }
  }

  log {
    category = "Requests"
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
