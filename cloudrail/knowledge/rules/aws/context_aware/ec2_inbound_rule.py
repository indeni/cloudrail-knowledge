from typing import List, Dict, Set

from cloudrail.knowledge.context.aws.elb.load_balancer import LoadBalancer
from cloudrail.knowledge.context.aws.networking_config.network_resource import NetworkResource
from cloudrail.knowledge.context.aws.aws_connection import PrivateConnectionDetail
from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class Ec2InboundRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'ec2_inbound_rule'

    def get_needed_parameters(self) -> List[ParameterType]:
        return [ParameterType.FIREWALL_EC2]

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        misplaced_ec2s: Set[Ec2Instance] = set()
        firewall_ec2s: List[Ec2Instance] = parameters[ParameterType.FIREWALL_EC2]
        network_resources: List[NetworkResource] = env_context.get_all_nodes_resources()
        for instance in network_resources:
            if instance.is_inbound_public:
                misplaced_ec2s = misplaced_ec2s.union(self._get_misplaced_ec2s(instance, firewall_ec2s))
        return [Issue(ec2, None, None) for ec2 in misplaced_ec2s]

    def _get_misplaced_ec2s(self, network_resource: NetworkResource, firewall_ec2s: List[Ec2Instance]) -> \
            List[Ec2Instance]:
        misplaced_ec2s: Set[Ec2Instance] = set()

        if isinstance(network_resource.owner, Ec2Instance):
            if network_resource.owner in firewall_ec2s:
                return []
            else:
                misplaced_ec2s.add(network_resource.owner)
        elif isinstance(network_resource.owner, LoadBalancer):
            for connection in network_resource.outbound_connections:
                if isinstance(connection, PrivateConnectionDetail):
                    instance = connection.target_instance
                    misplaced_ec2s = misplaced_ec2s.union(self._get_misplaced_ec2s(instance, firewall_ec2s))

        return list(misplaced_ec2s)

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.ec2s)
