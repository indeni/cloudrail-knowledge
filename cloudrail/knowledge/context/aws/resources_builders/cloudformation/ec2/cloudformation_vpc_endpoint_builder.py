from typing import Dict, List
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpointGateway, VpcEndpoint, VpcEndpointInterface
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import _build_policy
from cloudrail.knowledge.context.environment_context.common_component_builder import ALL_SERVICES_PUBLIC_FULL_ACCESS
from cloudrail.knowledge.utils.utils import safe_json_loads


class CloudformationVpcEndpointBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.VPC_ENDPOINT, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> VpcEndpoint:
        resource_properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        vpc_id = self.get_property(resource_properties, 'VpcId')
        service_name = self.get_property(resource_properties, 'ServiceName')
        vpce_id = self.get_resource_id(cfn_res_attr)
        policy: Policy
        if 'PolicyDocument' in resource_properties:
            policy = _build_policy(account, safe_json_loads(resource_properties['PolicyDocument']))
        else:
            full_access_statements: List[PolicyStatement] = [ALL_SERVICES_PUBLIC_FULL_ACCESS]
            policy = Policy(account, full_access_statements)

        if resource_properties['VpcEndpointType'] == 'Gateway':
            vpc_endpoint_gateway: VpcEndpointGateway = VpcEndpointGateway(region=region,
                                                                          vpc_id=vpc_id,
                                                                          account=account,
                                                                          service_name=service_name,
                                                                          state=None,
                                                                          policy=policy,
                                                                          vpce_id=vpce_id)
            vpc_endpoint_gateway.route_table_ids = self.get_property(resource_properties, 'RouteTableIds')
            return vpc_endpoint_gateway
        else:
            vpc_endpoint_interface: VpcEndpointInterface = VpcEndpointInterface(region=region,
                                                                                vpc_id=vpc_id,
                                                                                account=account,
                                                                                service_name=service_name,
                                                                                state=None,
                                                                                policy=policy,
                                                                                vpce_id=vpce_id)
            vpc_endpoint_interface.subnet_ids = self.get_property(resource_properties, 'SubnetIds', self.CFN_PSEUDO_LIST)
            vpc_endpoint_interface.security_group_ids = self.get_property(resource_properties, 'SecurityGroupIds', self.CFN_PSEUDO_LIST)
            vpc_endpoint_interface.network_interface_ids = self.get_property(resource_properties, 'NetworkInterfaceIds', self.CFN_PSEUDO_LIST)
            return vpc_endpoint_interface
