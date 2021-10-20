from typing import List
from cloudrail.knowledge.context.aws.resources.resource_based_policy import ResourceBasedPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class SecretsManagerSecretPolicy(ResourceBasedPolicy):
    """
        Attributes:
            secret_arn: The ARN of the secret.
            policy_statements: The statements of the policy.
            raw_document: The raw JSON of the policy.
    """
    def __init__(self,
                 secret_arn: str,
                 policy_statements: List[PolicyStatement],
                 raw_document: str,
                 account: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_SECRETSMANAGER_SECRET_POLICY)
        self.secret_arn: str = secret_arn

    def get_keys(self) -> List[str]:
        return [self.secret_arn]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Secrets Manager Secrets resource policy'
        else:
            return 'Secrets Manager Secrets resource policies'

    def to_drift_detection_object(self) -> dict:
        return {'secret_arn': self.secret_arn,
                'policy_statements': [statement.to_dict() for statement in self.statements]}
