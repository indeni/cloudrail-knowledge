from typing import List, Dict

from cloudrail.knowledge.context.aws.elb.load_balancer import LoadBalancerType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureLoadBalancerDropsInvalidHttpHeadersRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_alb_drops_invalid_http_headers'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for lb in env_context.load_balancers:
            if lb.load_balancer_type == LoadBalancerType.APPLICATION and lb.load_balancer_attributes:
                if not lb.load_balancer_attributes.drop_invalid_header_fields:
                    issues.append(
                        Issue(
                            f'The {lb.get_type()} `{lb.get_friendly_name()}` does not drop invalid HTTP headers', lb, lb))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.load_balancers)
