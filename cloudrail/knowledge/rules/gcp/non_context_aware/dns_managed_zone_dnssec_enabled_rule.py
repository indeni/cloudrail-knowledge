from typing import List, Dict

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class DnsManagedZoneDnssecEnabledRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_cloud_ensure_dnssec_enabled'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for dns_managed_zone in env_context.dns_managed_zones:
            if not dns_managed_zone.dnssec_config or dns_managed_zone.dnssec_config.state != 'on':
                issues.append(
                    Issue(
                        f"The {dns_managed_zone.get_type()} `{dns_managed_zone.get_friendly_name()}` doesn't have DNSSEC enabled.",
                        dns_managed_zone,
                        dns_managed_zone))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.dns_managed_zones)
