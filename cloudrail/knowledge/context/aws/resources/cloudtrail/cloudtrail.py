from typing import List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudTrail(AwsResource):
    """
        Attributes:
            name: The name of the CloudTrail trail.
            kms_encryption: True if KMS encryption is used.
            arn: The ARN of the CloudTrail trail.
            log_file_validation: True if log file validation is enabled.
            is_multi_region_trail: An indication if the trail is created in the current region or in all regions.
    """
    def __init__(self,
                 name: str,
                 kms_encryption: bool,
                 arn: str,
                 log_file_validation: bool,
                 region: str,
                 account: str,
                 is_multi_region_trail: bool):
        super().__init__(account, region, AwsServiceName.AWS_CLOUDTRAIL)
        self.name: str = name
        self.kms_encryption: bool = kms_encryption
        self.arn: str = arn
        self.log_file_validation: bool = log_file_validation
        self.is_multi_region_trail: bool = is_multi_region_trail
        self.with_aliases(name)

    def get_id(self) -> str:
        return self.name

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudTrail'
        else:
            return 'CloudTrails'

    def get_cloud_resource_url(self) -> str:
        return '{0}cloudtrail/home?region={1}#/trails/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.arn)

    @property
    def is_tagable(self) -> bool:
        return True
