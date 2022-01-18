from typing import List
from cloudrail.knowledge.context.azure.resources.load_balancer.azure_load_balancer_probe import AzureLoadBalancerProbe, AzureLoadBalancerProbeProtocol
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class LoadBalancerProbeBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-load-balancers.json'

    def do_build(self, attributes: dict) -> AzureLoadBalancerProbe:
        properties = attributes['properties']
        lb_id = attributes['id']
        lb_probes: List[LoadBalancerProbeBuilder] = []
        for probe in properties['probes']:
            probe_id = probe['id']
            probe_properties = probe['properties']
            probe = AzureLoadBalancerProbe(name=probe['name'],
                                           loadbalancer_id=lb_id,
                                           protocol=enum_implementation(AzureLoadBalancerProbeProtocol, probe_properties['protocol']),
                                           port=probe_properties['port'],
                                           request_path=probe_properties.get('requestPath'),
                                           interval_in_seconds=probe_properties['intervalInSeconds'],
                                           number_of_probes=probe_properties['numberOfProbes'])
            probe.set_id(probe_id)
            probe.with_aliases(probe_id)
            lb_probes.append(probe)
        return lb_probes
