from typing import Dict

from cloudrail.knowledge.context.aws.resources.ec2.elastic_ip import ElasticIp

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationElasticIpBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ELASTIC_IP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> ElasticIp:
        properties: dict = cfn_res_attr['Properties']
        return ElasticIp(
            allocation_id=None,
            public_ip=self.get_property(properties, 'PublicIpv4Pool', self.get_resource_id(cfn_res_attr)),
            private_ip=None,
            account=cfn_res_attr['account_id'],
            region=cfn_res_attr['region'])
