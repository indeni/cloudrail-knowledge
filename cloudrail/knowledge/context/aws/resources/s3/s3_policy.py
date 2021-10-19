from typing import List

from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.resource_based_policy import ResourceBasedPolicy


class S3Policy(ResourceBasedPolicy):

    def __init__(self, account: str, bucket_name: str, statements: List[PolicyStatement], raw_document: str):
        self.bucket_name: str = bucket_name
        super().__init__(account, statements, raw_document)

    def get_keys(self) -> List[str]:
        return [self.bucket_name]

    def __str__(self) -> str:
        return self.bucket_name + " policy"

    def get_cloud_resource_url(self) -> str:
        return 'https://s3.console.aws.amazon.com/s3/buckets/{0}-{1}?region={1}&tab=permissions' \
            .format(self.bucket_name, 'us-east-1')

    def to_drift_detection_object(self) -> dict:
        return {'bucket_name': self.bucket_name,
                'policy_statements': [statement.to_dict() for statement in self.statements]}
