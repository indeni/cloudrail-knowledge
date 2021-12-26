from typing import Optional, List
from enum import Enum
from dataclasses import dataclass

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting


class StreamAnalyticsJobCompatibilityLevel(str, Enum):
    LEVEL_1_0 = '1.0'
    LEVEL_1_1 = '1.1'
    LEVEL_1_2 = '1.2'


class StreamAnalyticsJobEventsPolicy(str, Enum):
    ADJUST = 'Adjust'
    DROP = 'Drop'


class StreamAnalyticsJobIdentityType(str, Enum):
    SYSTEM_ASSIGNED = 'SystemAssigned'


class StreamAnalyticsJobOutputErrorPolicy(str, Enum):
    STOP = 'Stop'
    DROP = 'Drop'


@dataclass
class StreamAnalyticsJobIdentity:
    """
        Attributes:
            type: The type of identity used for the Stream Analytics Job.
    """
    type: StreamAnalyticsJobIdentityType


class AzureStreamAnalyticsJob(AzureResource, IMonitorSettings):
    """
        Attributes:
            name: The name of the Stream Analytics Job.
            stream_analytics_cluster_id: The ID of an existing Stream Analytics Cluster where the Stream Analytics Job should run.
            compatibility_level: Specifies the compatibility level for this job - which controls certain runtime behaviours of the streaming job.
            data_locale: Specifies the Data Locale of the Job.
            events_late_arrival_max_delay_in_seconds: Specifies the maximum tolerable delay in seconds where events arriving late could be included.
            events_out_of_order_max_delay_in_seconds: Specifies the maximum tolerable delay in seconds where out-of-order events can be adjusted to be back in order.
            events_out_of_order_policy: Specifies the policy which should be applied to events which arrive out of order in the input event stream.
            identity: The identity used for the Stream Analytics Job.
            output_error_policy: Specifies the policy which should be applied to events which arrive at the output
            and cannot be written to the external storage due to being malformed (such as missing column values, column values of wrong type or size).
            streaming_units: Specifies the number of streaming units that the streaming job uses.
            transformation_query: Specifies the query that will be run in the streaming job.
    """

    def __init__(self,
                 name: str,
                 compatibility_level: StreamAnalyticsJobCompatibilityLevel,
                 data_locale: str,
                 events_late_arrival_max_delay_in_seconds: int,
                 events_out_of_order_max_delay_in_seconds: int,
                 events_out_of_order_policy: StreamAnalyticsJobEventsPolicy,
                 identity: StreamAnalyticsJobIdentity,
                 output_error_policy: StreamAnalyticsJobOutputErrorPolicy,
                 stream_units: int,
                 transformation_query: str):
        super().__init__(AzureResourceType.AZURERM_STREAM_ANALYTICS_JOB)
        self.name: str = name
        self.compatibility_level: StreamAnalyticsJobCompatibilityLevel = compatibility_level
        self.data_locale: str = data_locale
        self.events_late_arrival_max_delay_in_seconds: int = events_late_arrival_max_delay_in_seconds
        self.events_out_of_order_max_delay_in_seconds: int = events_out_of_order_max_delay_in_seconds
        self.events_out_of_order_policy: StreamAnalyticsJobEventsPolicy = events_out_of_order_policy
        self.identity: StreamAnalyticsJobIdentity = identity
        self.output_error_policy: StreamAnalyticsJobOutputErrorPolicy = output_error_policy
        self.stream_units: int = stream_units
        self.transformation_query: str = transformation_query
        self.monitor_diagnostic_settings: List[AzureMonitorDiagnosticSetting] = []

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource{self._id}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        return 'Stream Analytics Job' + ('s' if is_plural else '')

    def get_monitor_settings(self) -> List[AzureMonitorDiagnosticSetting]:
        return self.monitor_diagnostic_settings

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags,
                'compatibility_level': self.compatibility_level,
                'data_locale': self.data_locale,
                'events_late_arrival_max_delay_in_seconds': self.events_late_arrival_max_delay_in_seconds,
                'events_out_of_order_max_delay_in_seconds': self.events_out_of_order_max_delay_in_seconds,
                'identity': self.identity,
                'output_error_policy': self.output_error_policy,
                'stream_units': self.stream_units,
                'transformation_query': self.transformation_query,
                'monitor_diagnostic_settings': [settings.to_drift_detection_object() for settings in self.monitor_diagnostic_settings]}
