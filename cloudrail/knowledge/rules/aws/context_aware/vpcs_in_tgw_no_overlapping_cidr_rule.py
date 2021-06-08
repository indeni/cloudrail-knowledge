from typing import List, Dict

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.utils.utils import has_intersection, is_subset
from cloudrail.knowledge.context.aws.ec2.vpc import Vpc
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

        for transit_gateway in env_context.transit_gateways:
            vpc_ids = [route.vpc_attachment.resource_id for route_table in transit_gateway.route_tables
                       for route in route_table.routes if route.vpc_attachment]

            vpcs = [env_context.vpcs[vpc_id] for vpc_id in vpc_ids]
            if len(vpcs) > 1:
                for index, vpc1 in enumerate(vpcs):
                    for j in range(index+1, len(vpcs)):
                        vpc2 = vpcs[j]

                        intersection = self._vpcs_cidrs_intersect(vpc1, vpc2)
                        if intersection:
                            issues.append(Issue(
                                f"~{vpc1.get_type()} `{vpc1.get_friendly_name()}`~. "
                                f"`{vpc1.get_friendly_name()}` uses CIDR block `{intersection}` "
                                f"and has an attachment to {transit_gateway.get_type()} `{transit_gateway.get_friendly_name()}`. "
                                f"~{vpc2.get_type()} `{vpc2.get_friendly_name()}`~. "
                                f"`{vpc2.get_friendly_name()}` uses the same CIDR block and"
                                f" is is attached to the same {transit_gateway.get_type()}. "
                                f"~{transit_gateway.get_type()} `{vpc2.get_friendly_name()}`~",
                                transit_gateway,
                                transit_gateway))
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
