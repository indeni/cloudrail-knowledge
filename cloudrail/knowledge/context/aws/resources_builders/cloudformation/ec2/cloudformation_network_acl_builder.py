from typing import Dict
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_rule import NetworkAclRule
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import _build_network_acl_rule
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_association import NetworkAclAssociation
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationNetworkAclBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.NETWORK_ACL, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> NetworkAcl:
        properties: dict = cfn_res_attr['Properties']
        network_acl_id = self.get_resource_id(cfn_res_attr)
        vpc_id = self.get_property(properties, 'VpcId')
        name = self.get_name_tag(properties)
        return NetworkAcl(network_acl_id, vpc_id, False, name, None, cfn_res_attr['region'], cfn_res_attr['account_id'])


class CloudformationNetworkAclAssociationBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.SUBNET_NETWORK_ACL_ASSOCIATION, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> NetworkAclAssociation:
        properties: dict = cfn_res_attr['Properties']
        network_acl_id = self.get_property(properties, 'NetworkAclId')
        subnet_id = self.get_property(properties, 'SubnetId')
        network_acl_association_id = self.get_resource_id(cfn_res_attr)
        return NetworkAclAssociation(network_acl_id, subnet_id, network_acl_association_id, cfn_res_attr['region'], cfn_res_attr['account_id'])


class NetworkAclRuleBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.NETWORK_ACL_ENTRY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> NetworkAclRule:
        properties: dict = cfn_res_attr['Properties']
        network_acl_id = self.get_property(properties, 'NetworkAclId')
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        return _build_network_acl_rule(properties, network_acl_id, region, account)
