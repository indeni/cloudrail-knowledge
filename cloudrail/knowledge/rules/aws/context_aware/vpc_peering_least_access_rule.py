from typing import List, Dict, Optional

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.utils.utils import is_subset
from cloudrail.knowledge.context.aws.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class VpcPeeringLeastAccessRule(AwsBaseRule):

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.peering_connections)

    def get_id(self) -> str:
        return 'vpc_peering_least_access'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues = []

        for subnet in env_context.subnets:
            route_table = subnet.route_table
            peer_vpc_with_matching_cidr = self._has_peering_route_matching_vpc_cidr(route_table)
            if peer_vpc_with_matching_cidr:
                issues.append(Issue(f"~VPC Peer `{peer_vpc_with_matching_cidr}`~. "
                                    f"VPC Peer uses CIDR block `{peer_vpc_with_matching_cidr}`. "
                                    f"Local VPC's routing table `{route_table.get_friendly_name()}` has a route matching CIDR block. "
                                    f"Local VPC is potentially overexposing resources peering VPC. "
                                    f"~Local VPC `{subnet.vpc_id}`~", subnet.vpc, route_table))

        return issues

    @staticmethod
    def _has_peering_route_matching_vpc_cidr(route_table: RouteTable) -> Optional[str]:
        for route in route_table.routes:
            if route.peering_connection:
                peer_vpc_info = route.peering_connection.accepter_vpc_info \
                    if route.peering_connection.accepter_vpc_info.vpc_id != route_table.vpc_id \
                    else route.peering_connection.requester_vpc_info

                if any(is_subset(vpc_cidr, route.destination) for vpc_cidr in peer_vpc_info.cidr_blocks):
                    return peer_vpc_info.vpc_id

        return None
