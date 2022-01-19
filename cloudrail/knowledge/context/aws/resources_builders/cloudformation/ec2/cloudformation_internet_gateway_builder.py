from abc import abstractmethod
from typing import Dict
from cloudrail.knowledge.context.aws.resources.ec2.igw_type import IgwType
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class InternetGatewayBuilder(BaseCloudformationBuilder):

    def parse_resource(self, cfn_res_attr: dict) -> InternetGateway:
        return InternetGateway(vpc_id=cfn_res_attr['Properties'].get('VpcId'),
                               igw_id=self.get_resource_id(cfn_res_attr),
                               igw_type=self.get_igw_type(),
                               region=cfn_res_attr['region'],
                               account=cfn_res_attr['account_id'])

    @abstractmethod
    def get_igw_type(self):
        pass


class CloudformationInternetGatewayBuilder(InternetGatewayBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.INTERNET_GATEWAY, cfn_by_type_map)

    def get_igw_type(self):
        return IgwType.IGW


class CloudformationEgressOnlyInternetGatewayBuilder(InternetGatewayBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.EGRESS_ONLY_INTERNET_GATEWAY, cfn_by_type_map)

    def get_igw_type(self):
        return IgwType.EGRESS_ONLY_IGW
