from typing import Dict

from cloudrail.knowledge.context.aws.resources.ec2.elastic_ip import ElasticIp

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationElasticIpBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ELASTIC_IP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> ElasticIp:
        properties: dict = cfn_res_attr['Properties']
        allocation_id = self.get_resource_id(cfn_res_attr) if self.is_physical_id_exist(cfn_res_attr) else f'{self.get_resource_id(cfn_res_attr)}.AllocationId'
        return ElasticIp(
            # see !GetAtt: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip.html
            allocation_id=allocation_id,
            public_ip=self.get_property(properties, 'PublicIpv4Pool'),
            private_ip=None,
            account=cfn_res_attr['account_id'],
            region=cfn_res_attr['region'])
