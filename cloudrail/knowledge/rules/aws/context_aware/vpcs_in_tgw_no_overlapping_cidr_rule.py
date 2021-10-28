from typing import List, Dict
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway import TransitGateway
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_resource_type import TransitGatewayResourceType
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.utils.utils import has_intersection, is_subset
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class VpcsInTransitGatewayNoOverlappingCidrRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'vpcs_in_transit_gateway_no_overlapping_cidr_rule'

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List = []
        tgw_to_vpc_map: Dict[str, List[str]] = {}
        for tgw_attach in env_context.transit_gateway_attachments:
            if tgw_attach.resource_type == TransitGatewayResourceType.VPC:
                if tgw_attach.transit_gateway_id not in tgw_to_vpc_map:
                    tgw_to_vpc_map[tgw_attach.transit_gateway_id] = []
                tgw_to_vpc_map[tgw_attach.transit_gateway_id].append(tgw_attach.resource_id)

        transit_gateways: AliasesDict[TransitGateway] = AliasesDict(*env_context.transit_gateways)
        for tgw_id, vpc_ids in tgw_to_vpc_map.items():
            if len(vpc_ids) > 1:
                tgw: TransitGateway = transit_gateways.get(tgw_id)

                for index, vpc_id1 in enumerate(vpc_ids):
                    vpc1: Vpc = env_context.vpcs.get(vpc_id1)
                    for j in range(index+1, len(vpc_ids)):
                        vpc_id2 = vpc_ids[j]
                        vpc2: Vpc = env_context.vpcs.get(vpc_id2)
                        intersection = self._vpcs_cidrs_intersect(vpc1, vpc2)
                        if intersection:
                            issues.append(Issue(
                                f"~{vpc1.get_type()} `{vpc1.get_friendly_name()}`~. "
                                f"`{vpc1.get_friendly_name()}` uses CIDR block `{intersection}` "
                                f"and has an attachment to {tgw.get_type()} `{tgw.get_friendly_name()}`. "
                                f"~{vpc2.get_type()} `{vpc2.get_friendly_name()}`~. "
                                f"`{vpc2.get_friendly_name()}` uses the same CIDR block and"
                                f" is is attached to the same {tgw.get_type()}. "
                                f"~{tgw.get_type()} `{vpc2.get_friendly_name()}`~",
                                tgw,
                                tgw))
        return issues

    @staticmethod
    def _vpcs_cidrs_intersect(vpc1: Vpc, vpc2: Vpc):
        for cidr1 in vpc1.cidr_block:
            for cidr2 in vpc2.cidr_block:
                if has_intersection(cidr1, cidr2):
                    return cidr1 if is_subset(cidr1, cidr2) else cidr2
        return None

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.transit_gateways)
