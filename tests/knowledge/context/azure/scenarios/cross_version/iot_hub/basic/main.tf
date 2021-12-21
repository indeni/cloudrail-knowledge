
locals {
  resource_prefix = "cr3685"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "eastus"
}

resource "azurerm_storage_account" "storacc" {
  name                     = "${local.resource_prefix}tststacc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "example" {
  name                  = "examplecontainer"
  storage_account_name  = azurerm_storage_account.storacc.name
  container_access_type = "private"
}

resource "azurerm_iothub" "iothub" {
  name                = "${local.resource_prefix}-IoTHub"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  sku {
    name     = "S1"
    capacity = "1"
  }

  event_hub_partition_count   = 2
  event_hub_retention_in_days = 1

  endpoint {
    type                       = "AzureIotHub.StorageContainer"
    connection_string          = azurerm_storage_account.storacc.primary_blob_connection_string
    name                       = "export"
    batch_frequency_in_seconds = 60
    max_chunk_size_in_bytes    = 10485760
    container_name             = azurerm_storage_container.example.name
    encoding                   = "Avro"
    file_name_format           = "{iothub}/{partition}_{YYYY}_{MM}_{DD}_{HH}_{mm}"
    resource_group_name        = azurerm_resource_group.rg.name
  }

  fallback_route {
    source         = "DeviceMessages"
    condition      = "true"
    endpoint_names = ["export"]
    enabled        = true
  }

  file_upload {
    connection_string  = azurerm_storage_account.storacc.primary_blob_connection_string
    container_name     = azurerm_storage_container.example.name
    sas_ttl            = "PT1H"
    notifications      = false
    lock_duration      = "PT1M"
    default_ttl        = "PT1H"
    max_delivery_count = 10
  }

  ip_filter_rule {
    name    = "sample"
    ip_mask = "10.0.10.0/24"
    action  = "Accept"
  }

  route {
    name           = "export"
    source         = "DeviceMessages"
    condition      = "true"
    endpoint_names = ["export"]
    enabled        = true
  }

  enrichment {
    key            = "tenant"
    value          = "$twin.tags.Tenant"
    endpoint_names = ["export"]
  }

  public_network_access_enabled = false
  min_tls_version               = "1.2"

  tags = {
    environment = "Production"
  }

}

data "azurerm_monitor_diagnostic_categories" "main" {
  count       = local.enabled ? 1 : 0
  resource_id = azurerm_iothub.iothub.id
}
variable "log_categories" {
  type        = list(string)
  default     = null
  description = "List of log categories."
}

locals {
  logs_destinations_ids = "id"
  enabled               = length(local.logs_destinations_ids) > 0
  log_categories = (
    var.log_categories != null ?
    var.log_categories :
    try(data.azurerm_monitor_diagnostic_categories.main.0.logs, [])
  )
  logs = {
    for category in local.log_categories : category => {
      enabled        = true
      retention_days = 31
    }
  }
}


resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "example"
  target_resource_id = azurerm_iothub.iothub.id
  storage_account_id = azurerm_storage_account.storacc.id

  dynamic "log" {
    for_each = local.logs

    content {
      category = log.key
      enabled  = true

      retention_policy {
        enabled = true
        days    = 31
      }
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
