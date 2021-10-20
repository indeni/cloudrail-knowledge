from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.arn_utils import is_valid_arn


class LambdaAlias(AwsResource):
    """
        Attributes:
            arn: The ARN of the Lambda Alias.
            name: The name of the alias.
            function_name_or_arn: The name of the Lambda function or its ARN.
            function_version: The version of the Lambda function this alias
                is targeting.
            description: The description of the alias.

    """

    def __init__(self, account: str, region: str, arn: str, name: str, function_name_or_arn: str, function_version: str, description: str = None):
        super().__init__(account, region, AwsServiceName.AWS_LAMBDA_ALIAS)
        self.arn: str = arn
        self.name: str = name
        self.with_aliases(arn)
        self.function_version: str = function_version
        self.description: str = description
        self.function_name_or_arn: str = function_name_or_arn
        if is_valid_arn(function_name_or_arn) or function_name_or_arn.endswith('.arn'):
            self.function_arn = function_name_or_arn
        else:
            self.function_arn = create_lambda_function_arn(account, region, function_name_or_arn, function_version)
        self.with_aliases(self.function_arn)

    def get_keys(self) -> List[str]:
        return [self.function_arn, self.name]

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}lambda/home?region={1}#/functions/{2}/aliases/{3}?tab=configuration' \
            .format(self.AWS_CONSOLE_URL, self.region, self.function_name_or_arn, self.name)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name,
                'function_name_or_arn': self.function_name_or_arn,
                'function_version': self.function_version,
                'description': self.description}


def create_lambda_function_arn(account_id: str, region: str, lambda_func_name: str, qualifier: str = ''):
    qualifier = ':' + qualifier if qualifier and qualifier != '$LATEST' else ''
    return f"arn:aws:lambda:{region}:{account_id}:function:{lambda_func_name}{qualifier}"
