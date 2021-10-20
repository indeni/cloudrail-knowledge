from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.default_mergers.default_nacl_merger import DefaultNaclMerger
from cloudrail.knowledge.context.aws.default_mergers.default_route_table_merger import DefaultRouteTableMerger
from cloudrail.knowledge.context.aws.default_mergers.default_security_group_merger import DefaultSecurityGroupMerger
from cloudrail.knowledge.context.aws.default_mergers.default_subnet_merger import DefaultSubnetMerger
from cloudrail.knowledge.context.aws.default_mergers.default_vpc_attributes_merger import DefaultVpcAttributesMerger
from cloudrail.knowledge.context.aws.default_mergers.default_vpc_merger import DefaultVpcMerger
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.iac_action_type import IacActionType


class AwsEnvironmentContextDefaultsMerger:
    @staticmethod
    def merge_defaults(scanner_ctx: AwsEnvironmentContext, iac_ctx: AwsEnvironmentContext):
        AwsEnvironmentContextDefaultsMerger._merge_vpc_attributes(scanner_ctx, iac_ctx)
        AwsEnvironmentContextDefaultsMerger._merge_vpcs(scanner_ctx, iac_ctx)
        AwsEnvironmentContextDefaultsMerger._merge_subnets(scanner_ctx, iac_ctx)
        AwsEnvironmentContextDefaultsMerger._merge_security_groups(scanner_ctx, iac_ctx)
        AwsEnvironmentContextDefaultsMerger._merge_route_tables(scanner_ctx, iac_ctx)
        AwsEnvironmentContextDefaultsMerger._merge_nacls(scanner_ctx, iac_ctx)

    @staticmethod
    def _merge_vpcs(scanner_ctx: AwsEnvironmentContext, iac_ctx: AwsEnvironmentContext):
        def is_default(vpc: Vpc) -> bool:
            return vpc.is_default

        affected_vpcs = DefaultVpcMerger().merge(scanner_ctx.vpcs.where(is_default), iac_ctx.vpcs.where(is_default), True)
        iac_ctx.vpcs.remove(*affected_vpcs, remove_duplicates=True)
        scanner_ctx.vpcs.update(*affected_vpcs)

    @staticmethod
    def _merge_vpc_attributes(scanner_ctx: AwsEnvironmentContext, iac_ctx: AwsEnvironmentContext):
        new_attributes = [attribute for attribute in iac_ctx.vpcs_attributes if iac_ctx.vpcs[attribute.vpc_id].is_default]
        existing_attributes = [attribute for attribute in scanner_ctx.vpcs_attributes
                               if (vpc := (scanner_ctx.vpcs + iac_ctx.vpcs).get(attribute.vpc_id)) and vpc.is_default]

        affected_attributes = DefaultVpcAttributesMerger().merge(existing_attributes, new_attributes, True)

        iac_ctx.vpcs_attributes = [attribute for attribute in iac_ctx.vpcs_attributes if attribute not in affected_attributes]

    @staticmethod
    def _merge_subnets(scanner_ctx: AwsEnvironmentContext, iac_ctx: AwsEnvironmentContext):
        def is_default(subnet: Subnet) -> bool:
            return subnet.is_default

        affected_subnets = DefaultSubnetMerger().merge(scanner_ctx.subnets.where(is_default), iac_ctx.subnets.where(is_default), True)
        iac_ctx.subnets.remove(*affected_subnets, remove_duplicates=True)
        scanner_ctx.subnets.update(*affected_subnets)

    @staticmethod
    def _merge_security_groups(scanner_ctx: AwsEnvironmentContext, iac_ctx: AwsEnvironmentContext):
        tf_deleted_default_sgs = []
        tf_adopted_default_sgs = []
        scanner_default_sgs = [sg for sg in scanner_ctx.security_groups if sg.is_default]
        for security_group in iac_ctx.security_groups:
            if security_group.is_default:
                if security_group.iac_state.action == IacActionType.DELETE:
                    tf_deleted_default_sgs.append(security_group)
                else:
                    tf_adopted_default_sgs.append(security_group)

        iac_ctx.security_groups.remove(*tf_deleted_default_sgs, remove_duplicates=True)
        iac_ctx.security_groups.update(*tf_adopted_default_sgs)

        affected_sgs = DefaultSecurityGroupMerger().merge(scanner_default_sgs,
                                                          tf_adopted_default_sgs,
                                                          False,
                                                          scanner_ctx.vpcs)

        # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/default_security_group
        # When Terraform first adopts the Default Security Group, it immediately removes all ingress and egress rules in the Security Group.
        # It then proceeds to create any rules specified in the configuration.

        affected_security_group_ids = [sg.security_group_id for sg in affected_sgs]
        scanner_ctx.security_group_rules = [sg_rule for sg_rule in scanner_ctx.security_group_rules
                                            if sg_rule.security_group_id not in affected_security_group_ids]
        iac_ctx.security_groups.remove(*affected_sgs, remove_duplicates=True)
        scanner_ctx.security_groups.update(*affected_sgs)

    @staticmethod
    def _merge_route_tables(scanner_ctx: AwsEnvironmentContext, iac_ctx: AwsEnvironmentContext):
        tf_deleted_default_rts = []
        tf_adopted_default_rts = []
        scanner_default_rts = [rt for rt in scanner_ctx.route_tables if rt.is_main_route_table]
        for route_table in iac_ctx.route_tables:
            if route_table.is_main_route_table:
                if route_table.iac_state.action == IacActionType.DELETE:
                    tf_deleted_default_rts.append(route_table)
                else:
                    tf_adopted_default_rts.append(route_table)

        iac_ctx.route_tables.remove(*tf_deleted_default_rts, remove_duplicates=True)
        iac_ctx.route_tables.update(*tf_adopted_default_rts)

        affected_rts = DefaultRouteTableMerger().merge(scanner_default_rts,
                                                       tf_adopted_default_rts,
                                                       False)

        # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/default_route_table
        # When Terraform first adopts the Default Route Table, it immediately removes all defined routes.
        # It then proceeds to create any routes specified in the configuration.

        affected_route_table_ids = [sg.route_table_id for sg in affected_rts]
        scanner_ctx.routes = [route for route in scanner_ctx.routes
                              if route.route_table_id not in affected_route_table_ids]
        iac_ctx.route_tables.remove(*affected_rts, remove_duplicates=True)
        scanner_ctx.route_tables.update(*affected_rts)

    @staticmethod
    def _merge_nacls(scanner_ctx: AwsEnvironmentContext, iac_ctx: AwsEnvironmentContext):
        tf_deleted_default_nacls = []
        tf_adopted_default_nacls = []
        scanner_default_nacls = [rt for rt in scanner_ctx.network_acls if rt.is_default]
        for nacl in iac_ctx.network_acls:
            if nacl.is_default:
                if nacl.iac_state.action == IacActionType.DELETE:
                    tf_deleted_default_nacls.append(nacl)
                else:
                    tf_adopted_default_nacls.append(nacl)

        iac_ctx.network_acls.remove(*tf_deleted_default_nacls, remove_duplicates=True)
        iac_ctx.network_acls.update(*tf_adopted_default_nacls)

        affected_nacls = DefaultNaclMerger().merge(scanner_default_nacls,
                                                   tf_adopted_default_nacls,
                                                   False)

        # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/default_network_acl
        # When Terraform first adopts the Default Network ACL, it immediately removes all rules in the ACL.
        # It then proceeds to create any rules specified in the configuration.

        affected_nacl_ids = [sg.network_acl_id for sg in affected_nacls]
        scanner_ctx.network_acl_rules = [nacl_rule for nacl_rule in scanner_ctx.network_acl_rules
                                         if nacl_rule.network_acl_id not in affected_nacl_ids]

        # If subnet_ids is defined in the TF, then the associations are transfered to that nacl
        for tf_adopted_default_nacl in affected_nacls:
            if tf_adopted_default_nacl.subnet_ids:
                for subnet_id in tf_adopted_default_nacl.subnet_ids:
                    for nacl in scanner_ctx.network_acls:
                        if nacl not in affected_nacls and subnet_id in nacl.subnet_ids:
                            nacl.subnet_ids.remove(subnet_id)
                            break

        iac_ctx.network_acls.remove(*affected_nacls, remove_duplicates=True)
        scanner_ctx.network_acls.update(*affected_nacls)
