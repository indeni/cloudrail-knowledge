from typing import Optional, List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import ApiGatewayIntegration
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import RestApiMethod
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ApiGatewayMethod(AwsResource):
    """
        Attributes:
            rest_api_id: The ID of the associated REST API.
            resource_id: The API resource ID.
            http_method: The HTTP Method.
            integration: A reference to the matching ApiGatewayIntegration based on rest_api_id.
            authorization: The type of authorization used for the method.
    """

    def __init__(self, account: str, region: str, rest_api_id: str, resource_id: str, http_method: RestApiMethod, authorization: str):
        super().__init__(account, region, AwsServiceName.AWS_API_GATEWAY_METHOD)
        self.rest_api_id: str = rest_api_id
        self.resource_id: str = resource_id
        self.http_method: RestApiMethod = http_method
        self.integration: Optional[ApiGatewayIntegration] = None
        self.authorization: str = authorization

    def get_keys(self) -> List[str]:
        return [self.rest_api_id, self.resource_id, self.http_method]

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}apigateway/home?region={1}#/apis/{2}/resources/{3}/methods/{4}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.rest_api_id, self.resource_id, self.http_method.name)

    @property
    def is_tagable(self) -> bool:
        return False

    @staticmethod
    def is_standalone() -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'method': self.http_method.value,
                'authorization': self.authorization}
