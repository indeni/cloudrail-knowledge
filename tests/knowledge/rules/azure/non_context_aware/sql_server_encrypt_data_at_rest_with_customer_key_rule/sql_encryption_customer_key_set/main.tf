provider "azurerm" {
  features {}
}

locals {
  resource_prefix = "cr2523"
  tests_scope = "Tests"
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_mssql_server" "sql" {
  name                         = "${local.resource_prefix}-sqlserver"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "4dm1n157r470r"
  administrator_login_password = "4-v3ry-53cr37-p455w0rd"

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
  purge_protection_enabled    = false
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
  access_policy {
    tenant_id = azurerm_mssql_server.sql.identity[0].tenant_id
    object_id = azurerm_mssql_server.sql.identity[0].principal_id

    key_permissions = [
      "Get", "WrapKey", "UnwrapKey"
    ]
  }
}

resource "azurerm_key_vault_key" "key" {
  name         = "${local.resource_prefix}-sqlkey"
  key_vault_id = azurerm_key_vault.kv.id
  key_type     = "RSA"
  key_size     = 2048
  key_opts     = ["decrypt", "encrypt", "sign", "unwrapKey", "verify", "wrapKey"]
}

resource "azurerm_mssql_server_transparent_data_encryption" "example" {
  server_id        = azurerm_mssql_server.sql.id
  key_vault_key_id = azurerm_key_vault_key.key.id
}


resource "azurerm_mssql_database" "test" {
  name           = "${local.resource_prefix}-db"
  server_id      = azurerm_mssql_server.sql.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  license_type   = "LicenseIncluded"
  max_size_gb    = 1
  #read_scale     = true
  sku_name       = "Basic"
  zone_redundant = false
}
