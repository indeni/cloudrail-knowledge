from typing import List, Dict

from cloudrail.knowledge.context.aws.elb.load_balancer import LoadBalancerType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AlbDisallowHttpRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_alb_target_group_no_http'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        # Create a set list of target groups, to avoid possible duplicates:
        target_group_list = set()

        for load_balancer in env_context.load_balancers:
            if load_balancer.load_balancer_type == LoadBalancerType.APPLICATION:
                for target_group in load_balancer.target_groups:
                    if target_group not in target_group_list:
                        target_group_list.add(target_group)
                        if target_group.protocol == 'HTTP':
                            for target in target_group.targets:
                                issues.append(
                                    Issue(
                                        f'~{load_balancer.get_type()}~. '
                                        f'The {target_group.get_type()} `{target_group.get_friendly_name()}` '
                                        f'is set to use HTTP with its '
                                        f'targets. This exposes traffic between the load balancer and its '
                                        f'targets', target, target_group))

        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.load_balancers)
