import copy
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import create_lambda_function_arn
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.resource_based_policy import ResourceBasedPolicy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.utils import hash_list


class LambdaPolicy(ResourceBasedPolicy):
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
        return [self.lambda_func_arn]

    def get_id(self) -> str:
        return str(hash_list(self._get_statements_without_policy_attribute()))

    def _get_statements_without_policy_attribute(self) -> List[PolicyStatement]:
        statements_copy: List[PolicyStatement] = copy.deepcopy(self.statements)
        for stat in statements_copy:
            del stat.policy
        return statements_copy

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
        return create_lambda_function_arn(self.account, self.region, self.function_name, self.qualifier)

    def to_drift_detection_object(self) -> dict:
        return {'function_name': self.function_name,
                'qualifier': self.qualifier,
                'policy_statements': [statement.to_dict() for statement in self.statements]}
