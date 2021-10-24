from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.drift_detection.base_environment_context_drift_detector import BaseEnvironmentContextDriftDetector


class AzureEnvironmentContextDriftDetector(BaseEnvironmentContextDriftDetector):

    @classmethod
    def supported_drift_resource(cls, mergeable: Mergeable):
        pass
