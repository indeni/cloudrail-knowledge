from typing import List

from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance, GcpComputeInstanceNetworkInterface, \
    GcpComputeInstanceNetIntfAccessCfg, GcpComputeInstanceNetIntfAliasIpRange, GcpComputeInstanceNetIntfNicType, GcpComputeInstanceServiceAccount, \
    GcpComputeInstanceShieldInstCfg
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeInstanceBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-instances-list.json'

    def do_build(self, attributes: dict) -> GcpComputeInstance:

        ## Network Interfaces ##
        compute_network_interfaces: List[GcpComputeInstanceNetworkInterface] = []
        for interface in attributes.get('networkInterfaces', []):

            nic_type = interface.get('nicType')
            if nic_type:
                nic_type = GcpComputeInstanceNetIntfNicType(nic_type)

            access_config_list: List[GcpComputeInstanceNetIntfAccessCfg] = []
            for access_config in interface.get('accessConfigs', []):
                access_config_list.append(GcpComputeInstanceNetIntfAccessCfg(nat_ip=access_config.get('natIP'),
                                                                             public_ptr_domain_name=access_config.get('publicPtrDomainName'),
                                                                             network_tier=access_config.get('networkTier')))

            aliases_ip_range: List[GcpComputeInstanceNetIntfAliasIpRange] = []
            for ip in interface.get('aliasIpRanges', []):
                aliases_ip_range.append(GcpComputeInstanceNetIntfAliasIpRange(ip_cidr_range=ip.get('ipCidrRange'),
                                                                              subnetwork_range_name=ip.get('subnetworkRangeName')))

            subnetwork_project = self.get_project_from_url(interface.get('subnetwork'))
            compute_network_interfaces.append(GcpComputeInstanceNetworkInterface(network = interface.get('network'),
                                                                         subnetwork = interface.get('subnetwork'),
                                                                         subnetwork_project = subnetwork_project,
                                                                         network_ip = interface.get('networkIP'),
                                                                         access_config=access_config_list,
                                                                         alias_ip_range=aliases_ip_range,
                                                                         nic_type=nic_type))

        ## Service Account ##
        service_account = None
        if service_account_data := attributes.get('serviceAccounts'):
            service_account = GcpComputeInstanceServiceAccount(email=service_account_data[0]['email'],
                                                               scopes=service_account_data[0]['scopes'])

        ## Shielded Instance Config ##
        shielded_instance_config = None
        if shielded_instance_config_data := attributes.get('shieldedInstanceConfig'):
            shielded_instance_config = GcpComputeInstanceShieldInstCfg(shielded_instance_config_data.get('enableSecureBoot', False),
                                                                       shielded_instance_config_data.get('enableVtpm', True),
                                                                       shielded_instance_config_data.get('enableIntegrityMonitoring', True))

        metadata = []
        for metadata_attrbute in attributes.get('metadata', {}).get('items', []):
            metadata.append({metadata_attrbute['key']: metadata_attrbute['value']})

        return GcpComputeInstance(name=attributes['name'],
                                  zone=attributes['zone'].split('/')[-1],
                                  compute_network_interfaces=compute_network_interfaces,
                                  can_ip_forward=attributes.get('canIpForward', False),
                                  hostname=attributes.get('hostname'),
                                  metadata=metadata,
                                  service_account=service_account,
                                  shielded_instance_config=shielded_instance_config,
                                  instance_id=attributes['id'],
                                  self_link=attributes['selfLink'])
