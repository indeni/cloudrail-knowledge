import json
from typing import Optional
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.logic_app.azure_logic_app_workflow import AzureLogicAppWorkflow, \
    LogicAppWorkflowAccessControl, LogicAppWorkflowAccessControlRules

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class LogicAppWorkflowBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureLogicAppWorkflow:
        ## Access control config
        access_control_config_list = []
        for config in self._get_known_value(attributes, 'access_control', []):
            actions = self._get_access_control_rule(config, 'action')
            contents = self._get_access_control_rule(config, 'content')
            triggers = self._get_access_control_rule(config, 'trigger')
            workflow_management_list = self._get_access_control_rule(config, 'workflow_management')
            access_control_config_list.append(LogicAppWorkflowAccessControl(actions=actions,
                                                                            contents=contents,
                                                                            triggers=triggers,
                                                                            workflow_management_list=workflow_management_list))
        workflow_parameters = None
        if workflow_parameters_data := self._get_known_value(attributes, 'workflow_parameters'):
            for parameter in workflow_parameters_data:
                workflow_parameters_data[parameter] = json.loads(workflow_parameters_data[parameter])
            workflow_parameters = workflow_parameters_data
        parameters = None
        if parameters_data := self._get_known_value(attributes, 'parameters'):
            for parameter in parameters_data:
                if parameters_data[parameter] == 'true':
                    parameters_data[parameter] = True
                if parameters_data[parameter] == 'false':
                    parameters_data[parameter] = False
            parameters = parameters_data
        return AzureLogicAppWorkflow(name=attributes['name'],
                                     access_control_config_list=access_control_config_list,
                                     logic_app_integration_account_id=self._get_known_value(attributes, 'logic_app_integration_account_id'),
                                     enabled=self._get_known_value(attributes, 'enabled', True),
                                     workflow_schema=self._get_known_value(attributes, 'workflow_schema',
                                                                           'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#'),
                                     workflow_version=self._get_known_value(attributes, 'workflow_version', '1.0.0.0'),
                                     parameters=parameters,
                                     workflow_parameters=workflow_parameters)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_LOGIC_APP_WORKFLOW

    @classmethod
    def _get_access_control_rule(cls, data: dict, key: str) -> Optional[LogicAppWorkflowAccessControlRules]:
        if access_control_rule_data := cls._get_known_value(data, key):
            return LogicAppWorkflowAccessControlRules(allowed_caller_ip_address_range=cls._get_known_value(access_control_rule_data[0],
                                                                                                           'allowed_caller_ip_address_range'))
        return None
