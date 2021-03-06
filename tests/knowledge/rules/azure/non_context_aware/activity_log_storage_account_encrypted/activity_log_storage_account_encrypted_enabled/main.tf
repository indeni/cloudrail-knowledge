provider "azurerm" {
  features {  
  }
}

locals {
  resource_prefix = "cr24501"
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
  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_key_vault" "kv" {
  name                        = "${local.resource_prefix}-keyvault"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  #enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = true
  sku_name = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id
    key_permissions = [
      "Get", "List", "create", "delete", "recover",
    ]
    secret_permissions = [
      "Get", "List", "set",
    ]
    storage_permissions = [
      "Get",
    ]
  }
}

resource "azurerm_key_vault_access_policy" "storage" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_storage_account.storacc.identity.0.principal_id

  key_permissions    = ["get", "create", "list", "restore", "recover", "unwrapkey", "wrapkey", "encrypt", "decrypt", "sign", "verify"]
  secret_permissions = ["get"]
}


output "principal_id" {
  value = azurerm_storage_account.storacc.identity.0.principal_id
}

resource "azurerm_key_vault_key" "key" {
  name         = "${local.resource_prefix}-key"
  key_vault_id = azurerm_key_vault.kv.id
  key_type     = "RSA"
  key_size     = 2048
  key_opts     = ["decrypt", "encrypt", "sign", "unwrapKey", "verify", "wrapKey"]

  depends_on = [
    azurerm_key_vault_access_policy.storage,
  ]
}

resource "azurerm_storage_account_customer_managed_key" "example" {
  storage_account_id = azurerm_storage_account.storacc.id
  key_vault_id       = azurerm_key_vault.kv.id
  key_name           = azurerm_key_vault_key.key.name
}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "example"
  target_resource_id = azurerm_key_vault.kv.id
  storage_account_id = azurerm_storage_account.storacc.id

  log {
    category = "AuditEvent"
    enabled  = true
    retention_policy {
      enabled = true
      days = 31
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
