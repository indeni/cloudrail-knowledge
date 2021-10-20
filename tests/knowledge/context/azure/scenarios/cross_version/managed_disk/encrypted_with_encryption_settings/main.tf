
locals {
  resource_prefix = "cr23371"
  environment = "Tests"
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_key_vault" "kv" {
  name                        = "${local.resource_prefix}-keyvault"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  enabled_for_disk_encryption = true
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
      "Get", "List", "set", "delete",
    ]

    storage_permissions = [
      "Get",
    ]
  }
}

resource "azurerm_key_vault_secret" "secret" {
  name         = "${local.resource_prefix}-secret"
  value        = "szecffvfvhuan"
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_managed_disk" "disk" {
  name                 = "${local.resource_prefix}-disk"
  location             = azurerm_resource_group.rg.location
  resource_group_name  = azurerm_resource_group.rg.name
  storage_account_type = "Standard_LRS"
  create_option        = "Empty"
  disk_size_gb         = "5"

  encryption_settings {
    enabled = true
    disk_encryption_key {
      secret_url = azurerm_key_vault_secret.secret.id
      source_vault_id = azurerm_key_vault.kv.id
    }
  }

}
