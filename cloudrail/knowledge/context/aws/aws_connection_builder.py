import copy
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.aws_client import AwsClient
from cloudrail.knowledge.context.aws.resources.aws_policied_resource import PoliciedResource
from cloudrail.knowledge.context.connection import ConnectionProperty, ConnectionType, PolicyConnectionProperty, PortConnectionProperty, \
    PrivateConnectionDetail
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_list import CloudFrontDistribution, OriginConfig
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.aws.resources.ec2.nat_gateways import NatGateways
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_rule import NetworkAclRule, RuleAction
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.route import Route, RouteTargetType
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRule, SecurityGroupRulePropertyType
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway import TransitGateway
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route import TransitGatewayRoute, TransitGatewayRouteType
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpointGateway, VpcEndpointServiceType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_cluster import EcsCluster
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import IEcsInstance, PortMappings
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer, LoadBalancerSchemeType
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target import LoadBalancerTarget
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group import LoadBalancerTargetGroup
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import PrincipalType
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.prefix_lists import PrefixList
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_access_point import S3BucketAccessPointNetworkOriginType
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.arn_utils import are_arns_intersected
from cloudrail.knowledge.utils.port_utils import calculate_allowed_ports, convert_port_set_to_range_tuples, \
    is_ecs_network_configurations_contains_ports, reduce_allowed_ports_for_cidr_block_by_acls
from cloudrail.knowledge.utils.range_util import EMPTY_RANGE, get_range_numbers_dis_overlap, get_range_numbers_overlap
from cloudrail.knowledge.utils.utils import compare_prefix_length, flat_list, get_cidr_subset, get_cidrs_diff, get_overlap_cidr, is_port_in_range, \
    is_public_ip_range, is_subset, is_valid_cidr_block, set_multiprocessing_mode
from cloudrail.knowledge.context.aws.parallel.add_network_entity_private_connections_task import AddNetworkEntityPrivateConnectionsTask
from cloudrail.knowledge.context.aws.parallel.assign_inbound_permissions_connections_task import AssignInboundPermissionsConnectionsTask
from cloudrail.knowledge.context.aws.parallel.assign_roles_to_bucket_task import AssignRolesToBucketTask
from cloudrail.knowledge.context.environment_context.business_logic.connection_builder_data_holders import PrivateConnectionData, PublicConnectionData
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, FunctionData, IterFunctionData
from cloudrail.knowledge.utils.policy_evaluator import is_any_action_allowed, PolicyEvaluation, PolicyEvaluator
from cloudrail.knowledge.utils.s3_public_access_evaluator import S3PublicAccessEvaluator
from netaddr import IPSet


class AccessControlRule:
    def __init__(self, protocol_type: IpProtocol, port_range: Tuple[int, int], target_cidr: str, allow: bool, rule_number: int = 0) -> None:
        self.protocol_type: IpProtocol = protocol_type
        self.port_range: Tuple[int, int] = port_range
        self.target_cidr: str = target_cidr
        self.allow: bool = allow
        self.rule_number: int = rule_number

    def __str__(self) -> str:
        return f"target_cidr={self.target_cidr}, allow={self.allow}, range={str(self.port_range)} rule_number={self.rule_number}"


