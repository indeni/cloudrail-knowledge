
locals {
  resource_prefix = "cr2523"
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_user_assigned_identity" "sql" {
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  name                = "${local.resource_prefix}-userid"
}

resource "azurerm_mssql_server" "sql" {
  depends_on = [

  ]
  name                         = "${local.resource_prefix}-sqlserver"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "4dm1n157r470r"
  administrator_login_password = "4-v3ry-53cr37-p455w0rd"

  azuread_administrator {
    login_username              = "sqladmin"
    object_id                   = data.azurerm_client_config.current.object_id
    tenant_id                   = data.azurerm_client_config.current.tenant_id
    azuread_authentication_only = false
  }

  connection_policy = "Default"

  identity {
    type = "UserAssigned"
    user_assigned_identity_ids = [
      azurerm_user_assigned_identity.sql.id
    ]
  }

  minimum_tls_version               = "1.1"
  public_network_access_enabled     = false
  primary_user_assigned_identity_id = azurerm_user_assigned_identity.sql.id

  tags = {
    "environment" = "production"
  }
}

resource "azurerm_key_vault" "kv" {
  depends_on = [
    azurerm_mssql_server.sql
  ]

  name                = "${local.resource_prefix}-keyvault"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  #enabled_for_disk_encryption = true
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  sku_name                   = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id
    key_permissions = [
      "Get", "List", "create", "delete", "recover", "purge"
    ]
    secret_permissions = [
      "Get", "List", "set",
    ]
    storage_permissions = [
      "Get",
    ]
  }
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = azurerm_user_assigned_identity.sql.principal_id

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

resource "azurerm_storage_account" "example" {
  name                     = "${local.resource_prefix}tststoracc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "example" {
  name                  = "${local.resource_prefix}container"
  storage_account_name  = azurerm_storage_account.example.name
  container_access_type = "private"
}

resource "azurerm_mssql_server_security_alert_policy" "example" {
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_mssql_server.sql.name
  state               = "Enabled"
}

resource "azurerm_mssql_server_vulnerability_assessment" "example" {
  server_security_alert_policy_id = azurerm_mssql_server_security_alert_policy.example.id
  storage_container_path          = "${azurerm_storage_account.example.primary_blob_endpoint}${azurerm_storage_container.example.name}/"
  storage_account_access_key      = azurerm_storage_account.example.primary_access_key

  recurring_scans {
    enabled                   = true
    email_subscription_admins = true
    emails = [
      "email@example1.com",
      "email@example2.com"
    ]
  }
}
