provider "azurerm" {
  features {}
}

locals {
  resource_prefix = "cr2429"
  tests_scope = "Tests"
}

data "azurerm_subscription" "current" {
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.resource_prefix}-RG"
  location = "West Europe"
}

resource "azurerm_monitor_action_group" "action-gr" {
  name                = "example-actiongroup"
  resource_group_name = azurerm_resource_group.rg.name
  short_name          = "p0action"

  webhook_receiver {
    name        = "callmyapi"
    service_uri = "http://example.com/alert"
  }
}

resource "azurerm_monitor_activity_log_alert" "log-alert1" {
  name                = "${local.resource_prefix}-activitylogalert1"
  resource_group_name = azurerm_resource_group.rg.name
  scopes              = [data.azurerm_subscription.current.id]
  description         = "log alert rule"

  criteria {
    operation_name = "Microsoft.Network/networkSecurityGroups/write"
    category       = "Administrative"
  }

  action {
    action_group_id = azurerm_monitor_action_group.action-gr.id
  }
}

resource "azurerm_monitor_activity_log_alert" "log-alert2" {
  name                = "${local.resource_prefix}-activitylogalert2"
  resource_group_name = azurerm_resource_group.rg.name
  scopes              = [data.azurerm_subscription.current.id]
  description         = "log alert rule"

  criteria {
    operation_name = "Microsoft.ClassicNetwork/networkSecurityGroups/write"
    category       = "Administrative"
  }

  action {
    action_group_id = azurerm_monitor_action_group.action-gr.id
  }
}

resource "azurerm_monitor_activity_log_alert" "log-alert3" {
  name                = "${local.resource_prefix}-activitylogalert3"
  resource_group_name = azurerm_resource_group.rg.name
  scopes              = [data.azurerm_subscription.current.id]
  description         = "log alert rule"

  criteria {
    operation_name = "Microsoft.Network/networkSecurityGroups/delete"
    category       = "Administrative"
  }

  action {
    action_group_id = azurerm_monitor_action_group.action-gr.id
  }
}

resource "azurerm_monitor_activity_log_alert" "log-alert4" {
  name                = "${local.resource_prefix}-activitylogalert4"
  resource_group_name = azurerm_resource_group.rg.name
  scopes              = [data.azurerm_subscription.current.id]
  description         = "log alert rule"

  criteria {
    operation_name = "Microsoft.ClassicNetwork/networkSecurityGroups/delete"
    category       = "Administrative"
  }

  action {
    action_group_id = azurerm_monitor_action_group.action-gr.id
  }
}