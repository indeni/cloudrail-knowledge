from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class SageMakerEndpointConfig(AwsResource):
    """
        Attributes:
            sagemaker_endpoint_config_name: The name of the endpoint config.
            arn: The ARN of the SageMaker Endpoint Config.
            encrypted: True if encryption is enabled.
    """
    def __init__(self,
                 sagemaker_endpoint_config_name: str,
                 arn: str,
                 encrypted: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_SAGEMAKER_ENDPOINT_CONFIGURATION)
        self.sagemaker_endpoint_config_name: str = sagemaker_endpoint_config_name
        self.arn: str = arn
        self.encrypted: bool = encrypted

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.sagemaker_endpoint_config_name

    def get_arn(self) -> str:
        return self.arn

    @property
    def is_tagable(self) -> bool:
        return True

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'SageMaker Endpoint Configuration'
        else:
            return 'SageMaker Endpoint Configurations'

    def get_cloud_resource_url(self) -> str:
        return '{0}sagemaker/home?region={1}#/endpointConfig/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.sagemaker_endpoint_config_name)
