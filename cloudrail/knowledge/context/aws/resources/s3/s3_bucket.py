from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_logging import S3BucketLogging
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_object import S3BucketObject
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_versioning import S3BucketVersioning
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName, AwsServiceType, AwsServiceAttributes
from cloudrail.knowledge.context.connection import ConnectionInstance
from cloudrail.knowledge.context.aws.resources.s3.s3_policy import S3Policy
from cloudrail.knowledge.context.aws.resources.s3.public_access_block_settings import PublicAccessBlockSettings
from cloudrail.knowledge.context.aws.resources.s3.s3_acl import S3ACL
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_access_point import S3BucketAccessPoint, S3BucketAccessPointNetworkOriginType
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_encryption import S3BucketEncryption


class S3Bucket(ConnectionInstance, AwsResource):
    """
        Attributes:
            bucket_name: The name of the bucket.
            arn: The ARN of the bucket.
            resource_based_policy: the policy of this S3 bucket.
            acls: The list of ACLs applied to this bucket.
            public_access_block_settings: The public access block applied to this
                bucket specifically, if any (or None).
            access_points: The access points defined for this bucket.
            encryption_data: The encryption configuration for this bucket.
            bucket_objects: A list of objects in this bucket. NOTE: This is not
                fetched from the live environment and will only include objects
                that are defined in the infrastructure-as-code reviewed by Cloudrail.
            versioning_data: Configuration of versioning on the bucket.
            publicly_allowing_resources: ACL's/Policies that expose this bucket to the internet.
            exposed_to_agw_methods: The ApiGateway methods that can acccess this bucket.
            is_logger: Indicates if this bucket is the target bucket for logging of another bucket.
    """
    def __init__(self, account: str, bucket_name: str, arn: str, region: str = None,
                 policy: S3Policy = None):
        AwsResource.__init__(self, account, region, AwsServiceName.AWS_S3_BUCKET,
                                     AwsServiceAttributes(aws_service_type=AwsServiceType.S3.value, region=region))
        ConnectionInstance.__init__(self)
        self.resource_based_policy = policy
        self.bucket_name = bucket_name
        self.arn = arn
        self.bucket_domain_name = bucket_name + ".s3.amazonaws.com"
        self.bucket_regional_domain_name = '.'.join([bucket_name, 's3', region or '', 'amazonaws.com'])
        self.with_aliases(bucket_name, arn, self.bucket_domain_name)
        self.acls: List[S3ACL] = []
        self.public_access_block_settings: Optional[PublicAccessBlockSettings] = None
        self.access_points: List[S3BucketAccessPoint] = []
        self.encryption_data: Optional[S3BucketEncryption] = None
        self.bucket_objects: List[S3BucketObject] = []
        self.versioning_data: S3BucketVersioning = None
        self.bucket_logging: Optional[S3BucketLogging] = None
        self.publicly_allowing_resources: List[AwsResource] = []
        self.exposed_to_agw_methods: List[ApiGatewayMethod] = []
        self.is_logger = False

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_vpc_access_points(self, vpc_id: str):
        return [x for x in self.access_points
                if x.network_origin.access_type == S3BucketAccessPointNetworkOriginType.VPC and
                x.network_origin.vpc_id == vpc_id]

    def get_arn(self) -> str:
        return self.arn

    def get_name(self) -> str:
        return self.bucket_name

    def get_id(self) -> str:
        return self.get_name()

    def __str__(self) -> str:
        return self.bucket_name

    def get_cloud_resource_url(self) -> str:
        return 'https://s3.console.aws.amazon.com/s3/buckets/{0}?region={1}&tab=objects'\
            .format(self.bucket_name, self.region)

    @property
    def is_tagable(self) -> bool:
        return True

    @property
    def is_public(self):
        return len(self.publicly_allowing_resources) > 0
