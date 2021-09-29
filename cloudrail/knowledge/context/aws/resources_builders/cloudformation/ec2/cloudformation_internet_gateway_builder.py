from typing import Dict
from cloudrail.knowledge.context.aws.resources.ec2.igw_type import IgwType
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationInternetGatewayBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.INTERNET_GATEWAY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> InternetGateway:
        return InternetGateway(vpc_id=None,  # first creating the igw and than attaching it to vpc
                               igw_id=self.get_resource_id(cfn_res_attr),
                               igw_type=IgwType.IGW,
                               region=cfn_res_attr['region'],
                               account=cfn_res_attr['account_id'])
