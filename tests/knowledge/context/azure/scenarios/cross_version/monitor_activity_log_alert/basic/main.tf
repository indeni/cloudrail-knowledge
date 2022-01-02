locals {
  resource_prefix = "cr3690"
}

data "azurerm_subscription" "current" {
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_network_security_group" "nsg" {
  name                = "${local.resource_prefix}-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}


resource "azurerm_monitor_action_group" "test" {
  name                = "example-actiongroup"
  resource_group_name = azurerm_resource_group.rg.name
  short_name          = "p0action"

  webhook_receiver {
    name        = "callmyapi"
    service_uri = "http://example.com/alert"
  }
}

resource "azurerm_monitor_action_group" "test10" {
  name                = "doron_test"
  resource_group_name = azurerm_resource_group.rg.name
  short_name          = "dfghjk"

  webhook_receiver {
    name        = "callmyapi"
    service_uri = "http://example.com/alert"
  }
}

resource "azurerm_monitor_activity_log_alert" "test1" {
  name                = "${local.resource_prefix}-activitylogalert1"
  resource_group_name = azurerm_resource_group.rg.name
  scopes              = [data.azurerm_subscription.current.id]
  enabled             = true
  description         = "log alert rule"


  criteria {
    category                = "Administrative"
    operation_name          = "Microsoft.Network/networkSecurityGroups/write"
    resource_provider       = "Microsoft.Network"
    resource_type           = "networkSecurityGroups"
    resource_group          = "fakename"
    resource_id             = azurerm_network_security_group.nsg.id
    caller                  = "fake@emailaddress.com"
    level                   = "Warning"
    status                  = "doron"
    sub_status              = "Failed"
    recommendation_category = "OperationalExcellence"
    recommendation_impact   = "High"
  }

  action {
    action_group_id = azurerm_monitor_action_group.test.id

    webhook_properties = {
      "key" = "value"
    }
  }

  action {
    action_group_id = azurerm_monitor_action_group.test10.id

    webhook_properties = {
      "key" = "value"
    }
  }

  tags = {
    "environment" = "production"
  }
}

resource "azurerm_monitor_activity_log_alert" "test2" {
  name                = "${local.resource_prefix}-activitylogalert2"
  resource_group_name = azurerm_resource_group.rg.name
  scopes              = [data.azurerm_subscription.current.id]
  enabled             = true
  description         = "log alert rule"


  criteria {
    category            = "ServiceHealth"
    resource_group      = "fakename"
    resource_id         = azurerm_network_security_group.nsg.id
    level               = "Warning"
    recommendation_type = "fakeRecommendation"

    service_health {
      events    = ["Incident", "Maintenance"]
      locations = ["Global"]
      services  = ["All Services"]
    }

  }

  tags = {
    "environment" = "production"
  }
}
