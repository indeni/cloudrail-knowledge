from typing import List

from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.resource_based_policy import ResourceBasedPolicy


class S3AccessPointPolicy(ResourceBasedPolicy):

    def __init__(self, account: str, region: str, access_point_name: str, statements: List[PolicyStatement],
                 raw_document: str):
        self.access_point_name: str = access_point_name
        self.region: str = region
        super().__init__(account, statements, raw_document)

    def get_keys(self) -> List[str]:
        return [self.access_point_name]

    def __str__(self) -> str:
        return self.access_point_name + " policy"

    def get_cloud_resource_url(self) -> str:
        return 'https://s3.console.aws.amazon.com/s3/ap/{0}/{1}?region={2}' \
            .format(self.account, self.access_point_name, self.region)
