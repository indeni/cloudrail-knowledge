from typing import Optional
from cloudrail.knowledge.context.azure.resources.logic_app.azure_logic_app_workflow import AzureLogicAppWorkflow, \
    LogicAppWorkflowAccessControl, LogicAppWorkflowAccessControlRules
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.utils import is_iterable_with_values


class LogicAppWorkflowBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return  'list-logic-app-workflows.json'

    def do_build(self, attributes: dict) -> AzureLogicAppWorkflow:
        properties = attributes['properties']
        ## Access control config
        access_control_config_list = []
        actions = self._get_access_control_rule(properties.get('accessControl', {}), 'actions')
        contents = self._get_access_control_rule(properties.get('accessControl', {}), 'contents')
        triggers = self._get_access_control_rule(properties.get('accessControl', {}), 'triggers')
        workflow_management_list = self._get_access_control_rule(properties.get('accessControl', {}), 'workflowManagement')
        access_control_config_list.append(LogicAppWorkflowAccessControl(actions=actions,
                                                                        contents=contents,
                                                                        triggers=triggers,
                                                                        workflow_management_list=workflow_management_list))
        access_control_config_list = access_control_config_list if is_iterable_with_values(access_control_config_list) else []
        workflow_definitions = properties.get('definition', {})
        workflow_schema = workflow_definitions.get('$schema')
        workflow_version = workflow_definitions.get('contentVersion')
        workflow_parameters = workflow_definitions.get('parameters')
        parameters = properties.get('parameters')
        for parameter in parameters:
            parameters[parameter] = parameters[parameter]['value']
        return AzureLogicAppWorkflow(name=attributes['name'],
                                     access_control_config_list=access_control_config_list,
                                     logic_app_integration_account_id=properties.get('integrationAccount', {}).get('id'),
                                     enabled=properties.get('state') == 'Enabled',
                                     workflow_schema=workflow_schema if is_iterable_with_values(workflow_schema) else None,
                                     workflow_version=workflow_version if is_iterable_with_values(workflow_version) else None,
                                     parameters=parameters if is_iterable_with_values(parameters) else None,
                                     workflow_parameters=workflow_parameters if is_iterable_with_values(workflow_parameters) else None)

    @staticmethod
    def _get_access_control_rule(data: dict, key: str) -> Optional[LogicAppWorkflowAccessControlRules]:
        if data.get(key):
            return LogicAppWorkflowAccessControlRules([rule['addressRange'] for rule in data[key]['allowedCallerIpAddresses']])
        return None
