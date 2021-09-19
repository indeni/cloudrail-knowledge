locals {
  resource_prefix = "cr2152wa1"
  environment = "Tests"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_app_service_plan" "plan" {
  name                = "${local.resource_prefix}-service-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "webapp" {
  name = "${local.resource_prefix}-webapp"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  app_service_plan_id        = azurerm_app_service_plan.plan.id

  site_config {
    use_32_bit_worker_process = true
  }
  logs {
    http_logs {
      file_system {
        retention_in_days = 4
        retention_in_mb = 25
      }
    }
    detailed_error_messages_enabled = false
    failed_request_tracing_enabled = false
  }
}
