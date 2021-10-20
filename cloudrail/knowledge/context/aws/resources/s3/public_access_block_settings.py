from enum import Enum
from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class PublicAccessBlockLevel(Enum):
    ACCOUNT = "ACCOUNT"
    BUCKET = "BUCKET"


class PublicAccessBlockSettings(AwsResource):
    """
        Attributes:
            bucket_name_or_account_id: An access block may apply to either a specific
                bucket or a whole account, this is the identifier to use.
            block_public_acls: True if the block shouldn't allow public ACLs.
            ignore_public_acls: True if the block should ignore public ACLs.
            block_public_policy: True if the block shouldn't allow public policies.
            restrict_public_buckets: True if the block should enforce restriction
                on public buckets.
            access_level: Whether the block is on the account or specific bucket.
            account_access_block: The account-level access block, if this one
                targets a bucket only.
    """
    def __init__(self, bucket_name_or_account_id: str, block_public_acls: bool, ignore_public_acls: bool,
                 block_public_policy: bool, restrict_public_buckets: bool, access_level: PublicAccessBlockLevel,
                 account: str, region: str, account_access_block=None) -> None:
        super().__init__(account, region, AwsServiceName.AWS_S3_BUCKET_PUBLIC_ACCESS_BLOCK)
        self.bucket_name_or_account_id: str = bucket_name_or_account_id
        self.block_public_acls: bool = block_public_acls
        self.ignore_public_acls: bool = ignore_public_acls
        self.block_public_policy: bool = block_public_policy
        self.restrict_public_buckets: bool = restrict_public_buckets
        self.access_level: PublicAccessBlockLevel = access_level
        self.account_access_block: PublicAccessBlockSettings = account_access_block

    def get_keys(self) -> List[str]:
        return [self.bucket_name_or_account_id]

    def get_name(self) -> str:
        return f'access block of {self.bucket_name_or_account_id} [{self.access_level.value.lower()}]'

    def is_ignore_public_acls(self) -> bool:
        return self.ignore_public_acls or self.account_access_block.ignore_public_acls

    def is_restrict_public_buckets(self) -> bool:
        return self.restrict_public_buckets or self.account_access_block.block_public_policy

    def get_type(self, is_plural: bool = False) -> str:
        return 'Block public access settings'

    def get_cloud_resource_url(self) -> Optional[str]:
        if self.access_level == PublicAccessBlockLevel.BUCKET:
            return '{0}s3/buckets/{1}?region={2}&tab=permissions' \
                .format(self.AWS_CONSOLE_URL, self.bucket_name_or_account_id, self.region)
        else:
            return '{0}/not-supported'.format(self.AWS_CONSOLE_URL)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'bucket_name_or_account_id': self.bucket_name_or_account_id,
                'block_public_acls': self.block_public_acls,
                'ignore_public_acls': self.ignore_public_acls,
                'block_public_policy': self.block_public_policy,
                'restrict_public_buckets': self.restrict_public_buckets,
                'access_level': self.access_level.value}

def create_pseudo_access_block(bucket_name_or_account_id: str, access_level: PublicAccessBlockLevel,
                               account_id: str, region: str = None) -> PublicAccessBlockSettings:
    access_block = PublicAccessBlockSettings(bucket_name_or_account_id=bucket_name_or_account_id,
                                             block_public_acls=False, ignore_public_acls=False,
                                             block_public_policy=False, restrict_public_buckets=False,
                                             access_level=access_level,
                                             account=account_id,
                                             region=region)
    access_block.is_pseudo = True
    return access_block
