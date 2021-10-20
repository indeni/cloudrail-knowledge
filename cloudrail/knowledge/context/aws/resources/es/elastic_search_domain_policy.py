from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.resource_based_policy import ResourceBasedPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ElasticSearchDomainPolicy(ResourceBasedPolicy):
    """
        Attributes:
            domain_name: The name of the domain the policy is related to.
            policy_statements: The statements contained in the policy.
            raw_document: The raw JSON content of the policy.
    """

    def __init__(self,
                 domain_name: str,
                 policy_statements: Optional[List[PolicyStatement]],
                 raw_document: str,
                 account: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_ELASTICSEARCH_DOMAIN_POLICY)
        self.domain_name: str = domain_name

    def get_keys(self) -> List[str]:
        return [self.domain_name, self.region, self.account]

    def get_name(self) -> str:
        return self.domain_name + " policy"

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ElasticSearch Domain resource policy'
        else:
            return 'ElasticSearch Domain resource policies'

    def to_drift_detection_object(self) -> dict:
        return {'domain_name': self.domain_name,
                'policy_statements': [statement.to_dict() for statement in self.statements]}
