from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class RedshiftLogging(AwsResource):
    """
        Attributes:
            cluster_identifier: The ID for the Redshift cluster.
            s3_bucket: The S3 bucket name which the Redshift logs should be stored at.
            s3_prefix: A prefix string to be applied to the log file names.
            logging_enabled: Indication if the logs are enabled for the Redshift cluster.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 cluster_identifier: str,
                 s3_bucket: Optional[str],
                 s3_prefix: Optional[str],
                 logging_enabled: bool):
        super().__init__(account, region, AwsServiceName.AWS_REDSHIFT_CLUSTER)
        self.cluster_identifier: str = cluster_identifier
        self.s3_bucket: Optional[str] = s3_bucket
        self.s3_prefix: Optional[str] = s3_prefix
        self.logging_enabled: bool = logging_enabled

    def get_keys(self) -> List[str]:
        return [self.cluster_identifier]

    def get_name(self) -> str:
        return self.cluster_identifier

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}redshiftv2/home?region={1}#cluster-details?cluster={2}&tab=properties' \
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_identifier)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'cluster_identifier': self.cluster_identifier,
                's3_bucket': self.s3_bucket,
                's3_prefix': self.s3_prefix,
                'logging_enabled': self.logging_enabled}
