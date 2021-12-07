from typing import List

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance, GcpComputeInstanceNetworkInterface, \
    GcpComputeInstanceNetIntfAccessCfg, GcpComputeInstanceNetIntfAliasIpRange, GcpComputeInstanceNetIntfNicType, GcpComputeInstanceServiceAccount, \
    GcpComputeInstanceShieldInstCfg
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder


class ComputeInstanceBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeInstance:

        ## Network Interfaces ##
        compute_network_interfaces: List[GcpComputeInstanceNetworkInterface] = []
        for interface in self._get_known_value(attributes, 'network_interface', []):

            nic_type = self._get_known_value(interface, 'nic_type')
            if nic_type:
                nic_type = GcpComputeInstanceNetIntfNicType(nic_type)

            access_config_list: List[GcpComputeInstanceNetIntfAccessCfg] = []
            for access_config in self._get_known_value(interface, 'access_config', []):
                access_config_list.append(GcpComputeInstanceNetIntfAccessCfg(nat_ip=self._get_known_value(access_config, 'nat_ip'),
                                                                             public_ptr_domain_name=self._get_known_value(access_config, 'public_ptr_domain_name'),
                                                                             network_tier=self._get_known_value(access_config, 'network_tier', 'PREMIUM')))

            aliases_ip_range: List[GcpComputeInstanceNetIntfAliasIpRange] = []
            network = self._get_known_value(interface, 'network')
            subnetwork = self._get_known_value(interface, 'subnetwork')
            network = network or subnetwork
            for ip in self._get_known_value(interface, 'alias_ip_range', []):
                aliases_ip_range.append(GcpComputeInstanceNetIntfAliasIpRange(ip_cidr_range=self._get_known_value(ip, 'ip_cidr_range'),
                                                                              subnetwork_range_name=self._get_known_value(ip, 'subnetwork_range_name')))

            compute_network_interfaces.append(GcpComputeInstanceNetworkInterface(network=network, subnetwork=subnetwork,
                                                                         subnetwork_project=self._get_known_value(interface, 'subnetwork_project'),
                                                                         network_ip=self._get_known_value(interface, 'network_ip'),
                                                                         access_config=access_config_list,
                                                                         alias_ip_range=aliases_ip_range,
                                                                         nic_type=nic_type))

        ## Service Account ##
        service_account = None
        if service_account_data := self._get_known_value(attributes, 'service_account'):
            scopes = service_account_data[0]['scopes']
            for scope in scopes:
                if 'https://' not in scope:
                    scope = f'https://www.googleapis.com/auth/{scope}'
            service_account = GcpComputeInstanceServiceAccount(email=self._get_known_value(service_account_data[0], 'email'),
                                                               scopes=scopes)

        ## Shielded Instance Config ##
        shielded_instance_config = None
        if shielded_instance_config_data := self._get_known_value(attributes, 'shielded_instance_config'):
            shielded_instance_config = GcpComputeInstanceShieldInstCfg(self._get_known_value(shielded_instance_config_data[0], 'enable_secure_boot', False),
                                                                       self._get_known_value(shielded_instance_config_data[0], 'enable_vtpm', True),
                                                                       self._get_known_value(shielded_instance_config_data[0], 'enable_integrity_monitoring', True))
        metadata = []
        if metadata_attributes := self._get_known_value(attributes, 'metadata', []):
            metadata = [{key: metadata_attributes[key]} for key in metadata_attributes]

        if metadata_startup_script := self._get_known_value(attributes, 'metadata_startup_script'):
            metadata.append({'startup-script': metadata_startup_script})
        return GcpComputeInstance(name=attributes['name'],
                                  zone=self._get_known_value(attributes, 'zone'),
                                  compute_network_interfaces=compute_network_interfaces,
                                  can_ip_forward=self._get_known_value(attributes, 'can_ip_forward', False),
                                  hostname=self._get_known_value(attributes, 'hostname'),
                                  metadata=metadata,
                                  service_account=service_account,
                                  shielded_instance_config=shielded_instance_config,
                                  instance_id=attributes['instance_id'],
                                  self_link=attributes['self_link'])

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_INSTANCE
