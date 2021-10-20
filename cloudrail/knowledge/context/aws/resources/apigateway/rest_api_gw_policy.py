from typing import List
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.resource_based_policy import ResourceBasedPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement


class RestApiGwPolicy(ResourceBasedPolicy):
    """
        Attributes:
            rest_api_gw_id: The ID of the REST API Gateway.
            policy_statements: The statements of the resource policy attached to this gateway.
            raw_document: The raw JSON of the resource policy.
    """

    def __init__(self,
                 rest_api_gw_id: str,
                 policy_statements: List[PolicyStatement],
                 raw_document: str,
                 account: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_API_GATEWAY_REST_API_POLICY)
        self.rest_api_gw_id: str = rest_api_gw_id

    def get_keys(self) -> List[str]:
        return [self.rest_api_gw_id]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API Gateway resource policy'
        else:
            return 'API Gateway resource policies'

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'policy_statements': [statement.to_dict() for statement in self.statements]}
