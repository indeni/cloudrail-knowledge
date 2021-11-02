import re
from typing import List, Optional, Set

from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.ip_protocol import IpProtocol

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.pseudo_builder import PseudoBuilder
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.ec2.main_route_table_association import MainRouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_rule import NetworkAclRule, RuleAction, RuleType
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.resourcegroupstaggingapi.resource_tag_mapping_list import ResourceTagMappingList
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, FunctionData, IterFunctionData
from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator


class AwsDefaultsRelationsAssigner(DependencyInvocation):

    def __init__(self, context: AwsEnvironmentContext):
        super().__init__(context=context)
        self.pseudo_builder = PseudoBuilder(context)
        _function_pool: List[FunctionData] = [
            # All Resources#
            IterFunctionData(self._assign_resources_tags, [resource for resource in context.get_all_non_iac_managed_resources()
                                                           if not resource.tags and resource.is_tagable and resource.get_arn()
                                                           and not isinstance(resource, ResourceTagMappingList)],
                             (context.resources_tagging_list,)),
            IterFunctionData(self._assign_vpc_default_and_main_route_tables, context.vpcs,
                             (context.route_tables, context.main_route_table_associations)),
            IterFunctionData(self._assign_vpc_default_security_group, context.vpcs, (context.security_groups,)),
            IterFunctionData(self._assign_vpc_default_nacl, context.vpcs, (context.network_acls,)),
            IterFunctionData(self._assign_default_network_acl_rules_for_tf, [nacl for nacl in context.network_acls if nacl.is_managed_by_iac],
                             (context.vpcs,)),
            IterFunctionData(self._assign_rds_cluster_default_security_group, context.rds_clusters, (),
                             [self._assign_vpc_default_security_group, self._assign_subnet_vpc])
        ]
        self.add_func_pool(_function_pool)

    def _assign_resources_tags(self, resource: AwsResource, tags_list: List[ResourceTagMappingList]):
        def get_tags_data():
            tags_data = next((tags.tags for tags in tags_list if self._are_arns_equal(tags.resource_arn, resource)), None)
            if tags_data:
                return tags_data
            else:
                return {}

        resource.tags = ResourceInvalidator.get_by_logic(get_tags_data, False)

    @staticmethod
    def _are_arns_equal(tags_arn: str, resource: AwsResource) -> bool:
        if isinstance(resource, LambdaFunction):
            lambda_arn = re.sub(r":[^:]+$", "", resource.arn)
            return tags_arn == lambda_arn
        else:
            return tags_arn == resource.get_arn()

    def _assign_vpc_default_and_main_route_tables(self,
                                                  vpc: Vpc,
                                                  route_tables: AliasesDict[RouteTable],
                                                  main_route_table_association: List[MainRouteTableAssociation]):

        def get_default_rt():
            if main_route_table_id := next((rta.route_table_id for rta in main_route_table_association if rta.vpc_id == vpc.vpc_id), None):
                return ResourceInvalidator.get_by_id(route_tables, main_route_table_id, True, vpc)
            if default_rt := next((rt for rt in route_tables if rt.is_managed_by_iac and rt.is_main_route_table and rt.vpc_id == vpc.vpc_id),
                                  None):
                return default_rt
            if vpc.raw_data.main_route_table_id:
                if default_rt := ResourceInvalidator.get_by_id(route_tables, vpc.raw_data.main_route_table_id, False):
                    return default_rt
            if vpc.raw_data.default_route_table_id:
                if default_rt := ResourceInvalidator.get_by_id(route_tables, vpc.raw_data.default_route_table_id, False):
                    return default_rt
            if vpc.is_managed_by_iac:
                return self.pseudo_builder.create_main_route_table(vpc.vpc_id, vpc.account, vpc.region)
            return None

        vpc.main_route_table = ResourceInvalidator.get_by_logic(get_default_rt, True, vpc, 'Could not associate main route table')
        vpc.main_route_table.with_aliases(vpc.raw_data.main_route_table_id, vpc.raw_data.default_route_table_id)
        vpc.main_route_table.is_main_route_table = True

        route_tables.update(vpc.main_route_table)

    def _assign_vpc_default_security_group(self, vpc: Vpc, security_groups: AliasesDict[SecurityGroup]):
        def get_default_security_group():
            default_sg = self._find_default_vpc_security_group(set(vpc.aliases), security_groups)
            if not default_sg and vpc.is_managed_by_iac:
                default_sg = self.pseudo_builder.create_security_group(vpc, True, vpc.account, vpc.region)
            return default_sg

        vpc.default_security_group = ResourceInvalidator.get_by_logic(get_default_security_group,
                                                                      True, vpc, 'Could not find default security group')

        if vpc.raw_data.default_security_group_id:
            vpc.default_security_group.with_aliases(vpc.raw_data.default_security_group_id)
            security_groups.update(vpc.default_security_group)

    @staticmethod
    def _find_default_vpc_security_group(vpc_aliases: Set[str], security_groups: AliasesDict[SecurityGroup]) -> Optional[SecurityGroup]:
        for security_group in security_groups:
            if security_group.vpc_id in vpc_aliases and security_group.is_default:
                return security_group
        return None

    def _assign_vpc_default_nacl(self, vpc: Vpc, nacls: AliasesDict[NetworkAcl]):
        def get_default_nacl():
            nacl = next((nacl for nacl in nacls if nacl.is_default and nacl.vpc_id in vpc.aliases), None)
            if not nacl and vpc.is_managed_by_iac:
                nacl = self.pseudo_builder.create_default_nacl(vpc.vpc_id, vpc.account, vpc.region)
            return nacl

        vpc.default_nacl = ResourceInvalidator.get_by_logic(get_default_nacl, True, vpc, 'Could not associate default Network ACL')

    @staticmethod
    def _assign_default_network_acl_rules_for_tf(nacl: NetworkAcl, vpcs: AliasesDict[Vpc]):
        nacl_vpc = ResourceInvalidator.get_by_id(vpcs, nacl.vpc_id, True, nacl)
        if nacl_vpc:
            nacl.inbound_rules.append(NetworkAclRule(nacl.region, nacl.account, nacl.network_acl_id, '0.0.0.0/0',
                                                     0, 65535, RuleAction.DENY, 32767, RuleType.INBOUND, IpProtocol('ALL')))
            nacl.outbound_rules.append(NetworkAclRule(nacl.region, nacl.account, nacl.network_acl_id, '0.0.0.0/0',
                                                      0, 65535, RuleAction.DENY, 32767, RuleType.OUTBOUND, IpProtocol('ALL')))
        if len(nacl_vpc.ipv6_cidr_block) > 0:
            nacl.outbound_rules.append(NetworkAclRule(nacl.region, nacl.account, nacl.network_acl_id, '::/0',
                                                      0, 65535, RuleAction.DENY, 32768, RuleType.OUTBOUND, IpProtocol('ALL')))
            nacl.inbound_rules.append(NetworkAclRule(nacl.region, nacl.account, nacl.network_acl_id, '::/0',
                                                     0, 65535, RuleAction.DENY, 32768, RuleType.INBOUND, IpProtocol('ALL')))

    @staticmethod
    def _assign_rds_cluster_default_security_group(rds_cluster: RdsCluster):
        if rds_cluster.cluster_instances and not rds_cluster.security_group_ids:
            rds_cluster.security_group_ids.append(rds_cluster.cluster_instances[0].network_resource.vpc.default_security_group.security_group_id)

    @staticmethod
    def _assign_subnet_vpc(subnet: Subnet, vpcs: AliasesDict[Vpc]):
        subnet.vpc = ResourceInvalidator.get_by_id(vpcs, subnet.vpc_id, True, subnet)
