from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import AzureNetworkInterface, IpConfiguration


class NetworkInterfaceBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'network-interfaces.json'

    def do_build(self, attributes: dict) -> AzureNetworkInterface:
        return AzureNetworkInterface(
            name=attributes['name'],
            ip_configurations=[IpConfiguration(public_ip_id=ip_config['properties'].get('publicIpAddress', {}).get('id'),
                                               subnet_id=ip_config['properties']['subnet']['id'],
                                               private_ip=ip_config['properties']['privateIPAddress'],
                                               application_security_groups_ids=[asg['id'] for asg in ip_config['properties'].get('applicationSecurityGroups', [])])
                               for ip_config in attributes['properties']['ipConfigurations']])
