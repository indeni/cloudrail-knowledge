from typing import Set

from cloudrail.knowledge.drift_detection.base_environment_context_drift_detector import BaseEnvironmentContextDriftDetector


class GcpEnvironmentContextDriftDetector(BaseEnvironmentContextDriftDetector):

    @classmethod
    def get_excluded_attributes(cls) -> Set[str]:
        return set()
