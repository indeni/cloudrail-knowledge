locals {
  resource_prefix = "cr2388"
  environment = "Tests"
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_storage_account" "storacc" {
  name                     = "${local.resource_prefix}tststacc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_key_vault" "kv" {
  name                        = "${local.resource_prefix}-keyvault"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "Get", "List", "create", "delete",
    ]

    secret_permissions = [
      "Get", "List", "set",
    ]

    storage_permissions = [
      "Get",
    ]
  }
}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "testing-keyvault"
  target_resource_id = azurerm_key_vault.kv.id
  storage_account_id = azurerm_storage_account.storacc.id

  metric {
    category = "AllMetrics"
    enabled = true
    retention_policy {
      enabled = false
    }
  }
}
