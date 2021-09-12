from abc import abstractmethod
from typing import Optional, List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.resource_based_policy import ResourceBasedPolicy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName, AwsServiceAttributes


class AwsResourceWithBasedPolicy(AwsResource):

    def __init__(self, account: str, region: str, tf_resource_type: AwsServiceName, aws_service_attributes: AwsServiceAttributes = None):
        super().__init__(account, region, tf_resource_type, aws_service_attributes)
        self.resource_based_policy: Optional[ResourceBasedPolicy] = None

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
