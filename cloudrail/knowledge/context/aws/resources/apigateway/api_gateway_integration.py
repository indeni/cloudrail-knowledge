from enum import Enum
from typing import Optional, List
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import RestApiMethod
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class IntegrationType(str, Enum):
    """
        The type of integration.
    """
    HTTP = 'HTTP'
    MOCK = 'MOCK'
    AWS = 'AWS'
    AWS_PROXY = 'AWS_PROXY'
    HTTP_PROXY = 'HTTP_PROXY'
    NONE = None


class ApiGatewayIntegration(AwsResource):
    """
    Attributes:
        rest_api_id: The ID of the associated REST API.
        resource_id: The API resource ID.
        request_http_method: The HTTP method used when calling the associated resource.
        integration_http_method: The integration HTTP method, may be None.
        integration_type: The integration's input type.
        uri: The input's URI.
    """

    def __init__(self, account: str, region: str, rest_api_id: str, resource_id: str, request_http_method: RestApiMethod,
                 integration_http_method: RestApiMethod, integration_type: IntegrationType, uri: str):
        super().__init__(account, region, AwsServiceName.AWS_API_GATEWAY_INTEGRATION)
        self.rest_api_id: str = rest_api_id
        self.resource_id: str = resource_id
        self.request_http_method: RestApiMethod = request_http_method
        self.integration_http_method: RestApiMethod = integration_http_method
        self.integration_type: IntegrationType = integration_type
        self.uri: str = uri
        self.lambda_func_integration: Optional[LambdaFunction] = None

    def get_keys(self) -> List[str]:
        return [self.rest_api_id, self.resource_id, self.request_http_method]

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}apigateway/home?region={1}#/apis/{2}/resources/{3}/methods/{4}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.rest_api_id, self.resource_id, self.request_http_method.name)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'request_http_method': self.request_http_method.value,
                'integration_http_method': self.integration_http_method and self.integration_http_method.value,
                'integration_type': self.integration_type}
