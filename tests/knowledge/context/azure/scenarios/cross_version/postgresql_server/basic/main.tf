locals {
  resource_prefix = "cr3692"
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_storage_account" "test" {
  name                     = "${local.resource_prefix}stgacc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}

resource "azurerm_postgresql_server" "test1" {
  name                         = "${local.resource_prefix}-postgresql-server"
  location                     = azurerm_resource_group.rg.location
  resource_group_name          = azurerm_resource_group.rg.name
  sku_name                     = "GP_Gen5_2"
  version                      = "11"
  administrator_login          = "psqladminun"
  administrator_login_password = "H@Sh1CoR3!"
  auto_grow_enabled            = true
  backup_retention_days        = 7
  create_mode                  = "Default"
  geo_redundant_backup_enabled = false

  identity {
    type = "SystemAssigned"
  }

  infrastructure_encryption_enabled = false
  public_network_access_enabled     = true
  ssl_enforcement_enabled           = true
  ssl_minimal_tls_version_enforced  = "TLS1_2"
  storage_mb                        = 5120

  threat_detection_policy {
    enabled                    = false
    disabled_alerts            = ["Access_Anomaly"]
    email_account_admins       = false
    email_addresses            = ["admin@fake.com"]
    retention_days             = 1
    storage_account_access_key = azurerm_storage_account.test.primary_access_key
    storage_endpoint           = azurerm_storage_account.test.primary_blob_endpoint
  }

  tags = {
    "environment" = "production"
  }

}

resource "null_resource" "restore_time" {
  depends_on = [
    azurerm_postgresql_server.test1,
    azurerm_postgresql_configuration.test1
  ]

  provisioner "local-exec" {
    command = "az postgres server show --name ${local.resource_prefix}-postgresql-server --resource-group ${local.resource_prefix}-RG | jq -r '.earliestRestoreDate' > ${path.module}/restore_time.txt"
  }
}

# Needed to avoid Internal Server Errors when configuring the azurerm_postgresql_configuration right after the postgresql server is created.
resource "time_sleep" "wait_2_min" {
  depends_on = [
    azurerm_postgresql_server.test1
  ]

  create_duration = "2m"
}

resource "azurerm_postgresql_configuration" "test1" {
  depends_on = [
    time_sleep.wait_2_min
  ]

  name                = "connection_throttling"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_postgresql_server.test1.name
  value               = "on"
}


data "local_file" "restore_time" {
  filename   = "${path.module}/restore_time.txt"
  depends_on = [null_resource.restore_time]
}

resource "time_sleep" "wait_10_min" {
  depends_on = [
    azurerm_postgresql_server.test1,
    azurerm_postgresql_configuration.test1
  ]

  create_duration = "15m"
}

resource "azurerm_postgresql_server" "test2" {
  depends_on = [
    null_resource.restore_time,
    time_sleep.wait_10_min,
    azurerm_postgresql_configuration.test1
  ]

  name                              = "${local.resource_prefix}-postgresql-server2"
  location                          = azurerm_resource_group.rg.location
  resource_group_name               = azurerm_resource_group.rg.name
  sku_name                          = "GP_Gen5_2"
  version                           = "11"
  auto_grow_enabled                 = true
  create_mode                       = "PointInTimeRestore"
  creation_source_server_id         = azurerm_postgresql_server.test1.id
  infrastructure_encryption_enabled = false
  public_network_access_enabled     = true
  restore_point_in_time             = chomp(data.local_file.restore_time.content)
  ssl_enforcement_enabled           = true
  ssl_minimal_tls_version_enforced  = "TLS1_2"
}

resource "azurerm_postgresql_configuration" "test2" {
  name                = "connection_throttling"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_postgresql_server.test2.name
  value               = "on"
}
