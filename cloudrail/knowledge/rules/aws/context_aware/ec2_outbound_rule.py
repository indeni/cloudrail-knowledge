from typing import List, Dict, Set

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext


class Ec2OutboundRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'ec2_outbound_rule'

    def get_needed_parameters(self) -> List[ParameterType]:
        return [ParameterType.FIREWALL_EC2]

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        misplaced_ec2s: Set[Ec2Instance] = set()
        firewall_ec2s: List[Ec2Instance] = parameters[ParameterType.FIREWALL_EC2]

        for instance in env_context.ec2s:
            if instance.network_resource.is_outbound_public and instance not in firewall_ec2s:
                misplaced_ec2s.add(instance)
        return [Issue(ec2, None, None) for ec2 in misplaced_ec2s]

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.ec2s)
