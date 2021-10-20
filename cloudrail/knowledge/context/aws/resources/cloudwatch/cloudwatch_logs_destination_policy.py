from typing import List
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.resource_based_policy import ResourceBasedPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement


class CloudWatchLogsDestinationPolicy(ResourceBasedPolicy):
    """
        Attributes:
            destination_name: The name of the destination the policy applies to.
            statements: The list of statements in the policy.
            uuid: A randomly generated uuid for the policy (ignore, for internal use).
            raw_document: The raw JSON of the policy.
            access_analyzer_findings: The results from running IAM Access Analyzer's
                policy validation API on this policy's JSON.
            policy_type: The type of the policy (identity, resource, SCP).
    """
    def __init__(self,
                 destination_name: str,
                 policy_statements: List[PolicyStatement],
                 raw_document: str,
                 region: str,
                 account: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_CLOUDWATCH_LOG_DESTINATION_POLICY)
        self.destination_name: str = destination_name
        self.region: str = region

    def get_keys(self) -> List[str]:
        return [self.destination_name, self.region, self.account]

    def get_name(self) -> str:
        return self.destination_name + " policy"

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudWatch Logs Destination policy'
        else:
            return 'CloudWatch Logs Destination policies'

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'destination_name': self.destination_name,
                'statements': [statement.to_dict() for statement in self.statements]}
