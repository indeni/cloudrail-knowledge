from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureAthenaWorkGroupsResultsEncryptedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_athena_workgroup_query_results_encrypt_at_rest'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for workgroup in env_context.athena_workgroups:
            if workgroup.enforce_workgroup_config:
                if not workgroup.encryption_config:
                    issues.append(
                        Issue(
                            f"The {workgroup.get_type()} `{workgroup.get_friendly_name()}` is not "
                            f"set to encrypt at rest the query results", workgroup, workgroup))
            elif workgroup.encryption_config and not workgroup.enforce_workgroup_config:
                issues.append(
                    Issue(
                        f"The {workgroup.get_type()} `{workgroup.get_friendly_name()}` is "
                        f"set to encrypt at rest the query results, but the workgroup configurations are not set to enforce", workgroup, workgroup))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.athena_workgroups)
