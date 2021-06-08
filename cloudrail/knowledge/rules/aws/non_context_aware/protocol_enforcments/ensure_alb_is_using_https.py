from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureLoadBalancerListenerIsUsingHttps(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_alb_https'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for load_balancer_listener in env_context.load_balancer_listeners:
            if load_balancer_listener.default_action_type.lower() != 'redirect':
                if load_balancer_listener.listener_protocol.lower() == 'http':
                    issues.append(
                        Issue(
                            f'~{load_balancer_listener.get_type()}~. '
                            f'`{load_balancer_listener.get_friendly_name()}` {load_balancer_listener.get_type()} '
                            f'is configured to use protocol HTTP on '
                            f'port: `{load_balancer_listener.listener_port}`', load_balancer_listener, load_balancer_listener))
            else:
                if load_balancer_listener.redirect_action_protocol.lower() == 'http':
                    issues.append(
                        Issue(
                            f'~{load_balancer_listener.get_type()}~. '
                            f'`{load_balancer_listener.get_friendly_name()}` {load_balancer_listener.get_type()} '
                            f'is configured to redirect requests using HTTP protocol, and '
                            f'port: `{load_balancer_listener.redirect_action_port}`', load_balancer_listener, load_balancer_listener))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.load_balancer_listeners)
