from typing import List
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName, AwsServiceType, AwsServiceAttributes
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class RestApiGwMapping(AwsResource):
    """
        Attributes:
            api_id: The ID of the REST API Gateway.
            domain_name: The name of the domain.
    """

    def __init__(self,
                 api_id: str,
                 domain_name: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_API_GATEWAY_BASE_PATH_MAPPING,
                         AwsServiceAttributes(aws_service_type=AwsServiceType.APIGATEWAY.value, region=region))
        self.api_id: str = api_id
        self.domain_name: str = domain_name

    def get_keys(self) -> List[str]:
        return [self.api_id]

    def get_id(self) -> str:
        return self.api_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API mapping'
        else:
            return 'API mappings'

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}apigateway/home?region={1}#/apis/{2}/resources/'\
            .format(self.AWS_CONSOLE_URL, self.region, self.api_id)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'domain_name': self.domain_name}
