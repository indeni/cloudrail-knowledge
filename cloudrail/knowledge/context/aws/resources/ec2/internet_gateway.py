from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ec2.igw_type import IgwType
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.utils.tags_utils import filter_tags


class InternetGateway(AwsResource):
    """
        Attributes:
            vpc_id: The ID of the VPC the IGW belongs to.
            igw_id: The ID of the IGW.
            igw_type: The type of the IGW.
    """

    def __init__(self, account: str, region: str, vpc_id: str, igw_id: str, igw_type: IgwType,
                 tf_resource_type: AwsServiceName = AwsServiceName.AWS_INTERNET_GATEWAY):
        super().__init__(account, region, tf_resource_type)
        self.vpc_id: str = vpc_id
        self.igw_id: str = igw_id
        self.igw_type: IgwType = igw_type
        self.with_aliases(igw_id)

    def get_keys(self) -> List[str]:
        return [self.igw_id]

    def get_id(self) -> str:
        return self.igw_id

    def __str__(self) -> str:
        return "igw_type={}, igw_id={}, vpc_id={}".format(self.igw_type, self.igw_id, self.vpc_id)

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Internet gateway'
        else:
            return 'Internet gateways'

    def get_cloud_resource_url(self) -> str:
        return f'{self.AWS_CONSOLE_URL}vpc/home?region={self.region}#InternetGateway:internetGatewayId={self.igw_id}'

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'vpc_id': self.vpc_id,
                'igw_type': self.igw_type.value}
