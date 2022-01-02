
locals {
  resource_prefix = "cr3687"
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

resource "azurerm_search_service" "search" {
  name                          = "${local.resource_prefix}-search-service"
  resource_group_name           = azurerm_resource_group.rg.name
  location                      = azurerm_resource_group.rg.location
  sku                           = "standard"
  public_network_access_enabled = false
  partition_count               = 1
  replica_count                 = 1
  allowed_ips                   = ["8.8.8.8"]

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = "prod"
  }
}


resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "example"
  target_resource_id = azurerm_search_service.search.id
  storage_account_id = azurerm_storage_account.storacc.id

  log {
    category = "OperationLogs"
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
