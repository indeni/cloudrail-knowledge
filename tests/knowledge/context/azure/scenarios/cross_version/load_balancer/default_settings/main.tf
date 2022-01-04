locals {
  name = "cr3763"
}

resource "azurerm_resource_group" "test" {
  name     = "${local.name}-rg"
  location = "West Europe"
}

resource "azurerm_lb" "load_balancer" {
  name                = "${local.name}-lbGateway"
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name
}
