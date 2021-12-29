
locals {
  name = "cloudrailtest"
}

data "azurerm_client_config" "current" {}

data "azurerm_subscription" "primary" {}

data "azuread_service_principal" "mab" {
  display_name = "Microsoft Azure Batch"
}

resource "azurerm_resource_group" "test" {
  name     = "${local.name}-rg"
  location = "West Europe"
}

resource "azurerm_storage_account" "test" {
  name                     = "${local.name}storageacc"
  resource_group_name      = azurerm_resource_group.test.name
  location                 = azurerm_resource_group.test.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_key_vault" "test" {
  name                            = "${local.name}keyvault"
  location                        = azurerm_resource_group.test.location
  resource_group_name             = azurerm_resource_group.test.name
  enabled_for_disk_encryption     = true
  enabled_for_deployment          = true
  enabled_for_template_deployment = true
  tenant_id                       = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days      = 7
  purge_protection_enabled        = false
  sku_name                        = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azuread_service_principal.mab.object_id

    secret_permissions = [
      "get",
      "list",
      "set",
      "delete",
      "recover"
    ]
  }
}

resource "azurerm_batch_account" "test" {
  name                          = "${local.name}batchacc"
  resource_group_name           = azurerm_resource_group.test.name
  location                      = azurerm_resource_group.test.location
  pool_allocation_mode          = "UserSubscription"
  public_network_access_enabled = false
  storage_account_id            = azurerm_storage_account.test.id

  key_vault_reference {
    id  = azurerm_key_vault.test.id
    url = azurerm_key_vault.test.vault_uri
  }

  tags = {
    env = "test"
  }

  depends_on = [
    azurerm_role_assignment.contributor
  ]
}

resource "azurerm_role_assignment" "contributor" {
  scope                = data.azurerm_subscription.primary.id
  principal_id         = data.azuread_service_principal.mab.object_id
  role_definition_name = "Contributor"
}

resource "azurerm_monitor_diagnostic_setting" "diag1" {
  name               = "batchaccdiag"
  target_resource_id = azurerm_batch_account.test.id
  storage_account_id = azurerm_storage_account.test.id

  log {
    enabled  = true
    category = "ServiceLog"

    retention_policy {
      enabled = true
      days    = 0
    }
  }
}
