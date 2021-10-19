from dataclasses import dataclass
from enum import Enum
from typing import List

import dataclasses
from cloudrail.knowledge.context.aws.resources.aws_policied_resource import PoliciedResource
from cloudrail.knowledge.context.aws.resources.s3.s3_access_point_policy import S3AccessPointPolicy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class S3BucketAccessPointNetworkOriginType(str, Enum):
    VPC: str = 'VPC'
    INTERNET: str = 'Internet'


@dataclass
class S3BucketAccessPointNetworkOrigin:
    access_type: str
    vpc_id: str


class S3BucketAccessPoint(PoliciedResource):
    """
        Attributes:
            bucket_name: The name of the bucket this access point applies to.
            name: The name of the access point.
            network_origin: The network-level source of the traffic.
            arn: The ARN of the access point.
            policy: The policy applied to the access point.
    """

    def __init__(self, bucket_name: str, name: str, network_origin: S3BucketAccessPointNetworkOrigin,
                 arn: str, region: str, account: str, policy: S3AccessPointPolicy = None):
        super().__init__(account, region, AwsServiceName.AWS_S3_ACCESS_POINT, policy)
        self.bucket_name = bucket_name
        self.name = name
        self.network_origin = network_origin
        self.arn = arn

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_extra_data(self) -> str:
        bucket_name = 'bucket_name: {}'.format(self.bucket_name) if self.bucket_name else ''

        return ', '.join([bucket_name])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'S3 Access Point'
        else:
            return 'S3 Access Points'

    def get_cloud_resource_url(self) -> str:
        return 'https://s3.console.aws.amazon.com/s3/ap/{0}/{1}?region={2}' \
            .format(self.account, self.name, self.region)

    def get_arn(self) -> str:
        return self.arn

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'bucket_name': self.bucket_name,
                'name': self.name,
                'network_origin': dataclasses.asdict(self.network_origin)}
