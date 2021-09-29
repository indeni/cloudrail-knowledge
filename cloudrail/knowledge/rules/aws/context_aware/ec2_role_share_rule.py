from typing import List, Dict

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext


class Ec2RoleShareRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'ec2_role_share_rule'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        ec2s: List[Ec2Instance] = env_context.ec2s
        profile_to_public_ec2 = {}
        for public_ec2 in (x for x in ec2s if x.network_resource.is_inbound_public and x.iam_profile_name):
            profile_to_public_ec2[public_ec2.iam_profile_name] = public_ec2
        for private_ec2 in (x for x in ec2s if not x.network_resource.is_inbound_public and x.iam_profile_name):
            public_ec2 = profile_to_public_ec2.get(private_ec2.iam_profile_name)
            profile = private_ec2.iam_role.get_friendly_name() \
                if private_ec2.iam_role  \
                else private_ec2.iam_profile_name
            if public_ec2:
                issues.append(
                    Issue(
                        f"~Instance `{public_ec2.get_friendly_name()}`~. Instance is publicly exposed. "
                        f"Instance uses IAM role `{profile}`. "
                        f"Private EC2 instance shares IAM role `{profile}` as well. "
                        f"~Instance `{private_ec2.get_friendly_name()}`~",
                        private_ec2,
                        private_ec2.iam_role))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.ec2s)
