

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

resource "azurerm_virtual_network" "example" {
  name                = "${local.test_name}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

resource "azurerm_subnet" "example" {
  name                 = "${local.test_name}-subnet"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_eventhub_namespace" "example" {
  name                 = "${local.test_name}-eventhubnam"
  location             = azurerm_resource_group.example.location
  resource_group_name  = azurerm_resource_group.example.name
  sku                  = "Standard"
  capacity             = 2
  auto_inflate_enabled = true
  maximum_throughput_units = 2
  zone_redundant           = false

  identity {
    type = "SystemAssigned"
  }

  network_rulesets {
    default_action                 = "Deny"
    trusted_service_access_enabled = true

    virtual_network_rule {
      subnet_id = azurerm_subnet.example.id
      ignore_missing_virtual_network_service_endpoint = true
    }

    ip_rule {
      ip_mask = "10.0.1.0/24"
      action  = "Allow"
    }
  }

  tags = {
    environment = "Production"
  }
}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name               = "${local.test_name}-diag"
  target_resource_id = azurerm_eventhub_namespace.example.id
  storage_account_id = azurerm_storage_account.example.id

  log {
    category = "ArchiveLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 31
    }
  }
  log {
    category = "OperationalLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 31
    }
  }
  log {
    category = "AutoScaleLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 31
    }
  }
  log {
    category = "KafkaCoordinatorLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 31
    }
  }
  log {
    category = "KafkaUserErrorLogs"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 31
    }
  }
  log {
    category = "EventHubVNetConnectionEvent"
    enabled  = true
    retention_policy {
      enabled = true
      days    = 31
    }
  }
  log {
    category = "CustomerManagedKeyUserLogs"
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
