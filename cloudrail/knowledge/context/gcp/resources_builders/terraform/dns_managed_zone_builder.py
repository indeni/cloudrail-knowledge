from typing import List
from cloudrail.knowledge.context.gcp.resources.dns.gcp_dns_managed_zone import GcpDnsManagedZone, GcpDnsManagedZoneDnsSecCfg, GcpDnsManagedZoneDnsSecCfgDefKeySpecs, DnsDefKeyAlgorithm, DnsDefKeyType
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class GcpDnsManagedZoneBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpDnsManagedZone:
        ## DNS security config
        dnssec_config = None
        if dnssec_config_data := self._get_known_value(attributes, 'dnssec_config'):
            ## Default Key Specs config
            default_key_specs: List[GcpDnsManagedZoneDnsSecCfgDefKeySpecs] = []
            default_key_specs_data_list = self._get_known_value(dnssec_config_data[0], 'default_key_specs')
            if not default_key_specs_data_list:
                default_key_specs.extend([GcpDnsManagedZoneDnsSecCfgDefKeySpecs(DnsDefKeyAlgorithm('rsasha256'), 2048, DnsDefKeyType('keySigning'), 'dns#dnsKeySpec'),
                                          GcpDnsManagedZoneDnsSecCfgDefKeySpecs(DnsDefKeyAlgorithm('rsasha256'), 1024, DnsDefKeyType('zoneSigning'), 'dns#dnsKeySpec')])
            else:
                for default_key_specs_data in default_key_specs_data_list:
                    key_type = DnsDefKeyType(self._get_known_value(default_key_specs_data, 'key_type'))
                    key_length = self._get_known_value(default_key_specs_data, 'key_length')
                    if key_type == DnsDefKeyType.KEYSIGNING:
                        key_length = key_length or 2048
                    elif key_type == DnsDefKeyType.ZONESIGNING:
                        key_length = key_length or 1024
                    default_key_specs.append(GcpDnsManagedZoneDnsSecCfgDefKeySpecs(algorithm=DnsDefKeyAlgorithm(self._get_known_value(default_key_specs_data, 'algorithm', 'rsasha256')),
                                                                                   key_length=key_length,
                                                                                   key_type=key_type,
                                                                                   kind=self._get_known_value(default_key_specs_data, 'kind', 'dns#dnsKeySpec')))
            dnssec_config = GcpDnsManagedZoneDnsSecCfg(kind=self._get_known_value(dnssec_config_data[0], 'kind', 'dns#managedZoneDnsSecConfig'),
                                                       non_existence=self._get_known_value(dnssec_config_data[0], 'non_existence', 'nsec3'),
                                                       state=self._get_known_value(dnssec_config_data[0], 'state', 'off'),
                                                       default_key_specs=default_key_specs)
        return GcpDnsManagedZone(name=attributes['name'],
                                 dns_name=attributes['dns_name'],
                                 description=self._get_known_value(attributes, 'description'),
                                 dnssec_config=dnssec_config)

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_DNS_MANAGED_ZONE
