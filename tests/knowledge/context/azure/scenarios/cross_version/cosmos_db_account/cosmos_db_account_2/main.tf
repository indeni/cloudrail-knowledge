
resource "azurerm_resource_group" "rg" {
  name     = "cloudrailtest2-rg"
  location = "West Europe"
}

resource "random_integer" "ri" {
  min = 10000
  max = 99999
}

resource "azurerm_cosmosdb_account" "db" {
  name                          = "cloudrail-test-cosmos-db-${random_integer.ri.result}"
  location                      = azurerm_resource_group.rg.location
  resource_group_name           = azurerm_resource_group.rg.name
  offer_type                    = "Standard"
  kind                          = "GlobalDocumentDB"
  enable_automatic_failover     = true
  public_network_access_enabled = true

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 400
    max_staleness_prefix    = 200000
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }

  geo_location {
    location          = "France Central"
    failover_priority = 1
  }
}

resource "azurerm_cosmosdb_account" "db2" {
  name                          = "cloudrail-test-cosmos-db2-${random_integer.ri.result}"
  location                      = azurerm_resource_group.rg.location
  resource_group_name           = azurerm_resource_group.rg.name
  offer_type                    = "Standard"
  kind                          = "GlobalDocumentDB"
  enable_automatic_failover     = true
  public_network_access_enabled = true

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 400
    max_staleness_prefix    = 200000
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }

  geo_location {
    location          = "France Central"
    failover_priority = 1
  }
}