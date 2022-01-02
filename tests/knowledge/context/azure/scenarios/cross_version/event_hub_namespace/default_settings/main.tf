

locals {
  test_name = "cr3684"
}

resource "azurerm_resource_group" "example" {
  name     = "${local.test_name}-rg"
  location = "West Europe"
}

resource "azurerm_storage_account" "example" {
  name                     = "${local.test_name}dlstacc"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_eventhub_namespace" "example" {
  name                 = "${local.test_name}-eventhubnam"
  location             = azurerm_resource_group.example.location
  resource_group_name  = azurerm_resource_group.example.name
  sku                  = "Standard"
}
