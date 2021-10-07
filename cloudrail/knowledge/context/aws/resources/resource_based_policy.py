from abc import abstractmethod
from typing import List
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy


class ResourceBasedPolicy(Policy):

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass
