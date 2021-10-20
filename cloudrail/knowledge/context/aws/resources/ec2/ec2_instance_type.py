from dataclasses import dataclass
from typing import List

import dataclasses
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


@dataclass
class EbsInfo:
    """
        ebs_optimized_support: Indicates whether the instance type is Amazon EBS-optimized.
        encryption_support: Indicates whether Amazon EBS encryption is supported.
    """
    ebs_optimized_support: str
    encryption_support: str


class Ec2InstanceType(AwsResource):
    """
        Attributes:
            instance_type: The Instance type (i.e. 'm5.8xlarge').
            ebs_info: Information about the EBS attributes of the instance.
    """

    def __init__(self,
                 instance_type: str,
                 ebs_info: EbsInfo):
        super().__init__(None, AwsResource.GLOBAL_REGION, AwsServiceName.NONE)
        self.instance_type: str = instance_type
        self.ebs_info: EbsInfo = ebs_info

    def get_keys(self) -> List[str]:
        pass

    def get_name(self) -> str:
        return f'Instance Type {self.instance_type} of region {self.region}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'EC2 Instance type'
        else:
            return 'EC2 Instance types'

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2/v2/home?region={1}#InstanceTypes:'.format(self.AWS_CONSOLE_URL, self.region)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'instance_type': self.instance_type,
                'ebs_info': dataclasses.asdict(self.ebs_info)}
