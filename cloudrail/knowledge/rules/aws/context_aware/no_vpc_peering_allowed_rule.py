from typing import List, Dict

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.context.aws.ec2.route import RouteTargetType
from cloudrail.knowledge.context.aws.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext


class NoVpcPeeringAllowedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'no_vpc_peering_allowed_rule'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        peering_connections = self._check_for_peering_connections(env_context)
        issues = []
        for subnet, peerings in peering_connections.items():
            issues.append(Issue(f'{subnet.get_type()}: {subnet.get_friendly_name()} from {subnet.vpc.get_type()}: '
                                f'{subnet.vpc.get_friendly_name()} is using the following {subnet.vpc.get_type()}'
                                f'Peering connections: {peerings}', None, None))
        return issues

    @classmethod
    def _check_for_peering_connections(cls, env_context: AwsEnvironmentContext) -> Dict[Subnet, str]:
        peering_map = {}
        for subnet in env_context.subnets:
            peering_connection_routes = [x for x in subnet.route_table.routes if
                                         x.target_type == RouteTargetType.VPC_PEERING_ID]
            if peering_connection_routes:
                peering_map[subnet] = ', '.join(x.destination for x in peering_connection_routes)

        return peering_map

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.peering_connections)
