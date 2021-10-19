from typing import List
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class EmrPublicAccessConfiguration(AwsResource):
    """
    Attributes:
        account: The account ID in which this resource operates.
        region: The region name in which this resource operates.
        block_public_access: Does the EMR cluster being created into this region will block public access or not.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 block_public_access: bool):
        super().__init__(account, region, AwsServiceName.NONE)
        self.block_public_access: bool = block_public_access

    def get_keys(self) -> List[str]:
        return [self.account, self.region]

    def get_name(self) -> str:
        return f'EMR block public access configuration for region {self.region} in account {self.account}'

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}elasticmapreduce/home?region={1}#block-public-access:'\
            .format(self.AWS_CONSOLE_URL, self.region)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'block_public_access': self.block_public_access}
