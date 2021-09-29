from typing import List, Optional
from botocore.utils import ArnParser
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.arn_utils import is_valid_arn


class AthenaWorkgroup(AwsResource):
    """
        Attributes:
            name: The name of the workgroup.
            state: DISABLED or ENABLED.
            encryption_config: True if any encryption configuration is set, False otherwise.
            enforce_workgroup_config: True to enforce Workgroup encryption configuration on clients.
            encryption_option: Set if encryption is configured, one of SSE_S3, SSE_KMS, CSE_KMS.
            kms_key_arn: Set if KMS is used for encryption, this is the ARN of the key.
            kms_key_id: KMS key unique id.
    """
    def __init__(self,
                 name: str,
                 state: str,
                 encryption_config: bool,
                 enforce_workgroup_config: bool,
                 encryption_option: str,
                 kms_key_arn: str,
                 region: str,
                 account: str,
                 kms_key_id: str = None):
        super().__init__(account, region, AwsServiceName.AWS_ATHENA_WORKGROUP)
        self.name: str = name
        self.state: str = state
        self.encryption_config: bool = encryption_config
        self.enforce_workgroup_config: bool = enforce_workgroup_config
        self.encryption_option: str = encryption_option
        self.kms_key_arn: str = kms_key_arn
        self.kms_key_id: str = kms_key_id or (ArnParser().parse_arn(kms_key_arn)['resource'].replace('key/', '') if
                                              kms_key_arn and is_valid_arn(kms_key_arn) else None)

        self.kms_data: Optional[KmsKey] = None
        if self.account:
            self.arn: str = f'arn:aws:athena:{self.region}:{self.account}:workgroup/{self.name}'
        else:
            self.arn = None

    def get_keys(self) -> List[str]:
        return [self.name, self.region, self.account]

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> str:
        return '{0}athena/workgroup/view-details/{1}/home?region={2}'.format(self.AWS_CONSOLE_URL, self.name, self.region)

    @property
    def is_tagable(self) -> bool:
        return True
