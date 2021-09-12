from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class S3BucketObject(AwsResource):
    """
        NOTE: Cloudrail does not map objects in the live environment. Instead.
        only onjects specifically defined in infrastructure-as-code will be
        included as part of the context.

        Attributes:
            bucket_name: The bucket the object is in.
            key: The ARN of the key used to encrypt the object, if any.
            encrypted: True if the object is encrypted.
            owning_bucket: A pointer to the owning bucket.
    """
    def __init__(self,
                 bucket_name: str,
                 key: str,
                 encrypted: bool,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_S3_BUCKET_OBJECT)
        self.bucket_name: str = bucket_name
        self.key: str = key
        self.encrypted: bool = encrypted
        self.owning_bucket: 'S3Bucket' = None

    def get_keys(self) -> List[str]:
        return [self.bucket_name, self.key]

    def get_name(self) -> str:
        return self.key

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'S3 Bucket object'
        else:
            return 'S3 Bucket objects'

    def get_cloud_resource_url(self) -> str:
        return 'https://s3.console.aws.amazon.com/s3/object/{0}?region={1}&prefix={2}'\
            .format(self.bucket_name, self.region, self.key)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
