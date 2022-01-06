from abc import abstractmethod
from typing import Dict, List, Optional
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName, AwsServiceAttributes
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.utils.arn_utils import are_arns_intersected


class AwsResource(Mergeable):
    GLOBAL_REGION = 'GLOBAL_REGION'
    AWS_CONSOLE_URL = 'https://console.aws.amazon.com/'

    def __init__(self,
                 account: str,
                 region: str,
                 tf_resource_type: AwsServiceName = AwsServiceName.NONE,
                 aws_service_attributes: AwsServiceAttributes = None):
        super().__init__()
        self.account: str = account
        self.region: str = region
        self.tags: Dict[str, str] = {}
        self.tf_resource_type: AwsServiceName = tf_resource_type
        self.aws_service_attributes: Optional[AwsServiceAttributes] = aws_service_attributes

    def get_terraform_resource_type(self) -> AwsServiceName:
        return self.tf_resource_type

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    def get_aws_service_attributes(self) -> Optional[AwsServiceAttributes]:
        return self.aws_service_attributes

    def get_aws_service_type(self) -> Optional[str]:
        return None if self.aws_service_attributes is None else self.aws_service_attributes.get_service_type()

    @abstractmethod
    def get_arn(self) -> str:
        pass

    def get_friendly_name(self) -> str:
        if self.iac_state:
            return self.iac_state.address
        return self.get_name() or self.get_id() or self.get_arn()

    def is_arn_match(self, arn: str):
        return are_arns_intersected(arn, self.get_arn())

    def get_cfn_resource_id(self):
        return self.get_id()
