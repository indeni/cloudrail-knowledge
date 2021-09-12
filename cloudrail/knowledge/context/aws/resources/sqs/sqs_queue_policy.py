from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class SqsQueuePolicy(Policy):
    """
        Attributes:
            queue_name: The name of the queue.
            policy_statements: The statements of the policy.
            raw_document: The raw JSON of the policy.
    """
    def __init__(self,
                 queue_name: str,
                 policy_statements: Optional[List[PolicyStatement]],
                 raw_document: str,
                 account: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_SQS_QUEUE_POLICY)
        self.queue_name: str = queue_name

    def get_keys(self) -> List[str]:
        return [self.queue_name, self.account, self.region]

    def get_name(self) -> str:
        return self.queue_name + " policy"

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'SQS queue resource policy'
        else:
            return 'SQS queue resource policies'
