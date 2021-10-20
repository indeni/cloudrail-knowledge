from typing import Optional, List

from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import IntegrationType
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import RestApiMethod
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ApiGatewayV2Integration(AwsResource):
    """
    Attributes:
        account: The account ID in which this resource operates.
        region: The region name in which this resource operates.
        rest_api_id: The API GW ID.
        connection_id: The ID of the VPC link used by the API GW.
        integration_id: The ID of the integration used by the API GW.
        integration_http_method: API GW method used by the API GW.
        integration_type: The API GW integration type.
        uri: The input's URI.
    """

    def __init__(self, account: str, region: str, rest_api_id: str, connection_id: Optional[str], integration_id: str,
                 integration_http_method: RestApiMethod, integration_type: IntegrationType, uri: str):
        super().__init__(account, region, AwsServiceName.AWS_APIGATEWAYV_2_INTEGRATION)
        self.rest_api_id: str = rest_api_id
        self.connection_id: Optional[str] = connection_id
        self.integration_http_method: RestApiMethod = integration_http_method
        self.integration_type: IntegrationType = integration_type
        self.uri: str = uri
        self.integration_id: str = integration_id
        self.with_aliases(integration_id)

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.integration_id]

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}apigateway/main/develop/integrations/attach?api={1}&region={2}'\
            .format(self.AWS_CONSOLE_URL, self.rest_api_id, self.region)

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API Gateway integration'
        else:
            return 'API Gateway integrations'

    @property
    def is_tagable(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.integration_id

    def to_drift_detection_object(self) -> dict:
        return {'integration_http_method': self.integration_http_method.value,
                'integration_type': self.integration_type.value}
