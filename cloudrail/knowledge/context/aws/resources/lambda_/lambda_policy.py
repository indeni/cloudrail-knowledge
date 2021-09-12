from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import create_lambda_function_arn
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.utils import hash_list


class LambdaPolicy(Policy):
    """
        Attributes:
            function_name: The name of the Lambda Function the policy statements are for.
            statements: The statements themselves.
            qualifier: A Lambda Function may have a qualified set, this will be it
                (or None).
            lambda_func_arn: The ARN of the Lambda Function these policy statements are for.
    """
    def __init__(self, account: str, region: str, function_name: str,
                 statements: List[PolicyStatement], qualifier: str = None):
        super().__init__(account, statements, None, AwsServiceName.AWS_LAMBDA_PERMISSION)
        self.function_name: str = function_name
        self.qualifier: str = qualifier
        self.region: str = region

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_id(self) -> str:
        return str(hash_list(self.statements))

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}lambda/home?{1}#/functions/{2}?tab=permissions'\
            .format(self.AWS_CONSOLE_URL, self.region, self.function_name)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def lambda_func_arn(self) -> str:
        if ':' in self.function_name:
            if self.qualifier and self.qualifier in self.function_name:
                return create_lambda_function_arn(self.account, self.region, self.function_name.split(':')[-2], self.qualifier)
            else:
                return create_lambda_function_arn(self.account, self.region, self.function_name.split(':')[-1], self.qualifier)
        else:
            return create_lambda_function_arn(self.account, self.region, self.function_name, self.qualifier)
