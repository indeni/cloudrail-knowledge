data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                        = "cr2388-keyvault"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id

  sku_name = "standard"
}

resource "azurerm_resource_group" "rg" {
  name     = "example-resources"
  location = "West Europe"
}