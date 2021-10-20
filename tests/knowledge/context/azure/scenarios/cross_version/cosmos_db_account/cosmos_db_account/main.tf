locals {
  name = "crtest"
}

data "azurerm_subscription" "primary" {
}

data "azurerm_client_config" "current" {}

data "azuread_service_principal" "cosmosdb" {
  display_name = "Azure Cosmos DB"
}

resource "azurerm_role_assignment" "storage" {
  scope                = data.azurerm_subscription.primary.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.name}-rg"
  location = "West Europe"
}

resource "random_integer" "ri" {
  min = 10000
  max = 99999
}

resource "azurerm_key_vault" "test" {
  name                       = "${local.name}-kv-${random_integer.ri.result}"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = true
  sku_name                   = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id
    key_permissions = [
      "list",
      "create",
      "delete",
      "get",
      "purge",
      "update",
    ]
    secret_permissions = [
      "get",
      "delete",
      "set",
    ]
  }

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azuread_service_principal.cosmosdb.id

    key_permissions = [
      "list",
      "create",
      "delete",
      "get",
      "update",
      "unwrapKey",
      "wrapKey",
    ]
    secret_permissions = [
      "get",
      "delete",
      "set",
    ]
  }
}

resource "azurerm_key_vault_key" "generated" {
  name         = "${local.name}-key"
  key_vault_id = azurerm_key_vault.test.id
  key_type     = "RSA"
  key_size     = 2048

  key_opts = [
    "decrypt",
    "encrypt",
    "sign",
    "unwrapKey",
    "verify",
    "wrapKey",
  ]
}


resource "azurerm_virtual_network" "test" {
  name                = "${local.name}-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
  dns_servers         = ["10.0.0.4", "10.0.0.5"]

  subnet {
    name           = "subnet1"
    address_prefix = "10.0.1.0/24"
  }

  subnet {
    name           = "subnet2"
    address_prefix = "10.0.2.0/24"
  }

}

resource "azurerm_storage_account" "file" {
  name                     = "${local.name}storagfile"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_kind             = "StorageV2"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_data_lake_gen2_filesystem" "test" {
  name               = "${local.name}file"
  storage_account_id = azurerm_storage_account.file.id
  depends_on = [
    azurerm_role_assignment.storage
  ]
}

resource "azurerm_synapse_workspace" "test" {
  name                                 = "${local.name}-work"
  resource_group_name                  = azurerm_resource_group.rg.name
  location                             = azurerm_resource_group.rg.location
  storage_data_lake_gen2_filesystem_id = azurerm_storage_data_lake_gen2_filesystem.test.id
  sql_administrator_login              = "sqladminuser"
  sql_administrator_login_password     = "H@Sh1CoR3!"
}

resource "azurerm_cosmosdb_account" "db" {
  name                                  = "${local.name}-cosmosdb-${random_integer.ri.result}"
  location                              = azurerm_resource_group.rg.location
  resource_group_name                   = azurerm_resource_group.rg.name
  offer_type                            = "Standard"
  kind                                  = "MongoDB"
  enable_automatic_failover             = true
  enable_free_tier                      = true
  analytical_storage_enabled            = false
  is_virtual_network_filter_enabled     = true
  public_network_access_enabled         = false
  ip_range_filter                       = "8.8.8.8"
  key_vault_key_id                      = azurerm_key_vault_key.generated.versionless_id
  mongo_server_version                  = "4.0"
  network_acl_bypass_for_azure_services = true
  enable_multiple_write_locations       = false
  access_key_metadata_writes_enabled    = true
  local_authentication_disabled         = false
  network_acl_bypass_ids                = [azurerm_synapse_workspace.test.id]

  virtual_network_rule {
    id                                   = element(tolist(azurerm_virtual_network.test.subnet.*.id), 0)
    ignore_missing_vnet_service_endpoint = true
  }

  virtual_network_rule {
    id                                   = element(tolist(azurerm_virtual_network.test.subnet.*.id), 1)
    ignore_missing_vnet_service_endpoint = true
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 400
    max_staleness_prefix    = 200000
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }

  geo_location {
    location          = "France Central"
    failover_priority = 1
  }

  capabilities {
    name = "EnableMongo"
  }

  backup {
    type                = "Periodic"
    interval_in_minutes = 1440
    retention_in_hours  = 8
  }

  cors_rule {
    allowed_headers    = ["exampleHeader"]
    allowed_methods    = ["GET", "HEAD"]
    allowed_origins    = ["https://example.com"]
    exposed_headers    = ["exampleHeader"]
    max_age_in_seconds = 3600
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    "env" = "test"
  }
}


resource "azurerm_storage_account" "test" {
  name                     = "storageacc${random_integer.ri.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_monitor_diagnostic_setting" "diag1" {
  name               = "${local.name}-cosmosdbaccdiag"
  target_resource_id = azurerm_cosmosdb_account.db.id
  storage_account_id = azurerm_storage_account.test.id

  log {
    enabled  = true
    category = "DataPlaneRequests"

    retention_policy {
      enabled = true
      days    = 0
    }
  }
}
