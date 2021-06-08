from typing import List, Dict, Optional

from cloudrail.knowledge.context.aws.indirect_public_connection_data import IndirectPublicConnectionData
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class IndirectPublicAccessDbRds(AwsBaseRule):

    def get_id(self) -> str:
        return 'indirect_public_access_db_rds'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for rds_cluster in env_context.rds_clusters:
            for rds_instance in rds_cluster.cluster_instances:
                violation_info: Optional[IndirectPublicConnectionData] = rds_instance.indirect_public_connection_data
                if violation_info:
                    issues.append(Issue(
                        f"~Internet~. "
                        f"Instance resides in subnet(s) that are routable to internet gateway. Instance has public IP address."
                        f"Instance accepts incoming traffic on port 443. "
                        f"~Instance `{violation_info.target_eni.owner.get_friendly_name()}`~. "
                        f"{rds_cluster.get_type()} `{rds_cluster.get_friendly_name()}` "
                        f"is exposed due to {rds_instance.get_type()} `{rds_instance.get_friendly_name()}`. "
                        f"{rds_instance.get_type()} uses subnets "
                        f"`{', '.join([x.get_friendly_name() for x in rds_instance.network_resource.subnets])}`. "
                        f"{rds_instance.get_type()} "
                        f"resides in same subnet as instance `{violation_info.target_eni.owner.get_friendly_name()}`. "
                        f"{rds_instance.get_type()} relies on Network ACL's "
                        f"`{', '.join([x.network_acl.get_friendly_name() for x in rds_instance.network_resource.subnets])}`. "
                        f"{rds_instance.get_type()} also relies on security groups "
                        f"`{', '.join([x.get_friendly_name() for x in rds_instance.network_resource.security_groups])}`. "
                        f"{rds_instance.get_type()} is accessible from instance within public subnet. "
                        f"~{rds_instance.get_type()} `{rds_instance.get_friendly_name()}`~. ",
                        rds_cluster,
                        violation_info.security_group))

        for rds_instance in (x for x in env_context.rds_instances if x.db_cluster_id is None):
            violation_info: Optional[IndirectPublicConnectionData] = rds_instance.indirect_public_connection_data
            if violation_info:
                issues.append(Issue(
                    f"~Internet~. "
                    f"Instance resides in subnet(s) that are routable to internet gateway. Instance has public IP address. "
                    f"Instance accepts incoming traffic on port 443. "
                    f"~Instance `{violation_info.target_eni.owner.get_friendly_name()}`~. "
                    f"{rds_instance.get_type()} `{rds_instance.get_friendly_name()}` does not have public IP associated. "
                    f"{rds_instance.get_type()} is on subnets: "
                    f"`{', '.join([x.get_friendly_name() for x in rds_instance.network_resource.subnets])}`. "
                    f"{rds_instance.get_type()} resides in same subnet as instance `{violation_info.target_eni.owner.name}`. "
                    f"{rds_instance.get_type()} relies on Network ACL's "
                    f"`{', '.join([x.network_acl.get_friendly_name() for x in rds_instance.network_resource.subnets])}`. "
                    f"{rds_instance.get_type()} also relies on security groups "
                    f"`{', '.join([x.get_friendly_name() for x in rds_instance.network_resource.security_groups])}`. "
                    f"{rds_instance.get_type()} is accessible from instance within public subnet. "
                    f"~{rds_instance.get_type()}~",
                    rds_instance,
                    violation_info.security_group))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.rds_clusters or environment_context.rds_instances)
