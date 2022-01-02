
locals {
  resource_prefix = "cr3689a"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_storage_account" "storacc" {
  name                     = "${local.resource_prefix}storacc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_stream_analytics_job" "job" {
  name                = "${local.resource_prefix}-stream-job"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  compatibility_level                      = "1.1"
  data_locale                              = "en-GB"
  events_late_arrival_max_delay_in_seconds = 60
  events_out_of_order_max_delay_in_seconds = 50
  events_out_of_order_policy               = "Adjust"

  identity {
    type = "SystemAssigned"
  }

  output_error_policy = "Drop"
  streaming_units     = 3

  transformation_query = <<-QUERY
    SELECT *
    INTO [YourOutputAlias]
    FROM [YourInputAlias]
  QUERY

}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "example"
  target_resource_id = azurerm_stream_analytics_job.job.id
  storage_account_id = azurerm_storage_account.storacc.id

  log {
    category = "Execution"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 31
    }
  }
  log {
    category = "Authoring"
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
