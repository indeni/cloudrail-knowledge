from typing import Dict, List

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class PublicAccessDbRdsRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'public_access_db_rds_rule'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for rds_cluster in env_context.rds_clusters:
            for rds_instance in rds_cluster.cluster_instances:
                security_group = rds_instance.security_group_allowing_public_access
                if security_group:
                    issues.append(Issue(
                        f'~Internet~. '
                        f"Instance `{rds_instance.get_friendly_name()}` is "
                        f"in {rds_cluster.get_type()} `{rds_cluster.get_friendly_name()}`. "
                        f"{rds_instance.get_type()} is on {rds_instance.network_resource.vpc.get_type()}"
                        f" `{rds_instance.network_resource.vpc.get_friendly_name()}`. "
                        f"{rds_instance.get_type()} uses subnet(s) "
                        f"`{', '.join([x.get_friendly_name() for x in rds_instance.network_resource.security_groups])}`. "
                        f"{rds_instance.get_type()} is reachable from the internet due to subnet(s) and route table(s). "
                        f"Subnet uses Network ACL's "
                        f"`{', '.join([x.network_acl.get_friendly_name() for x in rds_instance.network_resource.subnets])}`. "
                        f"Network ACL's and security group(s) allows the RDS configured ports. "
                        f'~{rds_instance.get_type()}~',
                        rds_cluster, security_group))

        for rds_instance in (x for x in env_context.rds_instances if x.db_cluster_id is None):
            security_group = rds_instance.security_group_allowing_public_access
            if security_group:
                issues.append(Issue(
                    f"~Internet~. {rds_instance.get_type()} `{rds_instance.get_friendly_name()}` "
                    f"is on {rds_instance.network_resource.vpc.get_type()} "
                    f"`{rds_instance.network_resource.vpc.get_friendly_name()}`. "
                    f'instance uses security groups '
                    f"`{', '.join([x.get_friendly_name() for x in rds_instance.network_resource.security_groups])}` . "
                    f"{rds_instance.get_type()} uses the subnets "
                    f"`{', '.join([x.get_friendly_name() for x in rds_instance.network_resource.subnets])}`. "
                    f"{rds_instance.get_type()} is reachable from the internet due to subnet(s) and route table(s). "
                    f"Subnet uses Network ACL's "
                    f"`{', '.join([x.network_acl.get_friendly_name() for x in rds_instance.network_resource.subnets])}`. "
                    f"Network ACL's and security group(s) allows the RDS configured ports. "
                    f"~{rds_instance.get_type()}~", rds_instance, security_group))

        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.rds_clusters or environment_context.rds_instances)
