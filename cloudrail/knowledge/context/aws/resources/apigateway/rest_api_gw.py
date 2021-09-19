from enum import Enum
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_stage import ApiGatewayStage
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_domain import RestApiGwDomain
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_policy import RestApiGwPolicy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName, AwsServiceType, AwsServiceAttributes
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import ApiGatewayMethodSettings


class ApiGatewayType(Enum):
    EDGE = 'EDGE'
    REGIONAL = 'REGIONAL'
    PRIVATE = 'PRIVATE'


class RestApiGw(AwsResource):
    """
    Attributes:
        rest_api_gw_id: The ID of the REST API Gateway.
        api_gw_name: The name of the API gateway.
        api_gateway_type: One of EDGE, REGIONAL, PRIVATE.
        is_public: An indication on if this resource is accessible from the internet.
        api_gateway_methods: All the ApiGatewayMethods associated with this gateway.
        api_gw_stages: The stages associated with this REST API Gateway.
        agw_methods_with_valid_integrations_and_allowed_lambda_access: The ApiGatewayMethods associated with this gateway, with valid integrations, and are allowed to access a lambda function.
    """
    def __init__(self,
                 rest_api_gw_id: str,
                 api_gw_name: str,
                 region: str,
                 account: str, api_gateway_type: ApiGatewayType):
        super().__init__(account, region, AwsServiceName.AWS_REST_API_GW,
                         AwsServiceAttributes(aws_service_type=AwsServiceType.APIGATEWAY.value, region=region))
        self.rest_api_gw_id: str = rest_api_gw_id
        self.api_gw_name: str = api_gw_name
        self.api_gateway_type: ApiGatewayType = api_gateway_type
        self.method_settings: Optional[ApiGatewayMethodSettings] = None
        self.domain: Optional[RestApiGwDomain] = None
        self.api_gw_stages: List[ApiGatewayStage] = []
        self.is_public: bool = None
        self.api_gateway_methods: List[ApiGatewayMethod] = []
        self.agw_methods_with_valid_integrations_and_allowed_lambda_access: List[ApiGatewayMethod] = []
        self.resource_based_policy: RestApiGwPolicy = None

    def get_keys(self) -> List[str]:
        return [self.rest_api_gw_id]

    def get_id(self) -> str:
        return self.rest_api_gw_id

    def assign_policy_data_for_tf(self,
                                  policy_statements: List[PolicyStatement],
                                  raw_document: str,
                                  rest_api_gw_id: str) -> RestApiGwPolicy:
        self.resource_based_policy = RestApiGwPolicy(rest_api_gw_id, policy_statements, raw_document, self.account)
        return self.resource_based_policy

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API Gateway'
        else:
            return 'API Gateways'

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}apigateway/home?region={1}#/apis/{2}/resources/'\
            .format(self.AWS_CONSOLE_URL, self.region, self.rest_api_gw_id)

    @property
    def is_tagable(self) -> bool:
        return True
