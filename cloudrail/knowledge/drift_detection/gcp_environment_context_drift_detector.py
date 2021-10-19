from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.drift_detection.base_environment_context_drift_detector import BaseEnvironmentContextDriftDetector


class GcpEnvironmentContextDriftDetector(BaseEnvironmentContextDriftDetector):

    @classmethod
    def supported_drift_resource(cls, mergeable: Mergeable):
        pass

    @classmethod
    def convert_to_drift_detection_object(cls, mergeable: Mergeable):
        return mergeable.to_drift_detection_object()
