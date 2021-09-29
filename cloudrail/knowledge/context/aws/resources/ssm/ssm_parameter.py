from typing import List
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class SsmParameter(AwsResource):
    """
        Attributes:
            name: The name of the SSM parameter.
            ssm_type: The type of the SSM parameter.
            kms_key_id: The ID of the KMS Key used to encrypt the parameter, if any is used.
            kms_data: A reference to KmsKey based on the kms_key provided.
    """
    def __init__(self,
                 name: str,
                 ssm_type: str,
                 kms_key_id: str,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_SSM_PARAMETER)
        self.name: str = name
        self.ssm_type: str = ssm_type
        self.kms_key_id: str = kms_key_id
        self.kms_data: KmsKey = None
        if self.account:
            self.arn: str = f'arn:aws:ssm:{self.region}:{self.account}:parameter/{self.name}'
        else:
            self.arn = None

    def get_keys(self) -> List[str]:
        return [self.account, self.region,  self.name]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'SSM Parameter'
        else:
            return 'SSM Parameters'

    def get_cloud_resource_url(self) -> str:
        return '{0}systems-manager/parameters/{1}/description?region={2}&tab=Table'\
            .format(self.AWS_CONSOLE_URL, self.name, self.region)

    def get_arn(self) -> str:
        return self.arn

    @property
    def is_tagable(self) -> bool:
        return True
