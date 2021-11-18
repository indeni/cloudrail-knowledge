from enum import Enum
from typing import List
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName, AwsServiceAttributes
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.utils.tags_utils import filter_tags


class VpcEndpointServiceType(Enum):
    S3 = 's3'
    UNSUPPORTED = 'unsupported'


class VpcEndpoint(AwsResource):

    def __init__(self, region: str, account: str, vpce_id: str, vpc_id: str,
                 service_name: str, state: str, policy: Policy):
        AwsResource.__init__(self, account, region, AwsServiceName.AWS_VPC_ENDPOINT,
                             AwsServiceAttributes(aws_service_type=AwsServiceAttributes.parse_service_name(service_name), region=region))
        self.vpce_id: str = vpce_id
        self.vpc_id: str = vpc_id
        self.service_name: str = service_name
        self.state: str = state
        self.policy: Policy = policy

    def get_keys(self) -> List[str]:
        return [self.vpce_id]

    def get_extra_data(self) -> str:
        vpc_id = 'vpc_id: {}'.format(self.vpc_id) if self.vpc_id else ''
        service_name = 'service_name: {}'.format(self.service_name) if self.service_name else ''
        state = 'state: {}'.format(self.state) if self.state else ''
        return ', '.join([vpc_id, service_name, state])

    def get_id(self) -> str:
        return self.vpce_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'VPC Endpoint'
        else:
            return 'VPC Endpoints'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#Endpoints:vpcEndpointId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.vpce_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags), 'vpc_id': self.vpc_id,
                'service_name': self.service_name}


class VpcEndpointGateway(VpcEndpoint):

    def __init__(self, vpce_id: str, account: str, region: str, vpc_id: str, service_name: str, state: str, policy: Policy,
                 route_table_ids: List[str] = None):
        super().__init__(vpce_id=vpce_id, account=account, region=region,
                         vpc_id=vpc_id, service_name=service_name, state=state, policy=policy)
        self.route_table_ids: List[str] = route_table_ids or []
        self.route_tables: List[RouteTable] = []

    def get_type(self, is_plural: bool = False) -> str:
        return super().get_type(is_plural) + ' Gateway'

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags), 'vpce_id': self.vpce_id,
                'vpc_id': self.vpc_id,
                'service_name': self.service_name,
                'route_table_ids': self.route_table_ids}


class VpcEndpointInterface(VpcEndpoint, NetworkEntity):

    def __init__(self, vpce_id: str, account: str, region: str, vpc_id: str, service_name: str,
                 state: str, policy: Policy, subnet_ids: List[str] = None,
                 security_group_ids: List[str] = None, network_interface_ids: List[str] = None):
        VpcEndpoint.__init__(self, vpce_id=vpce_id, account=account, region=region,
                             vpc_id=vpc_id, service_name=service_name, state=state, policy=policy)
        NetworkEntity.__init__(self, name=vpce_id, account=account, region=region,
                               tf_resource_type=AwsServiceName.AWS_VPC_ENDPOINT,
                               aws_service_attributes=AwsServiceAttributes(aws_service_type=AwsServiceAttributes.parse_service_name(service_name),
                                                                           region=region))
        self.account: str = account
        self.region: str = region
        self.subnet_ids: List[str] = subnet_ids or []
        self.security_group_ids: List[str] = security_group_ids or []
        self.network_interface_ids: List[str] = network_interface_ids or []

    def get_type(self, is_plural: bool = False) -> str:
        return super().get_type(is_plural) + ' Interface'

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags), 'vpce_id': self.vpce_id,
                'vpc_id': self.vpc_id,
                'service_name': self.service_name,
                'subnet_ids': self.subnet_ids,
                'security_group_ids': self.security_group_ids,
                'network_interface_ids': self.network_interface_ids}
