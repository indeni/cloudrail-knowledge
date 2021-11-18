from typing import List, Optional

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_configuration import LaunchConfiguration
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_log_group import CloudWatchLogGroup
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import AssociatePublicIpAddress, Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.elastic_ip import ElasticIp
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_rule import NetworkAclRule, RuleAction, RuleType
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import ConnectionType, SecurityGroupRule, SecurityGroupRulePropertyType
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpointInterface
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer, LoadBalancerSchemeType, LoadBalancerType
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target import LoadBalancerTarget
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group import LoadBalancerTargetGroup
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.arn_utils import get_arn_resource
from cloudrail.knowledge.utils.utils import create_pseudo_id

from cloudrail.knowledge.context.aws.predefind_components import get_readonly_policy
from cloudrail.knowledge.context.aws.resources_assigner_util import ResourcesAssignerUtil
from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator


class PseudoBuilder:
    def __init__(self, merged_ctx: AwsEnvironmentContext):
        self.ctx = merged_ctx

    # Creating ReadOnlyAccess policy, as it is always placed in AWS, but the API will not fetch it unless used.
    # Required in order to evaluate TF templates which use it first time in the account.
    # If we run the evaluation with no-cloud-account flag, we will not have account to iterate over, which in that case we will create it anyway.
    def create_missing_policies(self):
        if self.ctx.accounts:
            for account in self.ctx.accounts:
                if not any(policy.arn == 'arn:aws:iam::aws:policy/ReadOnlyAccess' and policy.account == account.account
                           for policy in self.ctx.policies):
                    self.ctx.policies.append(get_readonly_policy(account.account))
        else:
            self.ctx.policies.append(get_readonly_policy(None))

    def create_main_route_table(self, vpc_id: str, account: str, region: str) -> RouteTable:
        route_table_id = create_pseudo_id('rt')
        route_table = RouteTable(route_table_id=route_table_id,
                                 vpc_id=vpc_id,
                                 name=route_table_id,
                                 region=region,
                                 account=account,
                                 is_main_route_table=True).with_aliases(route_table_id)
        route_table.is_pseudo = True
        self.ctx.route_tables.update(route_table)
        return route_table

    def create_security_group(self, vpc: Vpc, is_default: bool, account: str, region: str) -> SecurityGroup:
        security_group_id = create_pseudo_id('sg')
        has_description = True
        pseudo_inbound_security_group_rule = SecurityGroupRule(0, 65535, IpProtocol('ALL'), SecurityGroupRulePropertyType.SECURITY_GROUP_ID,
                                                               security_group_id, has_description, ConnectionType.INBOUND,
                                                               security_group_id, region, account)
        pseudo_inbound_security_group_rule.is_pseudo = True
        pseudo_outbound_security_group_rule_ipv4 = SecurityGroupRule(0, 65535, IpProtocol('ALL'),
                                                                     SecurityGroupRulePropertyType.IP_RANGES, '0.0.0.0/0', has_description,
                                                                     ConnectionType.OUTBOUND, security_group_id, region, account)
        pseudo_outbound_security_group_rule_ipv4.is_pseudo = True
        pseudo_outbound_security_group_rule_ipv6 = SecurityGroupRule(0, 65535, IpProtocol('ALL'),
                                                                     SecurityGroupRulePropertyType.IP_RANGES, '::/0', has_description,
                                                                     ConnectionType.OUTBOUND, security_group_id, region, account)
        pseudo_outbound_security_group_rule_ipv6.is_pseudo = True
        self.ctx.security_group_rules.append(pseudo_inbound_security_group_rule)
        self.ctx.security_group_rules.append(pseudo_outbound_security_group_rule_ipv4)
        self.ctx.security_group_rules.append(pseudo_outbound_security_group_rule_ipv6)
        security_group = SecurityGroup(security_group_id=security_group_id,
                                       region=vpc.region,
                                       name=security_group_id,
                                       vpc_id=vpc.vpc_id,
                                       is_default=is_default,
                                       account=account,
                                       has_description=True)
        security_group.is_pseudo = True
        self.ctx.security_groups.update(security_group)
        return security_group

    def create_security_group_from_rules_list(self, vpc: Vpc, is_default: bool, account: str, region: str, inbound_rules_list: Optional[List[dict]],
                                              outbound_rules_list_ipv4: Optional[List[dict]], outbound_rules_list_ipv6: Optional[List[dict]],
                                              has_description: bool) -> SecurityGroup:
        security_group_id = create_pseudo_id('sg')
        security_group = SecurityGroup(security_group_id=security_group_id, region=vpc.region, name=security_group_id, vpc_id=vpc.vpc_id,
                                       is_default=is_default, account=account, has_description=True)
        if inbound_rules_list:
            pseudo_inbound_rules: List[SecurityGroupRule] = []
            for rule in inbound_rules_list:
                pseudo_inbound_security_group_rule = SecurityGroupRule(rule['from_port'], rule['to_port'], IpProtocol(rule['ip_protocol']),
                                                                       rule['property_type'], security_group_id, has_description,
                                                                       ConnectionType.INBOUND, security_group_id, region, account)
                pseudo_inbound_security_group_rule.is_pseudo = True
                pseudo_inbound_rules.append(pseudo_inbound_security_group_rule)
            self.ctx.security_group_rules.extend(pseudo_inbound_rules)
            security_group.inbound_permissions.extend(pseudo_inbound_rules)
        if outbound_rules_list_ipv4:
            pseudo_outbound_ipv4_rules: List[SecurityGroupRule] = []
            for rule in outbound_rules_list_ipv4:
                pseudo_outbound_security_group_rule_ipv4 = SecurityGroupRule(rule['from_port'], rule['to_port'], IpProtocol(rule['ip_protocol']),
                                                                             rule['property_type'], rule['property_value'], has_description,
                                                                             ConnectionType.OUTBOUND, security_group_id, region, account)
                pseudo_outbound_security_group_rule_ipv4.is_pseudo = True
                pseudo_outbound_ipv4_rules.append(pseudo_outbound_security_group_rule_ipv4)
            self.ctx.security_group_rules.extend(pseudo_outbound_ipv4_rules)
            security_group.outbound_permissions.extend(pseudo_outbound_ipv4_rules)
        if outbound_rules_list_ipv6:
            pseudo_outbound_ipv6_rules: List[SecurityGroupRule] = []
            for rule in outbound_rules_list_ipv6:
                pseudo_outbound_security_group_rule_ipv6 = SecurityGroupRule(rule['from_port'], rule['to_port'], IpProtocol(rule['ip_protocol']),
                                                                             rule['property_type'], rule['property_value'], has_description,
                                                                             ConnectionType.OUTBOUND, security_group_id, region, account)
                pseudo_outbound_security_group_rule_ipv6.is_pseudo = True
                pseudo_outbound_ipv6_rules.append(pseudo_outbound_security_group_rule_ipv6)
            self.ctx.security_group_rules.extend(pseudo_outbound_ipv6_rules)
            security_group.outbound_permissions.extend(pseudo_outbound_ipv6_rules)
        security_group.is_pseudo = True
        self.ctx.security_groups.update(security_group)
        return security_group

    def create_ec2_network_interface(self, ec2: Ec2Instance, subnets: AliasesDict[Subnet], vpcs: AliasesDict[Vpc],
                                     launch_configuration: LaunchConfiguration = None):
        if not ec2.raw_data.subnet_id:
            default_vpc = ResourceInvalidator.get_by_logic(
                lambda: ResourcesAssignerUtil.get_default_vpc(vpcs, ec2.account, ec2.region),
                True,
                ec2,
                f'Could not find default vpc in region {ec2.region}'
            )
            subnet = ResourceInvalidator.get_by_logic(
                lambda: next((subnet for subnet in subnets if subnet.vpc_id == default_vpc.vpc_id), None),
                True,
                ec2,
                f'Could not find a subnet in the default vpc {default_vpc.vpc_id}'
            )
        else:
            subnet = ResourceInvalidator.get_by_id(subnets, ec2.raw_data.subnet_id, True, ec2)

        eni_id = create_pseudo_id('eni')
        private_ip_address = ec2.raw_data.private_ip_address or subnet.cidr_block.split('/')[0]
        public_ip_address = ec2.raw_data.public_ip_address

        should_associate_public_ip = (launch_configuration and launch_configuration.associate_public_ip_address) or \
                                     ec2.raw_data.associate_public_ip_address == AssociatePublicIpAddress.YES or \
                                     (ec2.raw_data.associate_public_ip_address == AssociatePublicIpAddress.USE_SUBNET_SETTINGS and
                                      subnet.map_public_ip_on_launch)

        if not public_ip_address and should_associate_public_ip:
            public_ip_address = '0.0.0.0'

        pseudo_eni = NetworkInterface(eni_id, subnet.subnet_id, private_ip_address, [],
                                      public_ip_address, ec2.raw_data.ipv6_addresses, ec2.raw_data.security_groups_ids, '', True,
                                      subnet.availability_zone, subnet.account, subnet.region)
        pseudo_eni.subnet = subnet
        pseudo_eni.is_pseudo = True
        self.ctx.network_interfaces.update(pseudo_eni)
        ec2.network_interfaces_ids = [pseudo_eni.eni_id]
        pseudo_eni.owner = ec2
        ec2.network_resource.add_interface(pseudo_eni)

    def create_vpc_endpoint_network_interface(self, vpc_endpoint: VpcEndpointInterface):
        for subnet_id in vpc_endpoint.subnet_ids:
            subnet = ResourceInvalidator.get_by_id(self.ctx.subnets, subnet_id, True, vpc_endpoint)
            self.create_eni(vpc_endpoint, subnet, vpc_endpoint.security_group_ids, False, None, None, 'VPCE Eni', False)

    def create_ec2(self, subnet: Subnet, image_id: str, security_groups_ids: List[str], instance_type: str, monitoring: bool, ebs_optimized: bool,
                   name: str, iam_instance_profile: str, tags: dict, assign_public_ip: Optional[bool]) -> Ec2Instance:
        private_ip = subnet.cidr_block.split('/')[0]
        public_ip = "0.0.0.0" if assign_public_ip else None
        pseudo_ec2 = Ec2Instance(
            account=subnet.vpc.account,
            region=subnet.region,
            instance_id=create_pseudo_id('ec2'),
            name=name,
            network_interfaces_ids=[],
            state='running',
            image_id=image_id,
            iam_profile_name=iam_instance_profile,
            http_tokens='optional',
            availability_zone=subnet.availability_zone,
            tags=tags,
            instance_type=instance_type,
            ebs_optimized=ebs_optimized,
            monitoring_enabled=monitoring
        ).with_raw_data(
            subnet_id=subnet.subnet_id,
            private_ip_address=private_ip,
            public_ip_address=public_ip,
            security_groups_ids=security_groups_ids)
        pseudo_ec2.is_pseudo = True
        self.ctx.ec2s.append(pseudo_ec2)
        return pseudo_ec2

    def create_load_balancer_targets_from_ec2s(self, target_groups: List[LoadBalancerTargetGroup], ec2s: List[Ec2Instance]) -> None:
        for ec2 in ec2s:
            for target_group in target_groups:
                target = LoadBalancerTarget(target_group_arn=target_group.target_group_arn,
                                            target_id=ec2.instance_id,
                                            port=target_group.port,
                                            account=target_group.account,
                                            region=target_group.region)
                target.is_pseudo = True
                self.ctx.load_balancer_targets.append(target)

    def create_default_nacl(self, vpc_id: str, account: str, region: str) -> NetworkAcl:
        network_acl_id = create_pseudo_id('nacl')
        nacl = NetworkAcl(network_acl_id=network_acl_id,
                          vpc_id=vpc_id,
                          is_default=True,
                          name=network_acl_id,
                          subnet_ids=[],
                          region=region,
                          account=account)
        nacl.is_pseudo = True
        pseudo_inbound_rule = NetworkAclRule(region, account, network_acl_id, '0.0.0.0/0',
                                             0, 65535, RuleAction.ALLOW, 100, RuleType.INBOUND)
        pseudo_inbound_rule.is_pseudo = True
        pseudo_outbound_rule = NetworkAclRule(region, account, network_acl_id, '0.0.0.0/0',
                                              0, 65535, RuleAction.ALLOW, 100, RuleType.OUTBOUND)
        pseudo_outbound_rule.is_pseudo = True
        self.ctx.network_acl_rules.append(pseudo_inbound_rule)
        self.ctx.network_acl_rules.append(pseudo_outbound_rule)
        self.ctx.network_acls.update(nacl)
        return nacl

    def create_load_balancer_network_interfaces(self, load_balancer: LoadBalancer, subnets: AliasesDict[Subnet],
                                                elastic_ips: List[ElasticIp]) -> None:
        def _create_eni(subnet: Subnet, private_ip, public_ip):
            eni_id = create_pseudo_id('eni')
            description = f'ELB {get_arn_resource(load_balancer.load_balancer_arn)}'
            pseudo_eni = NetworkInterface(eni_id, subnet.subnet_id, private_ip, [], public_ip, [],
                                          [] if load_balancer.load_balancer_type == LoadBalancerType.NETWORK
                                          else load_balancer.raw_data.security_groups_ids,
                                          description, True, subnet.availability_zone, subnet.account, subnet.region)
            pseudo_eni.subnet = subnet
            pseudo_eni.is_pseudo = True
            pseudo_eni.owner = load_balancer
            self.ctx.network_interfaces.update(pseudo_eni)
            load_balancer.network_resource.add_interface(pseudo_eni)

        for subnet_id in (subnet_id for subnet_id in load_balancer.raw_data.subnets_ids
                          if subnet_id not in load_balancer.network_resource.subnet_ids):
            subnet = ResourceInvalidator.get_by_id(subnets, subnet_id, True, load_balancer)
            private_ip = subnet.cidr_block.split('/')[0]  # First IP in Subnet
            public_ip = "0.0.0.0" if load_balancer.scheme_type == LoadBalancerSchemeType.INTERNET_FACING else None
            _create_eni(subnet, private_ip, public_ip)

        for subnet_mapping in load_balancer.raw_data.subnet_mapping:
            subnet = ResourceInvalidator.get_by_id(subnets, subnet_mapping.subnet_id, True, load_balancer)
            if subnet_mapping.allocation_id \
                and (elastic_ip := next((eip for eip in elastic_ips if eip.allocation_id == subnet_mapping.allocation_id), None)):
                private_ip = elastic_ip.private_ip or subnet_mapping.private_ipv4_address or subnet.cidr_block.split('/')[0]  # First IP in Subnet
                public_ip = elastic_ip.public_ip or "0.0.0.0"
            else:
                private_ip = subnet_mapping.private_ipv4_address or subnet.cidr_block.split('/')[0]  # First IP in Subnet
                public_ip = "0.0.0.0" if load_balancer.scheme_type == LoadBalancerSchemeType.INTERNET_FACING else None

            _create_eni(subnet, private_ip, public_ip)

    def create_eni(self, entity: NetworkEntity, subnet: Subnet, security_group_ids: List[str], assign_public_ip: bool,
                   private_ip: Optional[str], public_ip: Optional[str], description: str, assign_default_security_group: bool = True) -> None:
        eni: NetworkInterface = NetworkInterface(eni_id=create_pseudo_id('eni'),
                                                 subnet_id=subnet.subnet_id,
                                                 primary_ip_address=private_ip or ResourcesAssignerUtil.get_random_ip_in_subnet(subnet.cidr_block),
                                                 secondary_ip_addresses=[],
                                                 public_ip_address=public_ip or "0.0.0.0" if assign_public_ip else None,
                                                 ipv6_ip_addresses=[],
                                                 security_groups_ids=[],
                                                 description=description,
                                                 is_primary=True,
                                                 availability_zone=subnet.availability_zone,
                                                 account=subnet.account,
                                                 region=subnet.region)
        eni.is_pseudo = True
        eni.subnet = subnet
        self.ctx.network_interfaces.update(eni)

        eni.owner = entity
        if security_group_ids:
            eni.security_groups_ids = security_group_ids
            for sg_id in security_group_ids:
                if self.ctx.security_groups.get(sg_id):
                    eni.security_groups.append(self.ctx.security_groups[sg_id])
        elif assign_default_security_group:
            eni.security_groups.append(subnet.vpc.default_security_group)
        entity.network_resource.add_interface(eni)

        for security_group in eni.security_groups:
            security_group.add_usage(eni)

    def create_kms_key(self, key_id: str, arn: str, region: str, account: str) -> KmsKey:
        kms_key = KmsKey(key_id=key_id,
                         arn=arn,
                         key_manager=KeyManager.AWS,
                         region=region,
                         account=account)
        kms_key.is_pseudo = True
        self.ctx.kms_keys.append(kms_key)
        return kms_key

    def create_cloudwatch_log_group_for_lambda(self, lambda_functions: List[LambdaFunction]):
        for lambda_func in lambda_functions:
            if not any(lambda_func.function_name == cloudwatch_log_group.name.replace('/aws/lambda/', '')
                       for cloudwatch_log_group in self.ctx.cloud_watch_log_groups):
                pseudo_arn = create_pseudo_id(lambda_func.function_name)
                cloudwatch_log_group = CloudWatchLogGroup(f'/aws/lambda/{lambda_func.function_name}', None,
                                                          f'arn:aws:logs:{lambda_func.region}:{lambda_func.account}:'
                                                          f'log-group:/aws/resource/pseudo-{pseudo_arn}:*',
                                                          0, lambda_func.region, lambda_func.account)
                cloudwatch_log_group.is_pseudo = True
                self.ctx.cloud_watch_log_groups.append(cloudwatch_log_group)
