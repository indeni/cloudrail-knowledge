from abc import abstractmethod
from typing import List, Dict, Tuple, Optional

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.context.connection import ConnectionType, PortConnectionProperty, ConnectionDetail, \
    PrivateConnectionDetail
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpointInterface
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.utils.utils import is_port_in_ranges


class AbstractVpcEndpointRule(AwsBaseRule):

    def __init__(self, aws_service_type: AwsServiceType, service_ports: Tuple, services_list: List[str], include_service: bool) -> None:
        self.aws_service_type: AwsServiceType = aws_service_type
        self.services_list: List[str] = services_list
        self.include_service: bool = include_service
        self.service_ports: Tuple[int] = service_ports

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        pass

    def _init_maps(self, env_context: AwsEnvironmentContext)\
            -> Tuple[List[Vpc], Dict[str, List[AwsResource]], Dict[Vpc, List[NetworkInterface]]]:
        region_to_vpc_map: Dict[str, List[Vpc]] = {}
        region_to_service_map: Dict[str, List[AwsResource]] = {}
        for service in self._get_service_resource_list(env_context):
            if service.region not in region_to_vpc_map:
                region_to_vpc_map[service.region] = []
                region_to_service_map[service.region] = []
            region_to_service_map[service.region].append(service)

        for vpc in env_context.vpcs.values():
            if vpc.region in region_to_vpc_map:
                region_to_vpc_map[vpc.region].append(vpc)

        vpc_to_eni_map: Dict[Vpc, List[NetworkInterface]] = {}
        for eni in env_context.network_interfaces:
            if eni.vpc.region in region_to_vpc_map:
                vpc: Vpc = env_context.vpcs[eni.vpc_id]
                if vpc not in vpc_to_eni_map:
                    vpc_to_eni_map[vpc] = []
                if eni.owner:
                    vpc_to_eni_map[vpc].append(eni)
        return [vpc for vpc_list in region_to_vpc_map.values() for vpc in vpc_list], region_to_service_map, vpc_to_eni_map

    def _get_service_resource_list(self, env_context: AwsEnvironmentContext) -> List[AwsResource]:
        if self.aws_service_type == AwsServiceType.S3:
            return env_context.s3_buckets
        elif self.aws_service_type == AwsServiceType.DYNAMODB:
            return env_context.dynamodb_table_list
        elif self.aws_service_type == AwsServiceType.SQS:
            return env_context.sqs_queues
        elif self.aws_service_type == AwsServiceType.EC2:
            return env_context.ec2s
        else:
            raise Exception(f"unsupported '{self.aws_service_type}' service type")

    def _is_service_eni_match(self, eni: NetworkInterface) -> bool:
        return self.include_service == (eni.owner.get_terraform_resource_type().value in self.services_list)

    def _is_public_connection_exist(self, eni: NetworkInterface) -> bool:
        return any(self._is_connection_type_exist(conn, ConnectionType.PUBLIC) for conn in eni.outbound_connections)

    def _is_vpce_interface_connection_exist(self, eni: NetworkInterface) -> bool:
        return len(self._get_all_active_vpc_endpoint_eni_list(eni)) > 0

    def _get_all_active_vpc_endpoint_eni_list(self, eni: NetworkInterface) -> List[NetworkInterface]:
        vpc_endpoint_eni_list: List[NetworkInterface] = []
        for conn in eni.outbound_connections:
            if eni := self._get_active_vpc_endpoint_eni(conn):
                vpc_endpoint_eni_list.append(eni)
        return vpc_endpoint_eni_list

    def _get_active_vpc_endpoint_eni(self, conn: ConnectionDetail) -> Optional[NetworkInterface]:
        if self._is_connection_type_exist(conn, ConnectionType.PRIVATE) and \
                 (isinstance(conn, PrivateConnectionDetail) and
                  isinstance(conn.target_instance, NetworkInterface) and
                  isinstance(conn.target_instance.owner, VpcEndpointInterface) and
                  conn.target_instance.owner.get_aws_service_type() == self.aws_service_type.value):
            return conn.target_instance
        else:
            return None

    def _is_connection_type_exist(self, conn: ConnectionDetail, conn_type: ConnectionType):
        return conn.connection_type == conn_type and \
                isinstance(conn.connection_property, PortConnectionProperty) and \
                any(is_port_in_ranges(conn.connection_property.ports, port) for port in self.service_ports)

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.vpcs)
