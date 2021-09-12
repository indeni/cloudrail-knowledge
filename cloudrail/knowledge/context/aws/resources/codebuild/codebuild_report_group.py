from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CodeBuildReportGroup(AwsResource):
    """
        Attributes:
            name: The name of the report group.
            export_config_type: S3 or NO_EXPORT.
            export_config_s3_destination_bucket: If S3 type is used, the destination bucket.
            export_config_s3_destination_encryption_key: If S3 type is used,
                the encryption key to use.
            export_config_s3_destination_encryption_disabled: If S3 type is used,
                whether or not encryption is enabled.
            export_config_s3_destination_kms_data: If encryption is used, the KMS key
                used to encrypt.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 export_config_type: str,
                 export_config_s3_destination_bucket: str,
                 export_config_s3_destination_encryption_key: str,
                 export_config_s3_destination_encryption_disabled: bool,
                 arn: str):
        super().__init__(account, region, AwsServiceName.AWS_CODEBUILD_REPORT_GROUP)
        self.name: str = name
        self.export_config_type: str = export_config_type
        self.export_config_s3_destination_bucket: str = export_config_s3_destination_bucket
        self.export_config_s3_destination_encryption_disabled: bool = export_config_s3_destination_encryption_disabled
        self.export_config_s3_destination_encryption_key: str = export_config_s3_destination_encryption_key
        self.arn: str = arn
        self.export_config_s3_destination_kms_data: KmsKey = None
        self.with_aliases(arn)

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_id(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CodeBuild Report Group'
        else:
            return 'CodeBuild Report Groups'

    def get_cloud_resource_url(self) -> Optional[str]:
        if self.account:
            return 'https://console.aws.amazon.com/codesuite/codebuild/{0}/testReports/reportGroups/{1}'\
                .format(self.account, self.name)
        else:
            return None

    @property
    def is_tagable(self) -> bool:
        return True
