from typing import List, Optional
from dataclasses import dataclass

from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import ApiGatewayMethodSettings
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


@dataclass
class AccessLogsSettings:
    """
        Attributes:
            destination_arn: The ARN of either Cloudwatch log group or Kinesis Data Firehose delivery stream to receive the access logs.
            format: The formatting and values recorded in the logs.
    """
    destination_arn: str
    format: str


class ApiGatewayStage(AwsResource):
    """
        Attributes:
            api_gw_id: The ID of the REST API Gateway.
            stage_name: The name of the stage.
            xray_tracing_enabled: An indication if active tracing with X-ray is enabled.
            access_logs: Block information about the access logs settings of the REST API Gateway stage (if any configured).
            method_settings: The method settings configured for this stage, if configured.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 api_gw_id: str,
                 stage_name: str,
                 xray_tracing_enabled: bool,
                 access_logs: Optional[AccessLogsSettings]):
        super().__init__(account, region, AwsServiceName.AWS_API_GATEWAY_STAGE)
        self.api_gw_id: str = api_gw_id
        self.stage_name: str = stage_name
        self.xray_tracing_enabled: bool = xray_tracing_enabled
        self.access_logs: Optional[AccessLogsSettings] = access_logs
        self.method_settings: Optional[ApiGatewayMethodSettings] = None

    def get_keys(self) -> List[str]:
        if self.method_settings:
            return [self.api_gw_id, 'with_method_settings']
        else:
            return [self.api_gw_id]

    def get_id(self) -> str:
        return self.api_gw_id

    def get_name(self) -> str:
        return self.stage_name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API stage'
        else:
            return 'API stages'

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}apigateway/home?region={1}#/apis/{2}/stages/{3}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.api_gw_id, self.stage_name)

    @property
    def is_tagable(self) -> bool:
        return True
