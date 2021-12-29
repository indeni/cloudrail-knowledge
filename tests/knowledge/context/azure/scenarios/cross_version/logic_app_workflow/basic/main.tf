
locals {
  resource_prefix = "cr3686"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_storage_account" "storacc" {
  name                     = "${local.resource_prefix}batchstacc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_virtual_network" "example" {
  name                = "${local.resource_prefix}-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/22"]
}

resource "azurerm_subnet" "isesubnet1" {
  name                 = "${local.resource_prefix}-subnet1"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.1.0/26"]

  delegation {
    name = "integrationServiceEnvironments"
    service_delegation {
      name = "Microsoft.Logic/integrationServiceEnvironments"
    }
  }
}

resource "azurerm_subnet" "isesubnet2" {
  name                 = "${local.resource_prefix}-subnet2"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.1.64/26"]
}

resource "azurerm_subnet" "isesubnet3" {
  name                 = "${local.resource_prefix}-subnet3"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.1.128/26"]
}

resource "azurerm_subnet" "isesubnet4" {
  name                 = "${local.resource_prefix}-subnet4"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.1.192/26"]
}

# Uncomment this if you need to test this resource reference

# resource "azurerm_integration_service_environment" "example" {
#   name                 = "${local.resource_prefix}-ise"
#   location             = azurerm_resource_group.rg.location
#   resource_group_name  = azurerm_resource_group.rg.name
#   sku_name             = "Developer_0"
#   access_endpoint_type = "Internal"

#   virtual_network_subnet_ids = [
#     azurerm_subnet.isesubnet1.id,
#     azurerm_subnet.isesubnet2.id,
#     azurerm_subnet.isesubnet3.id,
#     azurerm_subnet.isesubnet4.id
#   ]
# }

resource "azurerm_logic_app_integration_account" "example" {
  name                = "${local.resource_prefix}-ia"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku_name            = "Standard"
}

resource "azurerm_logic_app_workflow" "workflow" {
  name                = "${local.resource_prefix}-workflow"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  access_control {
    action {
      allowed_caller_ip_address_range = ["10.10.0.2/32"]
    }

    content {
      allowed_caller_ip_address_range = ["10.10.0.2/32"]
    }

    trigger {
      allowed_caller_ip_address_range = ["10.10.0.2/32"]
    }

    workflow_management {
      allowed_caller_ip_address_range = ["10.10.0.2/32"]
    }
  }

  # Uncomment this if you need to test this resource reference

  #integration_service_environment_id = azurerm_integration_service_environment.example.id

  logic_app_integration_account_id = azurerm_logic_app_integration_account.example.id
  enabled                          = true
  workflow_parameters = {
    b = jsonencode({
      type = "Bool"
    })
  }

  workflow_schema  = "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#"
  workflow_version = "1.0.0.0"

  parameters = {
    b = "true"
  }

  tags = {
    "environment" = "prod"
  }

}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "example"
  target_resource_id = azurerm_logic_app_workflow.workflow.id
  storage_account_id = azurerm_storage_account.storacc.id

  log {
    category = "WorkflowRuntime"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 31
    }
  }

  metric {
    category = "AllMetrics"
    enabled  = false
    retention_policy {
      enabled = false
    }
  }
}
