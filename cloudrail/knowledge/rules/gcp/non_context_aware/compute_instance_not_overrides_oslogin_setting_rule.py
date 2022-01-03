from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class ComputeInstanceNotOverridesOsLoginSettingRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_project_ensure_oslogin_enabled_instance'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for compute_instance in env_context.compute_instances:
            if compute_instance.metadata.get('enable-oslogin', '').lower() == 'false':
                issues.append(
                    Issue(
                        f"The {compute_instance.get_type()} `{compute_instance.get_friendly_name()}` has 'enable-oslogin' set to false",
                        compute_instance,
                        compute_instance))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.compute_instances)
