from typing import List

from cloudrail.knowledge.context.aws.resources.resource_based_policy import ResourceBasedPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class EcrRepositoryPolicy(ResourceBasedPolicy):
    """
        Attributes:
            repo_name: The repository the policy applies to.
            policy_statements: The statements included in the policy.
            raw_document: The raw JSON code of the policy.
    """

    def __init__(self,
                 repo_name: str,
                 policy_statements: List[PolicyStatement],
                 raw_document: str,
                 account: str,
                 region: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_ECR_REPOSITORY_POLICY)
        self.repo_name: str = repo_name
        self.region: str = region
        self.account: str = account

    def get_keys(self) -> List[str]:
        return [self.repo_name, self.region, self.account]

    def get_name(self) -> str:
        return self.repo_name + " policy"

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ECR repository resource policy'
        else:
            return 'ECR repository resource policies'

    def to_drift_detection_object(self) -> dict:
        return {'repo_name': self.repo_name,
                'policy_statements': [statement.to_dict() for statement in self.statements]}
