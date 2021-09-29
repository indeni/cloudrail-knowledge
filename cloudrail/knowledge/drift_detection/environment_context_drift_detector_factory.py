from typing import Type

from cloudrail.knowledge.context.cloud_provider import CloudProvider

from cloudrail.knowledge.drift_detection.aws_environment_context_drift_detector import AwsEnvironmentContextDriftDetector
from cloudrail.knowledge.drift_detection.azure_environment_context_drift_detector import AzureEnvironmentContextDriftDetector
from cloudrail.knowledge.drift_detection.base_environment_context_drift_detector import BaseEnvironmentContextDriftDetector
from cloudrail.knowledge.drift_detection.gcp_environment_context_drift_detector import GcpEnvironmentContextDriftDetector
from cloudrail.knowledge.exceptions import UnsupportedCloudProviderException

class EnvironmentContextDriftDetectorFactory:

    @staticmethod
    def get(cloud_provider: CloudProvider) -> Type[BaseEnvironmentContextDriftDetector]:
        if cloud_provider == CloudProvider.AMAZON_WEB_SERVICES:
            return AwsEnvironmentContextDriftDetector
        if cloud_provider == CloudProvider.AZURE:
            return AzureEnvironmentContextDriftDetector
        if cloud_provider == CloudProvider.GCP:
            return GcpEnvironmentContextDriftDetector
        raise UnsupportedCloudProviderException(cloud_provider)
