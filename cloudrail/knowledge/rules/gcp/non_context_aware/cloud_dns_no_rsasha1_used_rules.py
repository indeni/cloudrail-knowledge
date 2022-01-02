from typing import List, Dict, Optional

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.dns.gcp_dns_managed_zone import GcpDnsManagedZone, DnsDefKeyAlgorithm, GcpDnsManagedZoneDnsSecCfgDefKeySpecs
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.gcp.gcp_base_rule import GcpBaseRule
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class CloudDnsNoRsasha1UsedRule(GcpBaseRule):
    def get_id(self) -> str:
        return 'non_car_cloud_dns_ensure_rsasha1_disabled'

    def execute(self, env_context: GcpEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for cloud_dns in env_context.dns_managed_zones:
            if affected_dns_keys := self._get_affected_keys(cloud_dns):
                issues.append(
                    Issue(
                        f"The {cloud_dns.get_type()} `{cloud_dns.get_friendly_name()}` has rsasha1 enabled for key(s) "
                        f"{', '.join(key.key_type.value for key in affected_dns_keys)}",
                        cloud_dns,
                        cloud_dns))
        return issues

    def should_run_rule(self, environment_context: GcpEnvironmentContext) -> bool:
        return bool(environment_context.dns_managed_zones)

    @staticmethod
    def _get_affected_keys(cloud_dns: GcpDnsManagedZone) -> Optional[List[GcpDnsManagedZoneDnsSecCfgDefKeySpecs]]:
        if cloud_dns.dnssec_config and cloud_dns.dnssec_config.state == 'on':
            return [default_key for default_key in cloud_dns.dnssec_config.default_key_specs
                    if default_key.algorithm == DnsDefKeyAlgorithm.RSASHA1]
        return None
