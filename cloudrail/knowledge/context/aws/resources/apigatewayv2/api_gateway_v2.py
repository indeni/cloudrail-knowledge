from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2_integration import ApiGatewayV2Integration
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2_vpc_link import ApiGatewayVpcLink
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ApiGateway(NetworkEntity):
    """
    Attributes:
        account: The account ID in which this resource operates.
        region: The region name in which this resource operates.
        api_gw_id: The API GW ID.
        arn: The ARN of the API GW.
        api_gw_name: The API GW name.
        protocol_type: The protocol type of the API GW.
        api_gw_integration: A reference to the matching ApiGatewayV2Integration based on api_gw_id.
        vpc_link: A reference to the matching ApiGatewayVpcLink based on api_gw_id.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 api_gw_id: str,
                 api_gw_name: str,
                 protocol_type: str,
                 arn: Optional[str]):
        super().__init__(api_gw_name, account, region, AwsServiceName.AWS_REST_API_GW)
        self.api_gw_id: str = api_gw_id
        self.api_gw_name: str = api_gw_name
        self.protocol_type: str = protocol_type
        self.api_endpoint: str = f'{protocol_type}://{api_gw_id}.execute-api.{region}.amazonaws.com'
        self.with_aliases(api_gw_id)
        self.arn: Optional[str] = arn if arn else self._create_arn()
        self.api_gw_integration: ApiGatewayV2Integration = None
        self.vpc_link: ApiGatewayVpcLink = None

    def get_keys(self) -> List[str]:
        return [self.api_gw_id]

    def get_id(self) -> str:
        return self.api_gw_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API Gateway'
        else:
            return 'API Gateways'

    def _create_arn(self) -> Optional[str]:
        if self.api_gw_id:
            return f'arn:aws:apigateway:{self.region}::/apis/{self.api_gw_id}'
        else:
            return None

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> str:
        return '{0}apigateway/main/api-detail/?api={1}&region={2}'\
            .format(self.AWS_CONSOLE_URL, self.api_gw_id, self.region)

    def get_all_network_configurations(self) -> Optional[List[NetworkConfiguration]]:
        if self.vpc_link:
            return [NetworkConfiguration(False,
                                         self.vpc_link.security_group_ids,
                                         self.vpc_link.subnet_ids)]
        else:
            return []

    @property
    def is_tagable(self) -> bool:
        return True
