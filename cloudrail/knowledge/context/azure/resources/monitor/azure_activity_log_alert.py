from typing import Optional, Dict, List
from enum import Enum
from dataclasses import dataclass
import dataclasses
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource


class MonitorActivityLogAlertCriteriaCategory(Enum):
    ADMINISTRATIVE = 'Administrative'
    AUTOSCALE = 'Autoscale'
    POLICY = 'Policy'
    RECOMMENDATION = 'Recommendation'
    RESOURCE_HEALTH = 'Resource_Health'
    SECURITY = 'Security'
    SERVICE_HEALTH = 'ServiceHealth'


class MonitorActivityLogAlertCriteriaLevel(Enum):
    VERBOSE = 'Verbose'
    INFORMATIONAL = 'Informational'
    WARNING = 'Warning'
    ERROR = 'Error'
    CRITICAL = 'Critical'


class MonitorActivityLogAlertCriteriaStatus(Enum):
    STARTED = 'Started'
    FAILED = 'Failed'
    SUCCEEDED = 'Succeeded'


class MonitorActivityLogAlertCriteriaRecommendationCategory(Enum):
    COST = 'Cost'
    RELIABILITY = 'Reliability'
    OPERATIONALEXCELLENCE = 'OperationalExcellence'
    PERFORMANCE = 'Performance'


class MonitorActivityLogAlertCriteriaRecommendationImpact(Enum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'


class MonitorActivityLogAlertCriteriaServiceHealthEvents(Enum):
    INCIDENT = 'Incident'
    MAINTENANCE = 'Maintenance'
    INFORMATIONAL = 'Informational'
    ACTION_REQUIRED = 'ActionRequired'
    SECURITY = 'Security'


@dataclass
class MonitorActivityLogAlertCriteriaServiceHealth:
    """
        Attributes:
        events: Events this alert will monitor.
        locations: Locations this alert will monitor.
        services: Services this alert will monitor.
    """
    events: Optional[List[MonitorActivityLogAlertCriteriaServiceHealthEvents]]
    locations: Optional[List[str]]
    services: Optional[List[str]]


@dataclass
class MonitorActivityLogAlertCriteria:
    """
        Attributes:
            category: The category of the operation.
            operation_name: The Resource Manager Role-Based Access Control operation name.
            resource_provider: The name of the resource provider monitored by the activity log alert.
            resource_type: The resource type monitored by the activity log alert.
            resource_group: The name of resource group monitored by the activity log alert.
            resource_id: The specific resource monitored by the activity log alert.
            caller: The email address or Azure Active Directory identifier of the user who performed the operation.
            level: The severity level of the event.
            status: The status of the event.
            sub_status: The sub status of the event.
            recommendation_type: The recommendation type of the event.
            recommendation_category: The recommendation category of the event.
            recommendation_impact: The recommendation impact of the event.
            service_health: A block to define fine grain service health settings.
    """
    category: MonitorActivityLogAlertCriteriaCategory
    operation_name: Optional[str]
    resource_provider: Optional[str]
    resource_type: Optional[str]
    resource_group: Optional[str]
    resource_id: Optional[str]
    caller: Optional[str]
    level: Optional[MonitorActivityLogAlertCriteriaLevel]
    status: Optional[MonitorActivityLogAlertCriteriaStatus]
    sub_status: Optional[str]
    recommendation_type: Optional[str]
    recommendation_category: Optional[MonitorActivityLogAlertCriteriaRecommendationCategory]
    recommendation_impact: Optional[MonitorActivityLogAlertCriteriaRecommendationImpact]
    service_health: Optional[MonitorActivityLogAlertCriteriaServiceHealth]


@dataclass
class MonitorActivityLogAlertAction:
    """
        Attributes:
            action_group_id: The ID of the Action Group.
            webhook_properties: The map of custom string properties to include with the post operation.
    """
    action_group_id: str
    webhook_properties: Dict[str, str] = None


class AzureMonitorActivityLogAlert(AzureResource):
    """
        Attributes:
            name: The name of the activity log aler.
            scopes: The Scope at which the Activity Log should be applied.
            criteria: The criteria parameters for this Activity Log Alert rule.
            actions: List of actions for this Log Alert rule.
            enabled: Whether or not this Activity Log Alert is enabled.
            description: The description of this activity log alert.
    """

    def __init__(self,
                 name: str,
                 scopes: List[str],
                 criteria: MonitorActivityLogAlertCriteria,
                 actions: Optional[List[MonitorActivityLogAlertAction]],
                 enabled: bool,
                 description: Optional[str]):
        super().__init__(AzureResourceType.AZURERM_MONITOR_ACTIVITY_LOG_ALERT)
        self.name: str = name
        self.scopes: List[str] = scopes
        self.enabled: bool = enabled
        self.description: Optional[str] = description
        self.criteria: MonitorActivityLogAlertCriteria = criteria
        self.actions: Optional[List[MonitorActivityLogAlertAction]] = actions

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self.get_id()}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Activity Log Alert' + ('s' if is_plural else '')

    def to_drift_detection_object(self) -> dict:
        return {"enabled": self.enabled,
                "tags": self.tags,
                "actions": [dataclasses.asdict(action) for action in self.actions],
                "scopes": self.scopes,
                "description": self.description,
                "criteria": dataclasses.asdict(self.criteria)
                }
