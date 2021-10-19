from enum import Enum
from typing import List, Tuple

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.s3.s3_policy import S3Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class S3PredefinedGroups(Enum):
    ALL_USERS = 'http://acs.amazonaws.com/groups/global/AllUsers'
    LOG_DELIVERY = 'http://acs.amazonaws.com/groups/s3/LogDelivery'
    AUTHENTICATED_USERS = 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers'


class GranteeTypes(Enum):
    GROUP = "Group"
    CANONICAL_USER = 'CanonicalUser'

    @staticmethod
    def get_type_value(grantee_type, raw_data: dict):
        if grantee_type == GranteeTypes.GROUP:
            return raw_data.get('URI') or raw_data.get('uri')
        else:
            return raw_data.get('ID') or raw_data.get('id')


class S3Permission(Enum):

    WRITE: Tuple[str] = ('s3:PutObject', 's3:DeleteObject')
    READ: Tuple[str] = ('s3:ListBucket', 's3:ListBucketVersions', 's3:ListBucketMultipartUploads')
    READ_ACP: Tuple[str] = ('s3:GetBucketAcl', )
    WRITE_ACP: Tuple[str] = ('s3:PutBucketAcl', )
    READ_WRITE: Tuple[str] = WRITE + READ
    FULL_CONTROL: Tuple[str] = WRITE + READ + WRITE_ACP + READ_ACP


class S3ACL(AwsResource):
    """
        Attributes:
            actions: A list of S3 actions included in this S3 ACL, based on
                the list from the S3Permission supplied.
            type: The type of the grantee - GROUP or CANONICAL_USER.
            type_value: The value of the grantee. If type is GROUP, this will be
                the group identifier. If CANONICAL_USER, this will be the
                canonical identifier for the user.
            bucket_name: The bucket to apply the ACL to.
            owner_id: The owner of this ACL.
            owner_name: The name of the owner.
    """
    def __init__(self, s3_permission: S3Permission, grantee_type: GranteeTypes, type_value: str, bucket_name: str,
                 account: str, region: str, owner_id: str = None, owner_name: str = None):
        super().__init__(account, region, AwsServiceName.NONE)
        self.actions: Tuple[str] = s3_permission.value
        self.type: GranteeTypes = grantee_type
        self.type_value: str = type_value
        self.bucket_name: str = bucket_name
        self.owner_id: str = owner_id
        self.owner_name: str = owner_name

    def get_keys(self) -> List[str]:
        return [self.bucket_name, self.type_value] + list(self.actions)

    def as_policy(self) -> S3Policy:
        if self.type == GranteeTypes.GROUP and self.type_value == S3PredefinedGroups.ALL_USERS.value:
            return S3Policy(self.account, self.bucket_name,
                            [PolicyStatement(StatementEffect.ALLOW, self.actions, ["*"], Principal(PrincipalType.PUBLIC, []))], None)
        if self.type == GranteeTypes.GROUP and self.type_value == S3PredefinedGroups.AUTHENTICATED_USERS.value:
            return S3Policy(self.account, self.bucket_name,
                            [PolicyStatement(StatementEffect.ALLOW, self.actions, ["*"], Principal(PrincipalType.AWS, ['arn:aws:*:::*']))], None)

        return S3Policy(self.account, self.bucket_name, [], None)

    def get_extra_data(self) -> str:
        bucket_name = 'bucket_name: {}'.format(self.bucket_name) if self.bucket_name else ''
        s3_type = 'type: {}'.format(self.type) if self.type else ''
        type_value = 'type_value: {}'.format(self.type_value) if self.type_value else ''

        return ', '.join([bucket_name, s3_type, type_value])

    def is_grantee_owner(self) -> bool:
        return self.type == GranteeTypes.CANONICAL_USER and self.type_value == self.owner_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'S3 ACL'
        else:
            return "S3 ACL's"

    def get_cloud_resource_url(self) -> str:
        return 'https://s3.console.aws.amazon.com/s3/buckets/{0}?region={1}&tab=objects'\
            .format(self.bucket_name, self.region)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def is_standalone(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'actions': self.actions,
                'type': self.type.value,
                'type_value': self.type_value,
                'bucket_name': self.bucket_name}
