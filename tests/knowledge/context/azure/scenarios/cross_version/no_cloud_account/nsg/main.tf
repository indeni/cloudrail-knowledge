resource "azurerm_resource_group" "rg" {
  name     = "temp-RG"
  location = "West Europe"
}

resource "azurerm_network_security_group" "nsg" {
  name                = "no-cloud-account-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}