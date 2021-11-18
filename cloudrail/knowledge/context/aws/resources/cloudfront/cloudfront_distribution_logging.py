from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudfrontDistributionLogging(AwsResource):
    """
        Attributes:
            name: The name of the workgroup.
            arn: The ARN of the CloudFront Distribution.
            distribution_id: The ID of the distribution.
            include_cookies: Specifies whether CloudFront will include cookies in access logs.
            s3_bucket: The S3 bucket to store access logs into.
            prefix: String to add as a prefix to access log file names.
            logging_enabled: Indication if access logging is enabled.
    """

    def __init__(self,
                 arn: str,
                 name: str,
                 distribution_id: str,
                 account: str,
                 include_cookies: bool,
                 s3_bucket: Optional[str],
                 prefix: Optional[str],
                 logging_enabled: bool):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_CLOUDFRONT_DISTRIBUTION_LIST)
        self.arn: str = arn
        self.name: str = name
        self.distribution_id: str = distribution_id
        self.include_cookies: bool = include_cookies
        self.s3_bucket: Optional[str] = s3_bucket
        self.prefix: Optional[str] = prefix
        self.logging_enabled: bool = logging_enabled

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.distribution_id

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> str:
        return '{0}cloudfront/home?region={1}#distribution-settings:{2}'\
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.distribution_id)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'include_cookies': self.include_cookies,
                's3_bucket': self.s3_bucket,
                'prefix': self.prefix,
                'logging_enabled': self.logging_enabled}