class AwsConnectionBuilder(DependencyInvocation):
    STRICT_MODE = False

    def __init__(self, ctx: AwsEnvironmentContext, multiprocessing_mode: bool = False, strict_mode: bool = False):
        self._set_strict_mode(strict_mode)
        set_multiprocessing_mode(multiprocessing_mode)

        eni_map_by_key = {eni.eni_id: eni for eni in ctx.network_interfaces}
        s3_pl_by_region_map: Dict[str, PrefixList] = {pll.region: pll.get_prefix_lists_by_service("S3") for pll in ctx.prefix_lists}
        network_entities_to_exclude = (LoadBalancer, LambdaFunction)
        network_entities_after_exclusion: list = [net_ent for net_ent in ctx.get_all_network_entities()
                                                  if not isinstance(net_ent, network_entities_to_exclude)]

        function_pool = [
            FunctionData(self._add_network_entity_private_connections, (network_entities_after_exclusion,
                                                                        ctx.transit_gateways,
                                                                        eni_map_by_key)),
            FunctionData(self._assign_ecs_load_balancing_private_connections,
                         (ctx.ecs_cluster_list, ctx.load_balancers, ctx.transit_gateways, eni_map_by_key)),
            ### Public Bi-Directional Connections
            IterFunctionData(self._assign_ecs_eni_public_connections, ctx.ecs_cluster_list,
                             (ctx.nat_gateway_list,)),
            ### Public Outbound Connections
            IterFunctionData(self._assign_outbound_public_port_connections, ctx.get_all_network_entities(),
                             (ctx.nat_gateway_list,)),
            ### Public Inbound Connections
            IterFunctionData(self._assign_inbound_public_port_connections, ctx.ec2s, ((),)),
            IterFunctionData(self._assign_inbound_public_port_connections,
                             [lb for lb in ctx.load_balancers if lb.scheme_type == LoadBalancerSchemeType.INTERNET_FACING],
                             (lambda x: x.listener_ports,)),
            IterFunctionData(self._assign_inbound_public_port_connections,
                             [redshift for redshift in ctx.redshift_clusters if redshift.is_ec2_vpc_platform],
                             (lambda x: [x.port],)),
            IterFunctionData(self._assign_inbound_public_port_connections, ctx.rds_instances, (lambda x: [x.port],)),
            IterFunctionData(self._assign_inbound_public_port_connections,
                             [eks for eks in ctx.eks_clusters if eks.endpoint_public_access
                              and any(cidr for cidr in eks.public_access_cidrs if is_public_ip_range(cidr))],
                             (lambda x: [x.port],)),
            IterFunctionData(self._assign_inbound_public_port_connections, ctx.neptune_cluster_instances,
                             (lambda x: [x.port],)),
            IterFunctionData(self._assign_inbound_public_port_connections, ctx.dms_replication_instances,
                             ((),)),
            FunctionData(self._add_s3_bucket_public_connections_via_cloudfront, (ctx.s3_buckets, ),
                         [self._add_cloudfront_to_s3_bucket_private_connections]),
            IterFunctionData(self._add_cloudfront_public_connections, ctx.cloudfront_distribution_list, ()),
            ### Private Connections
            IterFunctionData(self._assign_network_entity_to_s3_connections, ctx.get_all_network_entities_aws_clients(),
                             (ctx.s3_buckets, eni_map_by_key, s3_pl_by_region_map),
                             [self._assign_role_to_s3_connections]),
            IterFunctionData(self._assign_network_entity_to_rds_instance_connections, ctx.rds_instances,
                             (ctx.get_all_network_entities(), ctx.transit_gateways, eni_map_by_key)),
            IterFunctionData(self._assign_network_entity_to_elastic_search_domain_connections,
                             ctx.elastic_search_domains, (ctx.get_all_network_entities(), ctx.transit_gateways, eni_map_by_key)),
            IterFunctionData(self._assign_ec2_to_redshift_connections, ctx.redshift_clusters, (ctx.ec2s, ctx.transit_gateways, eni_map_by_key)),
            FunctionData(self._assign_role_to_s3_connections, (ctx.s3_buckets, ctx.roles)),
            IterFunctionData(self._assign_s3_bucket_public_connections, ctx.s3_buckets, ()),
            IterFunctionData(self._assign_load_balancer_to_ec2_connections, ctx.load_balancers, (ctx.transit_gateways, eni_map_by_key)),
            IterFunctionData(self._assign_load_balancer_from_ec2_connections, ctx.load_balancers, (ctx.ec2s, ctx.transit_gateways, eni_map_by_key)),
            IterFunctionData(self._assign_ecs_load_balancing_target_groups, ctx.ecs_cluster_list,
                             (ctx.load_balancers, ctx.load_balancer_target_groups, ctx.load_balancer_targets)),
            IterFunctionData(self._add_to_aws_client_outbound_permissions_connections, ctx.get_all_aws_clients(),
                             (ctx.s3_buckets,),
                             [self._add_network_entity_private_connections,
                              self._assign_outbound_public_port_connections,
                              self._assign_ecs_eni_public_connections]
                             ),  # todo - in the future should add more resources by (rules) requirements

            IterFunctionData(self._add_cloudfront_to_s3_bucket_private_connections, ctx.cloudfront_distribution_list,
                             (ctx.s3_buckets, ),
                             [self._add_network_entity_private_connections,
                              self._assign_outbound_public_port_connections,
                              self._assign_ecs_eni_public_connections]
                             ),
            # Lambda connections
            IterFunctionData(self._add_lambda_outbound_connections, ctx.lambda_function_list,
                             ([net_ent for net_ent in ctx.get_all_network_entities() if not isinstance(net_ent, LambdaFunction)],)),
            ### Inbound Permissions Aws Clients ###
            FunctionData(self._assign_inbound_permissions_connections,
                         (ctx.get_all_aws_clients(), ctx.get_all_iam_entities())),

        ]
        super().__init__(function_pool)

    @classmethod
    def _set_strict_mode(cls, enable: bool):
        cls.STRICT_MODE = enable

    @classmethod
    def _assign_network_entity_to_s3_connections(cls, network_entity: Union[NetworkEntity, AwsClient], buckets: AliasesDict[S3Bucket],
                                                 network_interfaces: AliasesDict[NetworkInterface], s3_pl_by_region_map: Dict[str, PrefixList]):
        for bucket in buckets:
            if bucket.region in s3_pl_by_region_map:
                s3_pl: PrefixList = s3_pl_by_region_map[bucket.region]
                connections_data: List[PrivateConnectionData] = cls._get_network_entity_to_s3_connections(network_entity, bucket, s3_pl)
                for connection_data in connections_data:
                    entity_eni = network_interfaces[connection_data.source]
                    policy_evaluation_results = connection_data.value
                    if policy_evaluation_results:
                        bucket.add_private_inbound_conn(PolicyConnectionProperty(policy_evaluation_results), entity_eni)
                        entity_eni.add_private_outbound_conn(PolicyConnectionProperty(policy_evaluation_results), bucket)

    @classmethod
    def _assign_load_balancer_to_ec2_connections(cls, load_balancer: LoadBalancer,
                                                 transit_gateways: List[TransitGateway],
                                                 network_interfaces: AliasesDict[NetworkInterface]):
        connections_data: List[PrivateConnectionData] = cls._get_load_balancer_to_ec2_connections(load_balancer, transit_gateways)
        for connection_data in connections_data:
            lb_eni = network_interfaces[connection_data.source]
            ec2_eni = network_interfaces[connection_data.destination]
            ports = connection_data.value
            # todo - ip protocol type need to be calculate
            lb_eni.add_private_outbound_conn(PortConnectionProperty(ports, ec2_eni.primary_ip_address, IpProtocol('TCP')), ec2_eni)
            ec2_eni.add_private_inbound_conn(PortConnectionProperty(ports, lb_eni.primary_ip_address, IpProtocol('TCP')), lb_eni)

    @classmethod
    def _assign_load_balancer_from_ec2_connections(cls, load_balancer: LoadBalancer,
                                                   ec2s: List[Ec2Instance],
                                                   transit_gateways: List[TransitGateway],
                                                   network_interfaces: AliasesDict[NetworkInterface]):
        connections_data: List[PrivateConnectionData] = cls._get_ec2_to_load_balancer_connections(load_balancer, ec2s, transit_gateways)
        for connection_data in connections_data:
            ec2_eni = network_interfaces[connection_data.source]
            lb_eni = network_interfaces[connection_data.destination]
            ports = connection_data.value
            # todo - ip protocol type need to be calculate
            lb_eni.add_private_inbound_conn(PortConnectionProperty(ports, ec2_eni.primary_ip_address, IpProtocol('TCP')), ec2_eni)
            ec2_eni.add_private_outbound_conn(PortConnectionProperty(ports, lb_eni.primary_ip_address, IpProtocol('TCP')), lb_eni)

    @classmethod
    def _assign_s3_bucket_public_connections(cls, bucket: S3Bucket):
        connection_data: PublicConnectionData = cls._get_s3_bucket_public_connections(bucket)
        if connection_data.value.policy_evaluation:
            bucket.add_public_inbound_conn(connection_data.value)

    @classmethod
    def _assign_role_to_s3_connections(cls, s3_buckets: AliasesDict[S3Bucket], roles: List[Role]) -> None:
        executor: AssignRolesToBucketTask = AssignRolesToBucketTask(roles, s3_buckets)
        executor.execute()

    @classmethod
    def _assign_ec2_to_redshift_connections(cls, redshift_cluster: RedshiftCluster, network_entities: List[NetworkEntity],
                                            transit_gateways: List[TransitGateway], network_interfaces: AliasesDict[NetworkInterface]):
        if not redshift_cluster.is_ec2_vpc_platform:
            return
        for network_entity in network_entities:
            connections_data: List[PrivateConnectionData] = cls._get_network_entity_connections(network_entity, redshift_cluster, transit_gateways)
            for connection_data in connections_data:
                redshift_eni = network_interfaces[connection_data.destination]
                ec2_eni = network_interfaces[connection_data.source]
                redshift: RedshiftCluster = redshift_eni.owner
                if any(range_tuple for range_tuple in connection_data.value if is_port_in_range(range_tuple, redshift.port)):
                    redshift_port_range = [(redshift.port, redshift.port)]
                    # todo - ip protocol type need to be calculate
                    redshift_eni.add_private_inbound_conn(
                        PortConnectionProperty(redshift_port_range, ec2_eni.primary_ip_address, IpProtocol('TCP')), ec2_eni)
                    ec2_eni.add_private_outbound_conn(
                        PortConnectionProperty(redshift_port_range, redshift_eni.primary_ip_address, IpProtocol('TCP')), redshift_eni)

    @classmethod
    def _assign_inbound_public_port_connections(cls, network_entity: NetworkEntity, get_ports_method: Callable[[NetworkEntity], List[int]] = None):
        network_interfaces = network_entity.network_resource.network_interfaces
        ports = get_ports_method(network_entity) if get_ports_method else None
        for network_interface in network_interfaces:
            connections: List[PortConnectionProperty] = cls.compute_eni_allowed_publicly_cidr_ports(network_interface, True)
            for conn in connections:
                if ports is None:
                    network_interface.add_public_inbound_conn(conn)
                else:
                    ports_in_range = {port for port in list(ports) for range_tuple in conn.ports if is_port_in_range(range_tuple, port)}
                    if ports_in_range:
                        range_tuples = convert_port_set_to_range_tuples(ports_in_range)
                        network_interface.add_public_inbound_conn(PortConnectionProperty(range_tuples, conn.cidr_block, conn.ip_protocol_type))

    @classmethod
    def _assign_outbound_public_port_connections(cls, network_entity: NetworkEntity, nat_gateway_list: List[NatGateways]):
        for eni in network_entity.network_resource.network_interfaces:
            cls._add_eni_outbound_connection(eni, nat_gateway_list)

    @classmethod
    def _assign_network_entity_to_rds_instance_connections(cls, rds_instance: RdsInstance,
                                                           network_entities: List[Union[NetworkEntity, AwsClient]],
                                                           transit_gateways: List[TransitGateway],
                                                           network_interfaces: AliasesDict[NetworkInterface]):
        for network_entity in network_entities:
            connections_data: List[PrivateConnectionData] = cls._get_network_entity_connections(network_entity, rds_instance, transit_gateways)
            for connection_data in connections_data:
                rds_eni = network_interfaces[connection_data.destination]
                ec2_eni = network_interfaces[connection_data.source]
                rds_instance: RdsInstance = rds_eni.owner
                if any(range_tuple for range_tuple in connection_data.value if is_port_in_range(range_tuple, rds_instance.port)):
                    redshift_port_range = [(rds_instance.port, rds_instance.port)]
                    # todo - ip protocol type need to be calculate
                    rds_eni.add_private_inbound_conn(PortConnectionProperty(redshift_port_range, ec2_eni.primary_ip_address,
                                                                            IpProtocol('TCP')), ec2_eni)
                    ec2_eni.add_private_outbound_conn(PortConnectionProperty(redshift_port_range, rds_eni.primary_ip_address,
                                                                             IpProtocol('TCP')), rds_eni)

    @classmethod
    def _assign_network_entity_to_elastic_search_domain_connections(cls, elastic_search_domain: ElasticSearchDomain,
                                                                    network_entities: List[NetworkEntity],
                                                                    transit_gateways: List[TransitGateway],
                                                                    network_interfaces: AliasesDict[NetworkInterface]):
        for network_entity in network_entities:
            connections_data: List[PrivateConnectionData] = cls._get_network_entity_connections(network_entity,
                                                                                                elastic_search_domain, transit_gateways)
            for connection_data in connections_data:
                es_eni = network_interfaces[connection_data.destination]
                ec2_eni = network_interfaces[connection_data.source]
                elastic_search_domain: ElasticSearchDomain = es_eni.owner

                open_ports = {port for port in elastic_search_domain.ports
                              for range_tuple in connection_data.value if is_port_in_range(range_tuple, port)}

                if open_ports:
                    open_ports_tuples = convert_port_set_to_range_tuples(open_ports)
                    # todo - ip protocol type need to be calculate
                    es_eni.add_private_inbound_conn(PortConnectionProperty(open_ports_tuples, ec2_eni.primary_ip_address, IpProtocol('TCP')), ec2_eni)
                    ec2_eni.add_private_outbound_conn(PortConnectionProperty(open_ports_tuples, es_eni.primary_ip_address, IpProtocol('TCP')), es_eni)

    @classmethod
    def _assign_ecs_eni_public_connections(cls, cluster: EcsCluster, nat_gateway_list: List[NatGateways]) -> None:
        for eni in cluster.get_all_eni_list():
            if eni.public_ip_address and isinstance(eni.owner, IEcsInstance):
                container_ports: List[PortMappings] = []
                if eni.owner.get_task_definition():
                    for container_definition in eni.owner.get_task_definition().container_definitions:
                        for ports_map in container_definition.port_mappings:
                            container_ports.append(ports_map)

                connections: List[PortConnectionProperty] = cls.compute_eni_allowed_publicly_cidr_ports(eni, True)
                for conn in connections:
                    for port_map in container_ports:
                        if conn.ip_protocol_type == port_map.protocol \
                                and any(is_port_in_range(ports, port_map.container_port) for ports in conn.ports):
                            eni.add_public_inbound_conn(
                                PortConnectionProperty([(port_map.container_port, port_map.container_port)],
                                                       conn.cidr_block, conn.ip_protocol_type))
                cls._add_eni_outbound_connection(eni, nat_gateway_list)

    @staticmethod
    def _assign_ecs_load_balancing_target_groups(cluster: EcsCluster,
                                                 elb_list: List[LoadBalancer],
                                                 target_group_list: List[LoadBalancerTargetGroup],
                                                 load_balancer_targets: List[LoadBalancerTarget]):
        service_with_elb_list = [service for service in cluster.service_list if service.elb_list]
        for service in service_with_elb_list:
            for elb_conf in service.elb_list:
                for target_group in target_group_list:
                    if elb_conf.target_group_arn == target_group.target_group_arn:
                        for elb in elb_list:
                            if target_group in elb.target_groups:
                                target = LoadBalancerTarget(elb_conf.target_group_arn, None,
                                                            target_group.port, target_group.account, target_group.region)
                                target.target_instance = service
                                target.is_pseudo = True
                                target_group.targets.append(target)
                                elb_conf.elb_name = elb.name
                                load_balancer_targets.append(target)
                                break
                        break

    @classmethod
    def _assign_ecs_load_balancing_private_connections(cls, ecs_cluster_list: List[EcsCluster],
                                                       elb_list: List[LoadBalancer],
                                                       transit_gateways: List[TransitGateway],
                                                       eni_map_by_key: AliasesDict[NetworkInterface]):
        service_with_elb_list: List[EcsService] = cls._get_all_ecs_services_with_elb_conf(ecs_cluster_list)
        for service in service_with_elb_list:
            ecs_elb_list: List[LoadBalancer] = [elb for elb_conf in service.elb_list for elb in elb_list if elb_conf.elb_name == elb.name]
            for lb in ecs_elb_list:
                cls._add_lb_network_entity_private_connections(lb, [service], transit_gateways, eni_map_by_key)
                cls._add_lb_network_entity_private_connections(service, [lb], transit_gateways, eni_map_by_key, lb.listener_ports)

    @classmethod
    def _add_lb_network_entity_private_connections(cls, network_entity: NetworkEntity,
                                                   network_entity_list: List[NetworkEntity],
                                                   transit_gateways: List[TransitGateway],
                                                   network_interfaces: AliasesDict[NetworkInterface],
                                                   ports_restrictions: List[int] = None):
        for dst_entity in network_entity_list:
            if network_entity is not dst_entity:
                connections_data: List[PrivateConnectionData] = \
                    cls._get_network_entity_connections(network_entity, dst_entity, transit_gateways, ports_restrictions)
                for connection_data in connections_data:
                    src_eni = network_interfaces[connection_data.source]
                    dst_eni = network_interfaces[connection_data.destination]
                    ports = connection_data.value
                    if ports:
                        # todo - ip protocol type need to be calculate
                        src_eni.add_private_outbound_conn(PortConnectionProperty(ports, dst_eni.primary_ip_address, IpProtocol('TCP')), dst_eni)
                        dst_eni.add_private_inbound_conn(PortConnectionProperty(ports, src_eni.primary_ip_address, IpProtocol('TCP')), src_eni)

    @classmethod
    def _get_network_entity_connections(cls, src_entity: NetworkEntity,
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

    @classmethod
    def _get_load_balancer_to_ec2_connections(cls, load_balancer: LoadBalancer, transit_gateways: List[TransitGateway]) \
            -> List[PrivateConnectionData]:
        connections_data = []

        for target_group in load_balancer.target_groups:
            if target_group.target_type == 'lambda':
                continue
            port = target_group.port
            for target in target_group.targets:
                if target.target_instance:
                    if isinstance(target.target_instance, Ec2Instance):
                        ec2_eni = next(
                            eni for eni in target.target_instance.network_resource.network_interfaces if eni.is_primary)
                    else:  # is instance of NetworkInterface
                        ec2_eni: NetworkInterface = target.target_instance
                    lb_eni = next((eni for eni in load_balancer.network_resource.network_interfaces
                                   if eni.availability_zone == ec2_eni.availability_zone), load_balancer.network_resource.network_interfaces[0])
                    allowed_ports = calculate_allowed_ports(lb_eni, ec2_eni, transit_gateways)
                    if port in allowed_ports:
                        connection_data = next((x for x in connections_data if x.source == lb_eni.eni_id), None)
                        if connection_data:
                            connection_data.value.add(port)
                        else:
                            connections_data.append(PrivateConnectionData(lb_eni.eni_id, ec2_eni.eni_id, {port}))

        for connection_data in connections_data:
            connection_data.value = convert_port_set_to_range_tuples(connection_data.value)

        return connections_data

    @classmethod
    def _get_ec2_to_load_balancer_connections(cls, load_balancer: LoadBalancer, ec2s: List[Ec2Instance], transit_gateways: List[TransitGateway]) \
            -> List[PrivateConnectionData]:
        connections_data = []

        for ec2 in ec2s:
            for ec2_eni in ec2.network_resource.network_interfaces:
                for lb_eni in load_balancer.network_resource.network_interfaces:
                    allowed_ports = calculate_allowed_ports(ec2_eni, lb_eni, transit_gateways, load_balancer.listener_ports)

                    if allowed_ports:
                        connections_data.append(PrivateConnectionData(ec2_eni.eni_id, lb_eni.eni_id, convert_port_set_to_range_tuples(allowed_ports)))

        return connections_data

    @classmethod
    def compute_eni_allowed_publicly_cidr_ports(cls, eni: NetworkInterface, ingress: bool,
                                                nat_gateway_list: List[NatGateways] = None) \
            -> List[PortConnectionProperty]:
        allowed_cidr_block: IPSet
        if ingress:
            allowed_cidr_block = cls._get_inbound_public_facing_ip_sets(eni.subnet.route_table, eni.subnet.vpc.internet_gateway) \
                if eni.public_ip_address else IPSet()
        else:
            allowed_cidr_block: IPSet = cls._get_outbound_public_facing_cidr_blocks(eni.subnet, nat_gateway_list)

        connections: Set[PortConnectionProperty] = cls._compute_eni_allowed_cidr_ports(eni, ingress)
        if allowed_cidr_block:
            for public_route in allowed_cidr_block.iter_cidrs():
                for conn in connections:
                    conn.cidr_block = get_cidr_subset(str(public_route), conn.cidr_block)

            return [conn for conn in connections if conn.cidr_block is not None and is_public_ip_range(conn.cidr_block)]
        else:
            return []

    @classmethod
    def _compute_eni_allowed_cidr_ports(cls, eni: NetworkInterface, ingress: bool) -> Set[PortConnectionProperty]:
        sg_rules_list: List[AccessControlRule] = []
        for security_group in eni.security_groups:
            sg_list: List[SecurityGroupRule] = security_group.inbound_permissions \
                if ingress else security_group.outbound_permissions
            for sg_rule in sg_list:
                if sg_rule.property_type == SecurityGroupRulePropertyType.IP_RANGES:
                    sg_rules_list.append(
                        AccessControlRule(sg_rule.ip_protocol, (sg_rule.from_port, sg_rule.to_port), sg_rule.property_value, True))

        nacl_rules_list: List[NetworkAclRule] = eni.subnet.network_acl.inbound_rules \
            if ingress else eni.subnet.network_acl.outbound_rules
        nacl_rules: Set[AccessControlRule] = set()
        for nacl_rule in nacl_rules_list:
            nacl_rules.add(
                AccessControlRule(nacl_rule.ip_protocol_type, (nacl_rule.from_port, nacl_rule.to_port),
                                  nacl_rule.cidr_block, nacl_rule.rule_action == RuleAction.ALLOW, nacl_rule.rule_number))

        return cls._compute_allowed_connections(sg_rules_list, nacl_rules)

    @classmethod
    def _compute_allowed_connections(cls, sg_rules_list: List[AccessControlRule],
                                     nacl_rules: Set[AccessControlRule]) \
            -> Set[PortConnectionProperty]:
        allow_cidr_ports_set: Set[PortConnectionProperty] = set()
        nacl_rules = sorted(nacl_rules, key=lambda rule: rule.rule_number)
        for sg_allow_rule in sg_rules_list:
            for nacl_rule in nacl_rules:
                overlap_ports_range: Tuple[int, int] = get_range_numbers_overlap(sg_allow_rule.port_range, nacl_rule.port_range)
                cidrs_overlap_set: IPSet = get_overlap_cidr(sg_allow_rule.target_cidr, nacl_rule.target_cidr)
                if overlap_ports_range != EMPTY_RANGE and cidrs_overlap_set and \
                        (nacl_rule.protocol_type == sg_allow_rule.protocol_type or nacl_rule.protocol_type == IpProtocol('ALL')):
                    if nacl_rule.allow:
                        cls._handle_nacl_allow_rule(overlap_ports_ranges=overlap_ports_range, cidrs_overlap_set=cidrs_overlap_set,
                                                    protocol_type=sg_allow_rule.protocol_type, allow_cidr_ports_set=allow_cidr_ports_set)
                    else:
                        full_denied: bool = cls._handle_nacl_deny_rule(overlap_ports_ranges=overlap_ports_range, sg_allow_rule=sg_allow_rule,
                                                                       nacl_rule=nacl_rule, sg_rules_list=sg_rules_list,
                                                                       cidrs_overlap_set=cidrs_overlap_set)
                        if full_denied:
                            break

        return allow_cidr_ports_set

    @staticmethod
    def _handle_nacl_allow_rule(overlap_ports_ranges: Tuple[int, int], cidrs_overlap_set: IPSet,
                                protocol_type: IpProtocol,
                                allow_cidr_ports_set: Set[PortConnectionProperty]):
        for cidr in cidrs_overlap_set.iter_cidrs():
            allow_cidr_ports_set.add(PortConnectionProperty([overlap_ports_ranges], str(cidr), protocol_type))

    @staticmethod
    def _handle_nacl_deny_rule(overlap_ports_ranges: Tuple[int, int],
                               sg_allow_rule: AccessControlRule,
                               nacl_rule: AccessControlRule,
                               sg_rules_list: List[AccessControlRule],
                               cidrs_overlap_set: IPSet) -> bool:

        cidrs_diff_set: IPSet = get_cidrs_diff(sg_allow_rule.target_cidr, nacl_rule.target_cidr)
        if any(str(cidr) == sg_allow_rule.target_cidr for cidr in cidrs_overlap_set.iter_cidrs()) and \
                sg_allow_rule.port_range == overlap_ports_ranges:
            return True
        first_cidr: bool = False
        if cidrs_overlap_set:
            for cidr in cidrs_overlap_set.iter_cidrs():
                for ports in get_range_numbers_dis_overlap(sg_allow_rule.port_range, nacl_rule.port_range):
                    sg_rule: AccessControlRule = copy.copy(sg_allow_rule)
                    sg_rule.target_cidr = str(cidr)
                    sg_rule.port_range = ports
                    if not (first_cidr or cidrs_diff_set):
                        sg_allow_rule.target_cidr = sg_rule.target_cidr
                        sg_allow_rule.port_range = sg_rule.port_range
                        first_cidr = True
                    elif sg_rule not in sg_rules_list:
                        sg_rules_list.append(sg_rule)

        if cidrs_diff_set:
            for cidr in cidrs_diff_set.iter_cidrs():
                if not first_cidr:
                    sg_allow_rule.target_cidr = str(cidr)
                    first_cidr = True
                else:
                    sg_rule: AccessControlRule = copy.copy(sg_allow_rule)
                    sg_rule.target_cidr = str(cidr)
                    if sg_rule not in sg_rules_list:
                        sg_rules_list.append(sg_rule)
        return False

    @classmethod
    def _get_outbound_public_facing_cidr_blocks(cls, subnet: Subnet, nat_gateway_list: List[NatGateways]) -> IPSet:
        result = IPSet()
        for route in subnet.route_table.routes:
            if is_valid_cidr_block(route.destination):
                route_destination: IPSet = IPSet([route.destination])
                if route.target_type in [RouteTargetType.NAT_GATEWAY_ID]:
                    if is_public_ip_range(route.destination) and \
                            cls._is_route_table_contains_valid_nat_gw(subnet, nat_gateway_list):
                        result.update(route_destination)
                elif route.target_type == RouteTargetType.GATEWAY_ID and subnet.vpc.internet_gateway:
                    if is_public_ip_range(route.destination):
                        result.update(route_destination)
                elif route.target_type == RouteTargetType.EGRESS_ONLY_GATEWAY_ID:
                    result.update(route_destination)
        return result

    @staticmethod
    def _get_inbound_public_facing_ip_sets(route_table: RouteTable, internet_gateway: Optional[InternetGateway]) -> IPSet:
        result = IPSet()
        for route in route_table.routes:
            if route.target_type == RouteTargetType.GATEWAY_ID:
                if internet_gateway and internet_gateway.igw_id == route.target:
                    result = result | IPSet([route.destination])
        return result

    @staticmethod
    def _is_route_table_contains_valid_nat_gw(subnet: Subnet,
                                              nat_gateway_list: List[NatGateways]) -> bool:
        nat_gw_route_list: List[Route] = subnet.route_table.get_nat_gateway_route()
        for nat_gw_route in nat_gw_route_list:
            for vpc_subnet in subnet.vpc.subnets:
                igw_route_list: List[Route] = vpc_subnet.route_table.get_internet_gateway_routes()
                for igw_route in igw_route_list:
                    if igw_route \
                            and (igw_route.target == subnet.vpc.internet_gateway.igw_id and subnet.vpc.internet_gateway.vpc_id == vpc_subnet.vpc_id) \
                            and any(nat_gw_route.target == nat_gw.nat_gateway_id
                                    and vpc_subnet.subnet_id == nat_gw.subnet_id for nat_gw in nat_gateway_list):
                        return True
        return False

    @staticmethod
    def _get_tgw_relevant_route(routes: List[TransitGatewayRoute], ip: str) -> TransitGatewayRoute:
        """
        Gets the relevant Transit-Gateway-Route-Table route for the destination ip as described in
        `Route Evaluation Order <https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html#tgw-routing-overview>`_
        """
        most_specific_routes: List[TransitGatewayRoute] = None
        for route in routes:
            if is_subset(ip, route.destination_cidr_block):
                if not most_specific_routes:
                    most_specific_routes = [route]
                else:
                    if compare_prefix_length(most_specific_routes[0].destination_cidr_block, route.destination_cidr_block) == 1:
                        most_specific_routes = [route]
                    elif compare_prefix_length(most_specific_routes[0].destination_cidr_block, route.destination_cidr_block) == 0:
                        most_specific_routes.append(route)

        if len(most_specific_routes) == 1:
            return most_specific_routes[0]

        static_route = next((x for x in most_specific_routes if x.route_type == TransitGatewayRouteType.STATIC))
        if static_route:
            return static_route

        # TODO: Among propagated routes, VPC CIDRs have a higher precedence than Direct Connect gateways than Site-to-Site VPN
        return most_specific_routes[0]

    @staticmethod
    def _get_s3_bucket_public_connections(bucket: S3Bucket) -> PublicConnectionData:
        evaluation_results = []

        evaluation_result = PolicyEvaluator.evaluate_actions(None,
                                                             bucket,
                                                             [bucket.resource_based_policy] + [x.as_policy() for x in bucket.acls],
                                                             [],
                                                             None)
        if is_any_action_allowed(evaluation_result):
            evaluation_results.append(evaluation_result)
        access_points = [ap for ap in bucket.access_points if ap.network_origin.access_type == S3BucketAccessPointNetworkOriginType.INTERNET]
        for access_point in access_points:
            evaluation_result = PolicyEvaluator.with_additional_policies(None,
                                                                         bucket,
                                                                         evaluation_result,
                                                                         [access_point.resource_based_policy])
            if is_any_action_allowed(evaluation_result):
                evaluation_results.append(evaluation_result)
        return PublicConnectionData(bucket.bucket_name, PolicyConnectionProperty(evaluation_results))

    @classmethod
    def _get_network_entity_to_s3_connections(cls, network_entity: Union[NetworkEntity, AwsClient],
                                              bucket: S3Bucket, s3_prefix_list: PrefixList) -> List[PrivateConnectionData]:
        connection_data = []
        all_policy_evaluation_results = []
        for eni in network_entity.network_resource.network_interfaces:
            vpce_policy_evaluation_results = cls._calculate_network_entity_to_s3_connection_via_vpce(eni, bucket, network_entity.iam_role)
            igw_policy_evaluation_results = cls._calculate_network_entity_to_s3_connection_via_igw(eni, bucket, network_entity.iam_role,
                                                                                                   s3_prefix_list)

            for vpce_id, policy_evaluation_results in vpce_policy_evaluation_results.items():
                if cls._is_eni_to_s3_network_enabled(eni, s3_prefix_list, vpce_id):
                    all_policy_evaluation_results.append(policy_evaluation_results)

            if igw_policy_evaluation_results and cls._is_eni_to_s3_network_enabled(eni, s3_prefix_list, None):
                all_policy_evaluation_results.append(igw_policy_evaluation_results)

            connection_data.append(PrivateConnectionData(eni.eni_id, bucket.bucket_name, flat_list(all_policy_evaluation_results)))

        return connection_data

    @staticmethod
    def _calculate_network_entity_to_s3_connection_via_vpce(eni: NetworkInterface, bucket: S3Bucket, role: Role) -> Dict[str, List[PolicyEvaluation]]:
        connection_map: Dict[str, List[PolicyEvaluation]] = {}
        all_vpc_endpoints = [vpce for vpce in eni.vpc.endpoints if vpce.get_aws_service_type() == VpcEndpointServiceType.S3.value]
        vpce_routes = [route for route in eni.subnet.route_table.routes
                       if route.target_type == RouteTargetType.GATEWAY_ID and
                       any(vpce for vpce in all_vpc_endpoints if vpce.vpce_id == route.target)]
        access_points = [ap for ap in bucket.access_points if
                         ap.network_origin.access_type == S3BucketAccessPointNetworkOriginType.VPC and
                         ap.network_origin.vpc_id == eni.vpc_id]

        if role:
            identity_evaluation_result = role.policy_evaluation_result_map.get(bucket.arn, PolicyEvaluation())

            for vpce_route in vpce_routes:
                vpce_evaluation_results = []
                vpce = next(vpce for vpce in all_vpc_endpoints if vpce.vpce_id == vpce_route.target)
                vpce_evaluation_result = PolicyEvaluator.with_additional_policies(role,
                                                                                  bucket,
                                                                                  identity_evaluation_result,
                                                                                  [vpce.policy])
                if is_any_action_allowed(vpce_evaluation_result):
                    vpce_evaluation_results.append(vpce_evaluation_result)

                for access_point in access_points:
                    ap_evaluation_result = PolicyEvaluator.with_additional_policies(role,
                                                                                    bucket,
                                                                                    vpce_evaluation_result,
                                                                                    [access_point.resource_based_policy])
                    if is_any_action_allowed(ap_evaluation_result):
                        vpce_evaluation_results.append(ap_evaluation_result)

                if vpce_evaluation_results:
                    connection_map[vpce.vpce_id] = vpce_evaluation_results

        return connection_map

    @staticmethod
    def _calculate_network_entity_to_s3_connection_via_igw(eni: NetworkInterface, bucket: S3Bucket, role: Role, s3_prefix_list: PrefixList) \
            -> List[PolicyEvaluation]:
        access_points = [ap for ap in bucket.access_points if
                         ap.network_origin.access_type == S3BucketAccessPointNetworkOriginType.INTERNET]
        is_routable = any(route for route in eni.subnet.route_table.routes if
                          route.is_internet_gateway_target() and
                          any(ip_range for ip_range in s3_prefix_list.cidr_list if is_subset(ip_range, route.destination)))

        policy_evaluation_results = []
        if is_routable:
            if role:  # todo - missing handling anonymous users connection
                identity_evaluation_result = role.policy_evaluation_result_map.get(bucket.arn, PolicyEvaluation())

                for access_point in access_points:
                    ap_evaluation_result = PolicyEvaluator.with_additional_policies(role,
                                                                                    bucket,
                                                                                    identity_evaluation_result,
                                                                                    [access_point.resource_based_policy])
                    if is_any_action_allowed(ap_evaluation_result):
                        policy_evaluation_results.append(ap_evaluation_result)

        return policy_evaluation_results

    @classmethod
    def _is_eni_to_s3_network_enabled(cls, eni: NetworkInterface, s3_prefix_list: PrefixList, vpce_id: Optional[str]) -> bool:
        sg_rules_defining_port_443 = [sg_permission for sg in eni.security_groups for sg_permission in sg.outbound_permissions
                                      if sg_permission.is_in_range(443)]
        allowed_by_nacl = any(ip_range for ip_range in s3_prefix_list.cidr_list if
                              reduce_allowed_ports_for_cidr_block_by_acls(eni.subnet.network_acl.outbound_rules,
                                                                          ip_range,
                                                                          [(443, 443)],
                                                                          cls.STRICT_MODE))
        allowed_by_security_group = \
            (
                any(sg_rule for sg_rule in sg_rules_defining_port_443 if vpce_id and
                    sg_rule.property_type == SecurityGroupRulePropertyType.PREFIX_LIST_ID and sg_rule.property_value == vpce_id)
                or
                any(sg_rule for sg_rule in sg_rules_defining_port_443 if
                    sg_rule.property_type == SecurityGroupRulePropertyType.IP_RANGES
                    and
                    any(ip_range for ip_range in s3_prefix_list.cidr_list if is_subset(ip_range, sg_rule.property_value)))
            )

        return allowed_by_nacl and allowed_by_security_group

    @classmethod
    def _add_eni_outbound_connection(cls, eni: NetworkInterface, nat_gateway_list: List[NatGateways]) -> None:
        connections_list: List[PortConnectionProperty] = cls.compute_eni_allowed_publicly_cidr_ports(
            eni, False, nat_gateway_list)
        for conn in connections_list:
            eni.add_public_outbound_conn(conn)

    @staticmethod
    def _get_all_ecs_services_with_elb_conf(ecs_cluster_list: List[EcsCluster]) -> List[EcsService]:
        return [service for cluster in ecs_cluster_list for service in cluster.service_list if service.elb_list]

    @staticmethod
    def _get_ecs_and_ec2_network_entites(ctx: AwsEnvironmentContext):
        ecs_network_entities: List[NetworkEntity] = [entity for cluster in ctx.ecs_cluster_list
                                                     for entity in cluster.get_all_ecs_instances()]
        return ecs_network_entities + ctx.ec2s

    @classmethod
    def _add_lambda_outbound_connections(cls, lambda_func: LambdaFunction, all_network_entities_list: List[NetworkEntity]) -> None:
        if lambda_func.vpc_config:
            for network_entity in all_network_entities_list:
                if set(network_entity.network_resource.subnets) & set(lambda_func.vpc_config.subnets):
                    for ec2_sg in network_entity.network_resource.security_groups:
                        for lambda_func_sg in lambda_func.vpc_config.security_groups:
                            for rule in SecurityGroup.get_rule_matches(lambda_func_sg.outbound_permissions, ec2_sg.inbound_permissions):
                                lambda_func.add_private_outbound_conn(
                                    PortConnectionProperty([rule.get_ports_range()], rule.property_value, rule.ip_protocol),
                                    network_entity.network_resource.owner)

    @classmethod
    def _add_to_aws_client_outbound_permissions_connections(cls, aws_client_instance: AwsClient,
                                                            target_resources: List[AwsResource]) -> None:
        for target_resource in target_resources:
            if aws_client_instance != target_resource:
                cls._evaluate_private_permissions_connection(aws_client_instance, target_resource)

    @classmethod
    def _evaluate_private_permissions_connection(cls, aws_client: AwsClient,
                                                 target_resource: AwsResource) -> None:
        role: Role = aws_client.iam_role
        if role:
            connection_establish: bool = cls._is_resource_connectivity_establish(aws_client, target_resource.get_aws_service_type()) \
                if isinstance(aws_client, NetworkEntity) and not isinstance(aws_client, LambdaFunction)\
                else True
            if connection_establish:
                policy_evaluation_result: PolicyEvaluation
                if target_resource.get_arn() in role.policy_evaluation_result_map:
                    policy_evaluation_result = role.policy_evaluation_result_map[target_resource.get_arn()]
                else:
                    resource_based_policies: List[Policy] = [target_resource.resource_based_policy] \
                        if isinstance(target_resource, PoliciedResource) and target_resource.resource_based_policy \
                        else []
                    policy_evaluation_result = PolicyEvaluator.evaluate_actions(role,
                                                                                target_resource,
                                                                                resource_based_policies,
                                                                                role.get_policies(),
                                                                                role.permission_boundary)
                    if is_any_action_allowed(policy_evaluation_result):
                        role.policy_evaluation_result_map[target_resource.get_arn()] = policy_evaluation_result
                if is_any_action_allowed(policy_evaluation_result):
                    aws_client.add_private_outbound_conn(PolicyConnectionProperty([policy_evaluation_result]), target_resource)

    @staticmethod
    def _is_resource_connectivity_establish(network_entity: NetworkEntity, aws_service_type: str) -> bool:
        for vpc_endpoint in network_entity.network_resource.vpc.endpoints:
            if isinstance(vpc_endpoint, VpcEndpointGateway):
                return any(route.target == vpc_endpoint.vpce_id
                           and vpc_endpoint.get_aws_service_type() == aws_service_type
                           for route in network_entity.network_resource.routes)
            else:
                for conn in network_entity.network_resource.outbound_connections:
                    if conn.connection_type == ConnectionType.PUBLIC or \
                            isinstance(conn, PrivateConnectionDetail) and \
                            isinstance(conn.target_instance, NetworkInterface) and \
                            conn.target_instance.owner == vpc_endpoint and \
                            vpc_endpoint.get_aws_service_type() == aws_service_type:
                        return True
        return False

    @staticmethod
    def _assign_inbound_permissions_connections(aws_instances: List[Union[AwsResource, AwsClient]], iam_entities: List[IamIdentity]) -> None:
        executor: AssignInboundPermissionsConnectionsTask = AssignInboundPermissionsConnectionsTask(aws_instances, iam_entities)
        executor.execute()

    @staticmethod
    def _add_network_entity_private_connections(network_entity_list: List[NetworkEntity],
                                                transit_gateways: List[TransitGateway],
                                                network_interfaces: AliasesDict[NetworkInterface],
                                                ports_restrictions: List[int] = None) -> None:
        executor = AddNetworkEntityPrivateConnectionsTask(network_entity_list,
                                                          transit_gateways,
                                                          network_interfaces,
                                                          ports_restrictions)
        executor.execute()

    @classmethod
    def _add_cloudfront_to_s3_bucket_private_connections(cls, cloudfront: CloudFrontDistribution,
                                                         bucket_name_to_s3_bucket_map: AliasesDict[S3Bucket]):
        for origin_config in cloudfront.origin_config_list:
            if s3_bucket := bucket_name_to_s3_bucket_map.get(origin_config.domain_name):
                read_actions: Set[str] = cls._get_cloudfront_allowed_s3_bucket_permissions(origin_config, s3_bucket)
                if read_actions:
                    policy_eval: PolicyEvaluation = PolicyEvaluation(read_actions)
                    conn_property: PolicyConnectionProperty = PolicyConnectionProperty([policy_eval])
                    cloudfront.add_private_outbound_conn(conn_property, s3_bucket)
                    s3_bucket.add_private_inbound_conn(conn_property, cloudfront)
                    break

    @classmethod
    def _get_cloudfront_allowed_s3_bucket_permissions(cls, origin_config: OriginConfig, s3_bucket: S3Bucket) -> Set[str]:
        evaluator: S3PublicAccessEvaluator = S3PublicAccessEvaluator(s3_bucket)
        cf_allowed_actions: Set[str] = evaluator.get_all_publicly_allowed_actions()
        if s3_bucket.resource_based_policy:
            for statement in s3_bucket.resource_based_policy.statements:
                if statement.effect == StatementEffect.ALLOW and \
                        any(are_arns_intersected(resource, s3_bucket.get_arn() + '/') for resource in statement.resources):
                    if cls._is_oai_user_arn_allowed(statement, origin_config) or \
                            cls._is_oai_canonical_user_allowed(statement, origin_config):
                        cf_allowed_actions.update(statement.actions)
        return cf_allowed_actions

    @classmethod
    def _add_s3_bucket_public_connections_via_cloudfront(cls, s3_buckets: List[S3Bucket]):
        for bucket in s3_buckets:
            public_conn_property_list: List[ConnectionProperty] = []
            for bucket_conn in bucket.inbound_connections:
                if isinstance(bucket_conn, PrivateConnectionDetail) and isinstance(bucket_conn.target_instance, CloudFrontDistribution):
                    cloudfront: CloudFrontDistribution = bucket_conn.target_instance
                    if any(cf_conn.connection_type == ConnectionType.PUBLIC for cf_conn in cloudfront.inbound_connections):
                        public_conn_property_list.append(bucket_conn.connection_property)
            for conn_property in public_conn_property_list:
                bucket.add_public_inbound_conn(conn_property)

    @staticmethod
    def _is_oai_user_arn_allowed(statement: PolicyStatement, origin_config: OriginConfig) -> bool:
        return (statement.principal.principal_type == PrincipalType.AWS and
                any(are_arns_intersected(oai.iam_arn, principal_val) or oai.iam_arn == principal_val
                    for principal_val in statement.principal.principal_values
                    for oai in origin_config.origin_access_identity_list))

    @staticmethod
    def _is_oai_canonical_user_allowed(statement: PolicyStatement, origin_config: OriginConfig) -> bool:
        return (statement.principal.principal_type == PrincipalType.CANONICAL_USER and
                any(oai.s3_canonical_user_id == principal_val
                    for principal_val in statement.principal.principal_values
                    for oai in origin_config.origin_access_identity_list))

    @classmethod
    def _add_cloudfront_public_connections(cls, cloudfront: CloudFrontDistribution):
        if not any(cache.trusted_signers for cache in cloudfront.get_all_cache_behaviors()):
            cloudfront.add_public_inbound_conn(PortConnectionProperty(ports=[(443, 443)], cidr_block='0.0.0.0/0', ip_protocol_type=IpProtocol('TCP')))
