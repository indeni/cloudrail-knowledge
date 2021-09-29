from typing import Dict
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer, LoadBalancerSchemeType, LoadBalancerType, LoadBalancerRawData, \
    LoadBalancerSubnetMapping
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLoadBalancerBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ELASTIC_LOAD_BALANCER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> LoadBalancer:
        properties: dict = cfn_res_attr['Properties']
        scheme: LoadBalancerSchemeType = LoadBalancerSchemeType.INTERNAL if self.get_property(properties, 'Scheme') == 'internal' else \
            LoadBalancerSchemeType.INTERNET_FACING

        elb_type = self.get_property(properties, 'Type')
        elb_type = LoadBalancerType(elb_type) if elb_type else LoadBalancerType.APPLICATION
        arn = self.get_resource_id(cfn_res_attr)

        lb = LoadBalancer(account=cfn_res_attr['account_id'],
                          name=self.get_property(properties, 'Name'),
                          region=cfn_res_attr['region'],
                          scheme_type=scheme,
                          load_balancer_type=elb_type,
                          load_balancer_arn=arn) \
            .with_aliases(arn)
        subnets_ids = self.get_property(properties, 'Subnets')
        security_groups_ids = self.get_property(properties, 'SecurityGroups')
        subnet_mapping = [LoadBalancerSubnetMapping(x.get('AllocationId'),
                                                    x.get('PrivateIPv4Address'),
                                                    x.get('SubnetId'))
                          for x in self.get_property(properties, 'SubnetMappings', [])]
        lb.raw_data = LoadBalancerRawData(subnets_ids or [], security_groups_ids or [], subnet_mapping or [])

        return lb
