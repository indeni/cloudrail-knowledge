from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class S3BucketLogging(AwsResource):
    """
        Attributes:
            bucket_name: The bucket which the logs associated with.
            target_bucket: The bucket name in which to send logs for this bucket.
            target_prefix: A key prefix for log objects.
    """
    def __init__(self,
                 bucket_name: str,
                 target_bucket: Optional[str],
                 target_prefix: Optional[str],
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_S3_BUCKET_OBJECT)
        self.bucket_name: str = bucket_name
        self.target_bucket: Optional[str] = target_bucket
        self.target_prefix: Optional[str] = target_prefix

    def get_keys(self) -> List[str]:
        return [self.bucket_name, self.account, self.region]

    def get_name(self) -> str:
        return self.bucket_name

    def get_cloud_resource_url(self) -> str:
        return 'https://s3.console.aws.amazon.com/s3/buckets/{0}?region={1}&tab=objects'\
            .format(self.bucket_name, self.region)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'bucket_name': self.bucket_name,
                'target_bucket': self.target_bucket,
                'target_prefix': self.target_prefix}
