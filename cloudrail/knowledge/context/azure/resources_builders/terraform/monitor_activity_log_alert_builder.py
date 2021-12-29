from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.monitor.azure_activity_log_alert import AzureMonitorActivityLogAlert, MonitorActivityLogAlertAction, MonitorActivityLogAlertCriteria, \
    MonitorActivityLogAlertCriteriaCategory, MonitorActivityLogAlertCriteriaLevel, MonitorActivityLogAlertCriteriaStatus, MonitorActivityLogAlertCriteriaRecommendationCategory, \
    MonitorActivityLogAlertCriteriaRecommendationImpact, MonitorActivityLogAlertCriteriaServiceHealth, MonitorActivityLogAlertCriteriaServiceHealthEvents

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import is_valid_enum_value, enum_implementation


class MonitorActivityLogAlertBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureMonitorActivityLogAlert:
        name = attributes['name']
        scopes = attributes['scopes']
        criteria = self.build_criteria(attributes)
        actions = self.build_actions(attributes)
        enabled = attributes.get('enabled', True)
        description = attributes.get('description')

        return AzureMonitorActivityLogAlert(name, scopes, criteria, actions, enabled, description)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_MONITOR_ACTIVITY_LOG_ALERT

    def build_criteria(self, attributes: dict) -> MonitorActivityLogAlertCriteria:
        criteria_dict = attributes['criteria'][0]
        category = enum_implementation(MonitorActivityLogAlertCriteriaCategory, criteria_dict['category'])
        operation_name = self._get_known_value(criteria_dict, 'operation_name')
        resource_provider = self._get_known_value(criteria_dict, 'resource_provider')
        resource_type = self._get_known_value(criteria_dict, 'resource_type')
        resource_group = self._get_known_value(criteria_dict, 'resource_group')
        resource_id = criteria_dict.get('resource_id')
        caller = self._get_known_value(criteria_dict, 'caller')
        level_value = self._get_known_value(criteria_dict, 'level')
        level = enum_implementation(MonitorActivityLogAlertCriteriaLevel, level_value) if level_value else None
        status_value = self._get_known_value(criteria_dict, 'status')
        status = enum_implementation(MonitorActivityLogAlertCriteriaStatus, status_value) if status_value else None
        sub_status = self._get_known_value(criteria_dict, 'sub_status')
        recommendation_type = self._get_known_value(criteria_dict, 'recommendation_type')
        rec_category_value = self._get_known_value(criteria_dict, 'recommendation_category')
        recommendation_category = enum_implementation(MonitorActivityLogAlertCriteriaRecommendationCategory, rec_category_value) if rec_category_value else None
        rec_impact_value = self._get_known_value(criteria_dict, 'recommendation_impact')
        recommendation_impact = enum_implementation(MonitorActivityLogAlertCriteriaRecommendationImpact, rec_impact_value) if rec_impact_value else None
        service_health = self.build_service_health(criteria_dict)

        return MonitorActivityLogAlertCriteria(category, operation_name, resource_provider, resource_type, resource_group, resource_id, caller, level, status, sub_status,
                                               recommendation_type, recommendation_category, recommendation_impact, service_health)

    def build_service_health(self, criteria_dict: dict) -> Optional[MonitorActivityLogAlertCriteriaServiceHealth]:
        if service_health_block := self._get_known_value(criteria_dict, 'service_health'):
            service_health_dict = service_health_block[0]
            events = [MonitorActivityLogAlertCriteriaServiceHealthEvents(value) for key, values in service_health_dict.items() for value in values
                      if key == 'events' and is_valid_enum_value(MonitorActivityLogAlertCriteriaServiceHealthEvents, value)]
            locations = self._get_known_value(service_health_dict, 'locations')
            services = self._get_known_value(service_health_dict, 'services')

            return MonitorActivityLogAlertCriteriaServiceHealth(events, locations, services)

        return None

    def build_actions(self, attributes: dict) -> Optional[List[MonitorActivityLogAlertAction]]:
        actions_list = []
        if action_block := self._get_known_value(attributes, 'action'):
            for action in action_block:
                action_group_id = action.get('action_group_id')
                webhook_properties = self._get_known_value(action, 'webhook_properties')
                actions_list.append(MonitorActivityLogAlertAction(action_group_id, webhook_properties))

            return actions_list

        return None
