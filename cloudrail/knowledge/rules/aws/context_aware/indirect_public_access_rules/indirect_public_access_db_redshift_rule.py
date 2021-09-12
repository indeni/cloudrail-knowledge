from typing import List, Dict, Optional

from cloudrail.knowledge.context.aws.resources.indirect_public_connection_data import IndirectPublicConnectionData
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class IndirectPublicAccessDbRedshift(AwsBaseRule):

    def get_id(self) -> str:
        return 'indirect_public_access_db_redshift'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for redshift in env_context.redshift_clusters:
            violation_data: Optional[IndirectPublicConnectionData] = redshift.indirect_public_connection_data
            if violation_data:
                issues.append(
                    Issue(
                        f'~Internet~. '
                        f"Instance `{violation_data.target_eni.owner.get_friendly_name()}"
                        f"` resides in subnet(s) that are routable to internet gateway. "
                        f'Instance has public IP address. '
                        f'Instance accepts incoming traffic on port 443. '
                        f"~Instance `{violation_data.target_eni.owner.get_friendly_name()}`~. "
                        f"Redshift Database: `{redshift.get_friendly_name()}` does not have a public IP address. "
                        f"{redshift.get_type()} is on subnets:"
                        f" `{', '.join([x.get_friendly_name() for x in redshift.network_resource.subnets])}`. "
                        f"Redshift resides in same subnet as Instance `{violation_data.target_eni.owner.get_friendly_name()}`. "
                        f"Redshift Database uses Network ACL's "
                        f"`{', '.join([x.network_acl.get_friendly_name() for x in redshift.network_resource.subnets])}`. "
                        f'{redshift.get_type()} is accessible from instance within public subnet. '
                        f"~{redshift.get_type()} `{redshift.get_friendly_name()}`~",
                        redshift,
                        violation_data.security_group))

        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.redshift_clusters)
