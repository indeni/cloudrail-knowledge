from typing import Dict

from cloudrail.knowledge.context.aws.resources.ec2.nat_gateways import NatGateways
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.utils import generate_random_public_ipv4


class CloudformationNatGatewayBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.NAT_GW, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> NatGateways:
        properties: dict = cfn_res_attr['Properties']
        allocation_id = self.get_property(properties, 'AllocationId')
        subnet_id = self.get_property(properties, 'SubnetId')
        # we are generating random public ip because the public ip is the name of nat gateway resource.
        # we will replace the real public ip value in '_update_object_properties' function
        public_ip = generate_random_public_ipv4()
        return NatGateways(nat_gateway_id=self.get_resource_id(cfn_res_attr), allocation_id=allocation_id,
                           subnet_id=subnet_id, eni_id=None,
                           private_ip=None, public_ip=public_ip,
                           account=cfn_res_attr['account_id'], region=cfn_res_attr['region'])
