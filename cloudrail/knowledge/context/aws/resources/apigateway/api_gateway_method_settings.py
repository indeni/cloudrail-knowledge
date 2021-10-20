from typing import List
from enum import Enum
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class RestApiMethod(Enum):
    NONE = None
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    PUT = 'PUT'
    ANY = 'ANY'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'


class ApiGatewayMethodSettings(AwsResource):
    """
        Attributes:
            api_gw_id: The ID of the REST API Gateway.
            stage_name: The name of the stage.
            method_path: The method resource path.
            http_method: The actual HTTP method (GET, etc.).
            caching_enabled: Set to True if caching is enabled, False or None otherwise.
            caching_encrypted: Set to True or a KMS ARN is enabled, False or None otherwise.
    """

    def __init__(self,
                 api_gw_id: str,
                 stage_name: str,
                 method_path: str,
                 http_method: RestApiMethod,
                 caching_enabled: bool,
                 caching_encrypted: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_REST_API_GW_METHOD_SETTINGS)
        self.api_gw_id: str = api_gw_id
        self.stage_name: str = stage_name
        self.method_path: str = method_path
        self.http_method: RestApiMethod = http_method
        self.caching_enabled: bool = caching_enabled
        self.caching_encrypted: bool = caching_encrypted

    def get_keys(self) -> List[str]:
        return [self.api_gw_id, self.method_path]

    def get_id(self) -> str:
        return self.api_gw_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API method'
        else:
            return 'API methods'

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}apigateway/home?region={1}#/apis/{2}/resources/' \
            .format(self.AWS_CONSOLE_URL, self.region, self.api_gw_id)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'stage_name': self.stage_name,
                'method_path': self.method_path,
                'http_method': self.http_method.value,
                'caching_enabled': self.caching_enabled,
                'caching_encrypted': self.caching_encrypted}
