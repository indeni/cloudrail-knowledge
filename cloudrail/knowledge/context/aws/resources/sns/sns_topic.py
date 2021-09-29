from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class SnsTopic(AwsResource):
    """
        Attributes:
            sns_arn: The ARN of this topic.
            sns_name: The name of this SNS topic.
            encrypted_at_rest: True if the topic is set to be encrypted at rest.
            kms_key: The ID of the KMS Key used to encrypt the topic, if any is used.
            kms_data: A reference to KmsKey based on the kms_key provided.
    """
    def __init__(self,
                 sns_arn: str,
                 sns_name: str,
                 encrypted_at_rest: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_SNS_TOPIC)
        self.sns_arn: str = sns_arn
        self.sns_name: str = sns_name
        self.encrypted_at_rest: bool = encrypted_at_rest
        self.kms_key: Optional[str] = None
        self.kms_data: Optional[KmsKey] = None

    def get_keys(self) -> List[str]:
        return [self.sns_arn]

    def get_arn(self) -> str:
        return self.sns_arn

    def get_name(self) -> str:
        return self.sns_name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'SNS topic'
        else:
            return 'SNS topics'

    def get_cloud_resource_url(self) -> str:
        return '{0}sns/v3/home?region={1}#/topic/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.sns_arn)

    @property
    def is_tagable(self) -> bool:
        return True
