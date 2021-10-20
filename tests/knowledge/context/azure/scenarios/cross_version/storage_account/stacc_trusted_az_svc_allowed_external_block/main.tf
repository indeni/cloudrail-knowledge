
locals {
  resource_prefix = "cr2496"
  environment = "Tests"
}

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

resource "azurerm_storage_account_network_rules" "test" {
  resource_group_name  = azurerm_resource_group.rg.name
  storage_account_name = azurerm_storage_account.storacc.name

  default_action             = "Deny"
  ip_rules                   = ["1.2.3.4"]
  bypass                     = ["AzureServices"]
}
