from typing import List

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.connection import PortConnectionProperty
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway import TransitGateway
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import IEcsInstance
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.port_utils import calculate_allowed_ports, convert_port_set_to_range_tuples, \
    is_ecs_network_configurations_contains_ports

from cloudrail.knowledge.context.environment_context.business_logic.connection_builder_data_holders import PrivateConnectionData
from cloudrail.knowledge.context.parallel.process.abstract_async_tasks_executor import AbstractAsyncTasksExecutor


class AddNetworkEntityPrivateConnectionsTask(AbstractAsyncTasksExecutor):

    def __init__(self,
                 network_entity_list: List[NetworkEntity],
                 transit_gateways: List[TransitGateway],
                 network_interfaces: AliasesDict[NetworkInterface],
                 ports_restrictions: List[int]) -> None:
        super().__init__(self._create_network_entity_private_connections)
        self.network_entity_list = network_entity_list
        self.transit_gateways = transit_gateways
        self.network_interfaces = network_interfaces
        self.ports_restrictions = ports_restrictions

    def init_args(self) -> None:
        self.args.extend(self.network_entity_list)

    def handle_results(self, results: list) -> None:
        for connection_data in results:
            src_eni = self.network_interfaces[connection_data.source]
            dst_eni = self.network_interfaces[connection_data.destination]
            ports = connection_data.value
            if ports:
                # todo - ip protocol type need to be calculate
                src_eni.add_private_outbound_conn(PortConnectionProperty(ports, dst_eni.primary_ip_address, IpProtocol('TCP')), dst_eni)
                dst_eni.add_private_inbound_conn(PortConnectionProperty(ports, src_eni.primary_ip_address, IpProtocol('TCP')), src_eni)

    def _create_network_entity_private_connections(self, src_network_entity_list: List[NetworkEntity]) -> List[PrivateConnectionData]:
        connections_data = []
        for src_entity in src_network_entity_list:
            for dst_entity in self.network_entity_list:
                if src_entity is not dst_entity:
                    connections = self._get_network_entity_connections(src_entity, dst_entity,
                                                                       self.transit_gateways,
                                                                       self.ports_restrictions)
                    if connections:
                        connections_data.extend(connections)
        return connections_data

    @staticmethod
    def _get_network_entity_connections(src_entity: NetworkEntity,
                                        dst_entity: NetworkEntity,
                                        transit_gateways: List[TransitGateway],
                                        ports_restrictions: List[int] = None) -> List[PrivateConnectionData]:
        connections_data = []

        for src_eni in src_entity.network_resource.network_interfaces:
            for dst_eni in dst_entity.network_resource.network_interfaces:
                allowed_ports = calculate_allowed_ports(src_eni, dst_eni, transit_gateways, ports_restrictions)

                if allowed_ports:
                    if isinstance(dst_entity.network_resource.owner, IEcsInstance):
                        if is_ecs_network_configurations_contains_ports(dst_entity.network_resource.owner, allowed_ports):
                            connections_data.append(
                                PrivateConnectionData(src_eni.eni_id, dst_eni.eni_id, convert_port_set_to_range_tuples(allowed_ports)))
                    else:
                        connections_data.append(
                            PrivateConnectionData(src_eni.eni_id, dst_eni.eni_id, convert_port_set_to_range_tuples(allowed_ports)))
        return connections_data
