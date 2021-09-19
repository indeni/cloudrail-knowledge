locals {
  resource_prefix = "cr2304aks"
  environment = "Tests"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "${local.resource_prefix}-aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "exampleaks1"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2S"
    os_disk_size_gb = 40
  }

  role_based_access_control {
    enabled = false
  }

  identity {
    type = "SystemAssigned"
  }

}
