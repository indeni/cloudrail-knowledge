from typing import Optional

from cloudrail.knowledge.context.azure.resources.monitor.azure_activity_log_alert import AzureMonitorActivityLogAlert, MonitorActivityLogAlertCriteria, MonitorActivityLogAlertCriteriaCategory, \
    MonitorActivityLogAlertCriteriaLevel, MonitorActivityLogAlertCriteriaStatus, MonitorActivityLogAlertCriteriaRecommendationCategory, MonitorActivityLogAlertCriteriaRecommendationImpact, \
    MonitorActivityLogAlertCriteriaServiceHealthEvents, MonitorActivityLogAlertCriteriaServiceHealth, MonitorActivityLogAlertAction

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import is_valid_enum_value


class MonitorActivityLogAlertBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'activity-log-alert-rules-list.json'

    def do_build(self, attributes: dict) -> AzureMonitorActivityLogAlert:
        properties = attributes['properties']

        name = attributes["name"]
        scopes = properties['scopes']
        criteria = self.build_criteria(properties)
        action = self.build_action(properties)
        enabled = properties.get('enabled')
        description = properties.get('description')

        return AzureMonitorActivityLogAlert(name, scopes, criteria, action, enabled, description)

    def build_criteria(self, properties: dict) -> MonitorActivityLogAlertCriteria:
        criteria_list = properties.get('condition').get('allOf')
        criteria_dict = {criteria['field']: {'equals': criteria['equals'], 'containsAny': criteria['containsAny']} for criteria in criteria_list if 'field' in criteria}
        any_of_dict = self.build_any_of_block(criteria_list)
        category = self.assignee_enum(MonitorActivityLogAlertCriteriaCategory, criteria_dict['category']['equals'])
        operation_name = criteria_dict.get('operationName', {}).get('equals')
        resource_provider = criteria_dict.get('resourceProvider', {}).get('equals')
        resource_type = criteria_dict.get('resourceType', {}).get('equals')
        resource_group = criteria_dict.get('resourceGroup', {}).get('equals')
        resource_id = criteria_dict.get('resourceId', {}).get('equals')
        caller = criteria_dict.get('caller', {}).get('equals')
        level_value = criteria_dict.get('level', {}).get('equals')
        level = self.assignee_enum(MonitorActivityLogAlertCriteriaLevel, level_value) if level_value else None
        status_value = criteria_dict.get('status', {}).get('equals')
        status = self.assignee_enum(MonitorActivityLogAlertCriteriaStatus, status_value) if status_value else None
        sub_status = criteria_dict.get('subStatus', {}).get('equals')
        recommendation_type = criteria_dict.get('properties.recommendationType', {}).get('equals')
        rec_category_value = criteria_dict.get('properties.recommendationCategory', {}).get('equals')
        recommendation_category = self.assignee_enum(MonitorActivityLogAlertCriteriaRecommendationCategory, rec_category_value) if rec_category_value else None
        rec_impact_value = criteria_dict.get('properties.recommendationImpact', {}).get('equals')
        recommendation_impact = self.assignee_enum(MonitorActivityLogAlertCriteriaRecommendationImpact, rec_impact_value) if rec_impact_value else None
        service_health = self.build_service_health(criteria_dict, any_of_dict)

        return MonitorActivityLogAlertCriteria(category, operation_name, resource_provider, resource_type, resource_group, resource_id, caller, level, status, sub_status,
                                               recommendation_type, recommendation_category, recommendation_impact, service_health)

    @staticmethod
    def build_service_health(criteria_dict: dict, any_of_dict: dict) -> Optional[MonitorActivityLogAlertCriteriaServiceHealth]:
        events = [MonitorActivityLogAlertCriteriaServiceHealthEvents(value) for key, value_list in any_of_dict.items() for value in value_list
                  if key == 'properties.incidentType' and is_valid_enum_value(MonitorActivityLogAlertCriteriaServiceHealthEvents, value)]
        locations = criteria_dict.get('properties.impactedServices[*].ImpactedRegions[*].RegionName', {}).get('containsAny')
        services = criteria_dict.get('properties.impactedServices[*].ServiceName', {}).get('containsAny')

        if events or locations or services:
            return MonitorActivityLogAlertCriteriaServiceHealth(events, locations, services)

        return None

    @staticmethod
    def build_action(properties: dict) -> Optional[MonitorActivityLogAlertAction]:
        if action_block := properties.get('actions').get('actionGroups'):
            action_dict = action_block[0]
            action_group_id = action_dict.get('actionGroupId')
            webhook_properties = action_dict.get('webhookProperties')
            return MonitorActivityLogAlertAction(action_group_id, webhook_properties)

        return None

    @staticmethod
    def build_any_of_block(criteria_list: dict) -> dict:
        any_of_dict = dict()
        for block in criteria_list:
            for any_of in block.get('anyOf', []):
                field_name = any_of['field']
                value = any_of['equals']
                if field_name in any_of_dict.keys():
                    any_of_dict[field_name].append(value)
                else:
                    any_of_dict[field_name] = [value]

        return any_of_dict

    @staticmethod
    def assignee_enum(enum_meta_class, value):
        return enum_meta_class(value) if is_valid_enum_value(enum_meta_class, value) else None
