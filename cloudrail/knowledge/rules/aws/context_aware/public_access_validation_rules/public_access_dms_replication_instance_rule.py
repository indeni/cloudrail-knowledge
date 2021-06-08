from typing import Dict, List

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class PublicAccessDmsReplicationInstanceRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'public_access_dms_replication_instance'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for dms_instance in env_context.dms_replication_instances:
            security_group = dms_instance.security_group_allowing_public_access
            if security_group:
                issues.append(Issue(
                    f'~Internet~. '
                    f"Instance `{dms_instance.get_friendly_name()}` is on "
                    f"{dms_instance.network_resource.vpc.get_type()}"
                    f" `{dms_instance.network_resource.vpc.get_friendly_name()}`. "
                    f"{dms_instance.get_type()} uses subnet(s) "
                    f"`{', '.join([x.get_friendly_name() for x in dms_instance.network_resource.subnets])}`. "
                    f"{dms_instance.get_type()} is reachable from the internet due to subnet(s) and route table(s). "
                    f"Subnet uses Network ACL(s) "
                    f"`{', '.join({x.network_acl.get_friendly_name() for x in dms_instance.network_resource.subnets})}`. "
                    f"Network ACL's and security group(s) allows access to the {dms_instance.get_type()}. "
                    f'~{dms_instance.get_type()}~',
                    dms_instance, security_group))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.dms_replication_instances)
