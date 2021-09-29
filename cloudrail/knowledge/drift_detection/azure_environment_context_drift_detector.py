from typing import Set

from cloudrail.knowledge.drift_detection.base_environment_context_drift_detector import BaseEnvironmentContextDriftDetector


class AzureEnvironmentContextDriftDetector(BaseEnvironmentContextDriftDetector):

    @classmethod
    def get_excluded_attributes(cls) -> Set[str]:
        return {'is_managed_by_iac',
                'cloud_resource_url',
                'origin',
                'is_pseudo',
                'tenant_id',
                'subscription_id',
                'property_type',
                'is_invalidated',
                'is_tagable',
                'iac_state',
                'friendly_name',
                'tf_resource_type',
                'raw_data',
                'inbound_connections',
                'outbound_connections',
                'invalidation',
                'location',
                'resource_group_name'}
