from typing import List, Dict

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class PublicAccessDbRedshiftRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'public_access_db_redshift_rule'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for redshift in env_context.redshift_clusters:
            violating_security_group = redshift.security_group_allowing_public_access
            if violating_security_group:
                issues.append(Issue(
                    f'~Internet~. '
                    f"{redshift.get_type()}: `{redshift.get_friendly_name()}` "
                    f"is on {redshift.network_resource.vpc.get_type()}"
                    f" `{redshift.network_resource.vpc.get_friendly_name()}`. "
                    f"{redshift.get_type()} uses security groups "
                    f"`{', '.join([x.get_friendly_name() for x in redshift.network_resource.security_groups])}`. "
                    f"Security group(s) allow Redshift associated port. "
                    f"{redshift.get_type()} is on subnets:"
                    f" `{', '.join([x.get_friendly_name() for x in redshift.network_resource.subnets])}`. "
                    f"Subnets rely on Network ACL's "
                    f"`{', '.join([x.network_acl.get_friendly_name() for x in redshift.network_resource.subnets])}`. "
                    f"{redshift.get_type()} is capable of traversing to the internet via Redshift associated port. "
                    f"~{redshift.get_type()} `{redshift.get_friendly_name()}`~",
                    redshift,
                    violating_security_group))

        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.redshift_clusters)
