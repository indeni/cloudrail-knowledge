from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.utils.tags_utils import filter_tags


class ElasticIp(AwsResource):
    """
        Attributes:
            allocation_id: The ID of the elastic IP's allocation.
            public_ip: The public IP of the elastic IP. May be "0.0.0.0" to denote
                that we do not know what it is (usually when the resource is
                still being built).
            private_ip: The private IP of the elastic IP, may be None.
    """

    def __init__(self, allocation_id: str, public_ip: Optional[str], private_ip: Optional[str], region: str, account: str):
        super().__init__(account, region, AwsServiceName.AWS_ELASTIC_IP)
        self.allocation_id: str = allocation_id
        self.public_ip: str = public_ip or "0.0.0.0"
        self.with_aliases(self.public_ip)
        self.private_ip: Optional[str] = private_ip

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.public_ip]

    def get_id(self) -> str:
        return self.allocation_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Elastic IP address'
        else:
            return 'Elastic IP addresses'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#Addresses:public-ip={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.public_ip)

    def get_arn(self) -> Optional[str]:
        if self.account:
            return f'arn:aws:ec2:us-east-1:{self.account}:elastic-ip/{self.allocation_id}'
        else:
            return None

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags)}
