from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class VpcEndpointRouteTableAssociation(AwsResource):

    def __init__(self, route_table_id: str, vpc_endpoint_id: str, region: str, account: str):
        super().__init__(account, region, AwsServiceName.NONE)
        self.route_table_id: str = route_table_id
        self.vpc_endpoint_id: str = vpc_endpoint_id

    def get_keys(self) -> List[str]:
        return [self.route_table_id, self.vpc_endpoint_id]

    def get_type(self, is_plural: bool = False) -> str:
        return 'VPC Endpoint Route Table Associations'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#Endpoints:vpcEndpointId={2};sort=vpcEndpointId'\
            .format(self.AWS_CONSOLE_URL, self.region, self.vpc_endpoint_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'route_table_id': self.route_table_id,
                'vpc_endpoint_id': self.vpc_endpoint_id}
