from typing import Optional, Dict, List
from dataclasses import dataclass
import dataclasses

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting


@dataclass
class LogicAppWorkflowAccessControlRules:
    """
        Attributes:
            allowed_caller_ip_address_range:  A list of the allowed caller IP address ranges.

    """
    allowed_caller_ip_address_range: List[str]


@dataclass
class LogicAppWorkflowAccessControl:
    """
        Attributes:
            actions: List of access control items to workflow actions.
            contents: List of access control items to workflow content.
            triggers: List of access control items to workflow triggers.
            workflow_management_list: List of access control items to workflow management.

    """
    actions: Optional[LogicAppWorkflowAccessControlRules]
    contents: Optional[LogicAppWorkflowAccessControlRules]
    triggers: Optional[LogicAppWorkflowAccessControlRules]
    workflow_management_list: Optional[LogicAppWorkflowAccessControlRules]


class AzureLogicAppWorkflow(AzureResource, IMonitorSettings):
    """
        Attributes:
            name: The name of the Logic App Workflow.
            access_control_config_list: The access control configuration to control access to this workflow.
            logic_app_integration_account_id: The ID of the integration account linked by this Logic App Workflow.
            enabled: If this Logic App Workflow is enabled or not.
            workflow_parameters: Specifies a map of Key-Value pairs of the Parameter Definitions to use for this Logic App Workflow.
            workflow_schema: Specifies the Schema to use for this Logic App Workflow.
            workflow_version: Specifies the version of the Schema used for this Logic App Workflow.
            parameters: A map of a Key-Value pair.
    """

    def __init__(self,
                 name: str,
                 access_control_config_list: List[LogicAppWorkflowAccessControl],
                 logic_app_integration_account_id: Optional[str],
                 enabled: bool,
                 workflow_schema: str,
                 workflow_version: str,
                 parameters: Dict[str, str] = None,
                 workflow_parameters: Dict[str, str] = None):
        super().__init__(AzureResourceType.AZURERM_LOGIC_APP_WORKFLOW)
        self.name: str = name
        self.access_control_config_list: Optional[List[LogicAppWorkflowAccessControl]] = access_control_config_list
        self.enabled: bool = enabled
        self.workflow_parameters: Dict[str, str] = workflow_parameters
        self.parameters: Dict[str, str] = parameters
        self.workflow_schema: str = workflow_schema
        self.workflow_version: str = workflow_version
        self.logic_app_integration_account_id: Optional[str] = logic_app_integration_account_id
        self.monitor_diagnostic_settings: List[AzureMonitorDiagnosticSetting] = []

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self._id}/logicApp'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Logic App Workflow' + ('s' if is_plural else '')

    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        return self.monitor_diagnostic_settings

    def to_drift_detection_object(self) -> dict:
        return {'access_control_config_list': [dataclasses.asdict(config) for config in self.access_control_config_list],
                'enabled': self.enabled,
                'workflow_parameters': self.workflow_parameters,
                'parameters': self.parameters,
                'logic_app_integration_account_id': self.logic_app_integration_account_id,
                'monitor_diagnostic_settings': [settings.to_drift_detection_object() for settings in self.monitor_diagnostic_settings]}
