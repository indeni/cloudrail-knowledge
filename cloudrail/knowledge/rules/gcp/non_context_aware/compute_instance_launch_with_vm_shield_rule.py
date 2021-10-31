from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class ComputeInstanceLaunchWithVmShieldRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_compute_instance_ensure_shielded_vm'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for compute_instance in env_context.compute_instances:
            if not compute_instance.shielded_instance_config \
                or not compute_instance.shielded_instance_config.enable_secure_boot \
                    or not compute_instance.shielded_instance_config.enable_integrity_monitoring \
                        or not compute_instance.shielded_instance_config.enable_vtpm:
                issues.append(
                    Issue(
                        f"The {compute_instance.get_type()} `{compute_instance.get_friendly_name()}` does not have all "
                        f"shielded_instance_config attributes set to true (enable_secure_boot, enable_vtpm and enable_integrity_monitoring).",
                        compute_instance,
                        compute_instance))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.compute_instances)
