import json
from collections.abc import Iterable
from typing import Dict, List, Optional

from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import ApiGatewayIntegration, IntegrationType
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import ApiGatewayMethodSettings, RestApiMethod
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_stage import AccessLogsSettings, ApiGatewayStage
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw import ApiGatewayType, RestApiGw
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_domain import RestApiGwDomain
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_mapping import RestApiGwMapping
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_policy import RestApiGwPolicy
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2 import ApiGateway
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2_integration import ApiGatewayV2Integration
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2_vpc_link import ApiGatewayVpcLink
from cloudrail.knowledge.context.aws.resources.athena.athena_database import AthenaDatabase
from cloudrail.knowledge.context.aws.resources.athena.athena_workgroup import AthenaWorkgroup
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_configuration import AutoScalingGroup, LaunchConfiguration
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.resources.batch.batch_compute_environment import BatchComputeEnvironment
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_list import CacheBehavior, CloudFrontDistribution, OriginConfig, \
    ViewerCertificate
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_logging import CloudfrontDistributionLogging
from cloudrail.knowledge.context.aws.resources.cloudfront.origin_access_identity import OriginAccessIdentity
from cloudrail.knowledge.context.aws.resources.cloudhsmv2.cloudhsm_v2_cluster import CloudHsmV2Cluster
from cloudrail.knowledge.context.aws.resources.cloudhsmv2.cloudhsm_v2_hsm import CloudHsmV2Hsm
from cloudrail.knowledge.context.aws.resources.cloudtrail.cloudtrail import CloudTrail
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_event_target import CloudWatchEventTarget
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_log_group import CloudWatchLogGroup
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloudwatch_logs_destination import CloudWatchLogsDestination
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloudwatch_logs_destination_policy import CloudWatchLogsDestinationPolicy
from cloudrail.knowledge.context.aws.resources.codebuild.codebuild_project import CodeBuildProject
from cloudrail.knowledge.context.aws.resources.codebuild.codebuild_report_group import CodeBuildReportGroup
from cloudrail.knowledge.context.aws.resources.configservice.config_aggregator import ConfigAggregator
from cloudrail.knowledge.context.aws.resources.dax.dax_cluster import DaxCluster
from cloudrail.knowledge.context.aws.resources.dms.dms_replication_instance import DmsReplicationInstance
from cloudrail.knowledge.context.aws.resources.dms.dms_replication_instance_subnet_group import DmsReplicationInstanceSubnetGroup
from cloudrail.knowledge.context.aws.resources.docdb.docdb_cluster import DocumentDbCluster
from cloudrail.knowledge.context.aws.resources.docdb.docdb_cluster_parameter import DocDbClusterParameter
from cloudrail.knowledge.context.aws.resources.docdb.docdb_cluster_parameter_group import DocDbClusterParameterGroup
from cloudrail.knowledge.context.aws.resources.ds.directory_service import DirectoryService
from cloudrail.knowledge.context.aws.resources.dynamodb.dynamodb_table import BillingMode, DynamoDbTable, TableField, TableFieldType
from cloudrail.knowledge.context.aws.resources.ec2.ec2_image import Ec2Image
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import AssociatePublicIpAddress, Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.elastic_ip import ElasticIp
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.aws.resources.ec2.main_route_table_association import MainRouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.nat_gateways import NatGateways
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_rule import NetworkAclRule, RuleAction, RuleType
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.peering_connection import PeeringConnection, PeeringVpcInfo
from cloudrail.knowledge.context.aws.resources.ec2.route import Route, RouteTargetType
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.route_table_association import RouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import ConnectionType, SecurityGroupRule, SecurityGroupRulePropertyType
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway import TransitGateway
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_resource_type import TransitGatewayResourceType
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route import TransitGatewayRoute, TransitGatewayRouteState, TransitGatewayRouteType
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table import TransitGatewayRouteTable
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table_association import TransitGatewayRouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table_propagation import TransitGatewayRouteTablePropagation
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_vpc_attachment import TransitGatewayVpcAttachment
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc, VpcAttribute
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpoint, VpcEndpointGateway, VpcEndpointInterface
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint_route_table_association import VpcEndpointRouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.vpc_gateway_attachment import VpcGatewayAttachment
from cloudrail.knowledge.context.aws.resources.ecr.ecr_repository import EcrRepository
from cloudrail.knowledge.context.aws.resources.ecr.ecr_repository_policy import EcrRepositoryPolicy
from cloudrail.knowledge.context.aws.resources.ecs.ecs_cluster import EcsCluster
from cloudrail.knowledge.context.aws.resources.ecs.ecs_constants import LaunchType, NetworkMode
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.resources.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import ContainerDefinition, EcsTaskDefinition, EfsVolume, PortMappings
from cloudrail.knowledge.context.aws.resources.ecs.load_balancing_configuration import LoadBalancingConfiguration
from cloudrail.knowledge.context.aws.resources.efs.efs_file_system import ElasticFileSystem
from cloudrail.knowledge.context.aws.resources.efs.efs_mount_target import EfsMountTarget
from cloudrail.knowledge.context.aws.resources.efs.efs_policy import EfsPolicy
from cloudrail.knowledge.context.aws.resources.eks.eks_cluster import EksCluster
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_cluster import ElastiCacheCluster
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_replication_group import ElastiCacheReplicationGroup
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_subnet_group import ElastiCacheSubnetGroup
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer, LoadBalancerSchemeType, LoadBalancerType
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_attributes import LoadBalancerAccessLogs, LoadBalancerAttributes
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_listener import LoadBalancerListener
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target import LoadBalancerTarget
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group import LoadBalancerTargetGroup
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group_association import LoadBalancerTargetGroupAssociation
from cloudrail.knowledge.context.aws.resources.emr.emr_cluster import EmrCluster
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain, LogPublishingOptions
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain_policy import ElasticSearchDomainPolicy
from cloudrail.knowledge.context.aws.resources.fsx.fsx_windows_file_system import FsxWindowsFileSystem
from cloudrail.knowledge.context.aws.resources.glacier.glacier_vault import GlacierVault
from cloudrail.knowledge.context.aws.resources.glacier.glacier_vault_policy import GlacierVaultPolicy
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator import GlobalAccelerator
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator_attributes import GlobalAcceleratorAttribute
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator_endpoint_group import GlobalAcceleratorEndpointGroup
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator_listener import GlobalAcceleratorListener
from cloudrail.knowledge.context.aws.resources.glue.glue_connection import GlueConnection
from cloudrail.knowledge.context.aws.resources.glue.glue_data_catalog_crawler import GlueCrawler
from cloudrail.knowledge.context.aws.resources.glue.glue_data_catalog_policy import GlueDataCatalogPolicy
from cloudrail.knowledge.context.aws.resources.glue.glue_data_catalog_table import GlueDataCatalogTable
from cloudrail.knowledge.context.aws.resources.iam.iam_group import IamGroup
from cloudrail.knowledge.context.aws.resources.iam.iam_group_membership import IamGroupMembership
from cloudrail.knowledge.context.aws.resources.iam.iam_instance_profile import IamInstanceProfile
from cloudrail.knowledge.context.aws.resources.iam.iam_password_policy import IamPasswordPolicy
from cloudrail.knowledge.context.aws.resources.iam.iam_policy_attachment import IamPolicyAttachment
from cloudrail.knowledge.context.aws.resources.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.resources.iam.iam_user_group_membership import IamUserGroupMembership
from cloudrail.knowledge.context.aws.resources.iam.iam_users_login_profile import IamUsersLoginProfile
from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy, InlinePolicy, ManagedPolicy, Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_group_attachment import PolicyGroupAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_role_attachment import PolicyRoleAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementCondition, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.policy_user_attachment import PolicyUserAttachment
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.kinesis.kinesis_firehose_stream import KinesisFirehoseStream
from cloudrail.knowledge.context.aws.resources.kinesis.kinesis_stream import KinesisStream
from cloudrail.knowledge.context.aws.resources.kms.kms_alias import KmsAlias
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.resources.kms.kms_key_policy import KmsKeyPolicy
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import create_lambda_function_arn, LambdaAlias
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_policy import LambdaPolicy
from cloudrail.knowledge.context.aws.resources.mq.mq_broker import MqBroker
from cloudrail.knowledge.context.aws.resources.neptune.neptune_cluster import NeptuneCluster
from cloudrail.knowledge.context.aws.resources.neptune.neptune_instance import NeptuneInstance
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.rds.db_subnet_group import DbSubnetGroup
from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_global_cluster import RdsGlobalCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.aws.resources.redshift.redshift_logging import RedshiftLogging
from cloudrail.knowledge.context.aws.resources.redshift.redshift_subnet_group import RedshiftSubnetGroup
from cloudrail.knowledge.context.aws.resources.s3.public_access_block_settings import PublicAccessBlockLevel, PublicAccessBlockSettings
from cloudrail.knowledge.context.aws.resources.s3.s3_acl import GranteeTypes, S3ACL, S3Permission, S3PredefinedGroups
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.resources.s3.s3_policy import S3Policy
from cloudrail.knowledge.context.aws.resources.s3.s3_access_point_policy import S3AccessPointPolicy
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_access_point import S3BucketAccessPoint, S3BucketAccessPointNetworkOrigin, \
    S3BucketAccessPointNetworkOriginType
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_encryption import S3BucketEncryption
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_logging import S3BucketLogging
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_object import S3BucketObject
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_versioning import S3BucketVersioning
from cloudrail.knowledge.context.aws.resources.s3outposts.s3outpost_endpoint import S3OutpostEndpoint
from cloudrail.knowledge.context.aws.resources.sagemaker.sagemaker_endpoint_config import SageMakerEndpointConfig
from cloudrail.knowledge.context.aws.resources.sagemaker.sagemaker_notebook_instance import SageMakerNotebookInstance
from cloudrail.knowledge.context.aws.resources.secretsmanager.secrets_manager_secret import SecretsManagerSecret
from cloudrail.knowledge.context.aws.resources.secretsmanager.secrets_manager_secret_policy import SecretsManagerSecretPolicy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.sns.sns_topic import SnsTopic
from cloudrail.knowledge.context.aws.resources.sqs.sqs_queue import SqsQueue
from cloudrail.knowledge.context.aws.resources.sqs.sqs_queue_policy import SqsQueuePolicy
from cloudrail.knowledge.context.aws.resources.ssm.ssm_parameter import SsmParameter
from cloudrail.knowledge.context.aws.resources.worklink.worklink_fleet import WorkLinkFleet
from cloudrail.knowledge.context.aws.resources.workspaces.workspace_directory import WorkspaceDirectory
from cloudrail.knowledge.context.aws.resources.workspaces.workspace import Workspace
from cloudrail.knowledge.context.aws.resources.xray.xray_encryption import XrayEncryption
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils import hash_utils

from cloudrail.knowledge.utils.arn_utils import build_arn, is_valid_arn
from cloudrail.knowledge.utils.port_utils import get_port_by_engine
from cloudrail.knowledge.utils.utils import build_lambda_function_integration_endpoint_uri, safe_json_loads

from cloudrail.knowledge.context.environment_context.common_component_builder \
    import ALL_SERVICES_PUBLIC_FULL_ACCESS, build_policy_statement, build_policy_statements_from_str, get_dict_value

route_destination_types: Dict[str, RouteTargetType] = {
    'gateway_id': RouteTargetType.GATEWAY_ID,
    'nat_gateway_id': RouteTargetType.NAT_GATEWAY_ID,
    'instance_id': RouteTargetType.INSTANCE_ID,
    'egress_only_gateway_id': RouteTargetType.EGRESS_ONLY_GATEWAY_ID,
    'vpc_peering_connection_id': RouteTargetType.VPC_PEERING_ID,
    'transit_gateway_id': RouteTargetType.TRANSIT_GATEWAY_ID}


def build_ec2(attributes: dict) -> Ec2Instance:
    private_ip = _get_known_value(attributes, 'private_ip')
    public_ip = _get_known_value(attributes, 'public_ip')
    ipv6_addresses = _get_known_value(attributes, 'ipv6_addresses', [])
    network_interfaces = _get_known_value(attributes, 'network_interface', [])
    network_interface_ids = [ni['network_interface_id'] for ni in network_interfaces]
    primary_network_interface_id = _get_known_value(attributes, 'primary_network_interface_id') \
                                   or _get_known_value(attributes, 'network_interface_id')
    security_groups_ids_classic = _get_known_value(attributes, 'vpc_security_group_ids')
    security_groups_ids_standard = _get_known_value(attributes, 'security_groups')
    security_groups_ids = security_groups_ids_standard \
        if (security_groups_ids_standard and any(sg_id != 'default' for sg_id in security_groups_ids_standard)) \
            else security_groups_ids_classic
    if primary_network_interface_id:
        network_interface_ids.append(primary_network_interface_id)
    associate_public_ip_address = AssociatePublicIpAddress.convert_from_optional_boolean(_get_known_value(attributes, 'associate_public_ip_address'))

    metadata_options = _get_known_value(attributes, 'metadata_options')
    http_tokens = 'optional'
    if metadata_options:
        http_tokens = _get_known_value(metadata_options[0], 'http_tokens')

    ebs_optimized = False
    if _get_known_value(attributes, 'ebs_optimized'):
        ebs_optimized = attributes['ebs_optimized']

    return Ec2Instance(account=attributes['account_id'],
                       region=attributes['region'],
                       instance_id=attributes['id'],
                       name=_get_name(attributes),
                       network_interfaces_ids=network_interface_ids,
                       state=attributes.get('instance_state'),
                       image_id=attributes['ami'],
                       iam_profile_name=attributes.get('iam_instance_profile') if attributes.get('iam_instance_profile') else None,
                       http_tokens=http_tokens,
                       availability_zone=_get_known_value(attributes, 'availability_zone'),
                       tags=_get_known_value(attributes, 'tags') or {},
                       instance_type=attributes['instance_type'],
                       ebs_optimized=ebs_optimized,
                       monitoring_enabled=_get_known_value(attributes, 'monitoring', False)) \
        .with_raw_data(subnet_id=_get_known_value(attributes, 'subnet_id'),
                       private_ip_address=private_ip,
                       public_ip_address=public_ip,
                       associate_public_ip_address=associate_public_ip_address,
                       ipv6_addresses=ipv6_addresses,
                       security_groups_ids=security_groups_ids)


def build_iam_role(attributes: dict) -> Role:
    qualified_arn: str = build_arn('iam', None, attributes['account_id'], 'role', attributes.get('path'), attributes['name'])
    role: Role = Role(account=attributes['account_id'], qualified_arn=qualified_arn,
                      arn=attributes['arn'], role_name=attributes['name'],
                      role_id=attributes.get('unique_id'),
                      permission_boundary_arn=attributes['permissions_boundary'],
                      creation_date=_get_known_value(attributes, 'create_date'))
    if role.role_id:
        role.with_aliases(role.role_id, attributes['id'])
    else:
        role.with_aliases(attributes['id'])
    return role


def build_iam_assume_role_policy(attributes: dict) -> AssumeRolePolicy:
    return AssumeRolePolicy(attributes['account_id'], attributes['name'], attributes['arn'],
                            _build_policy_statements_from_str(attributes, 'assume_role_policy'),
                            _get_known_value(attributes, 'assume_role_policy'))


def build_iam_group(attributes: dict) -> IamGroup:
    qualified_arn: str = build_arn('iam', None, attributes['account_id'], 'group', attributes.get('path'), attributes['name'])
    return IamGroup(name=attributes['name'],
                    group_id=attributes['unique_id'],
                    qualified_arn=qualified_arn,
                    arn=attributes['arn'],
                    account=attributes['account_id'])


def build_iam_user(attributes: dict) -> IamUser:
    qualified_arn: str = build_arn('iam', None, attributes['account_id'], 'user', attributes.get('path'), attributes['name'])
    return IamUser(account=attributes['account_id'],
                   name=attributes['name'],
                   user_id=attributes['unique_id'],
                   qualified_arn=qualified_arn,
                   arn=attributes['arn'],
                   permission_boundary_arn=attributes['permissions_boundary'])


def build_user_login_profile(attributes: dict) -> IamUsersLoginProfile:
    return IamUsersLoginProfile(attributes['user'],
                                attributes['account_id'])


def build_load_balancer(attributes: dict) -> LoadBalancer:
    raw_subnet_ids = attributes['subnets']
    raw_subnet_ids = raw_subnet_ids if isinstance(raw_subnet_ids, list) else []
    arn = attributes['arn']

    return LoadBalancer(account=attributes['account_id'],
                        name=attributes['name'],
                        region=attributes['region'],
                        scheme_type=_get_load_balancer_scheme_type(attributes),
                        load_balancer_type=LoadBalancerType(attributes['load_balancer_type']),
                        load_balancer_arn=arn) \
        .with_raw_data(raw_subnet_ids, _get_known_value(attributes, 'security_groups'), _get_known_value(attributes, 'subnet_mapping')) \
        .with_aliases(arn, attributes['id'])


def build_load_balancer_target_group_association(attributes: dict) -> LoadBalancerTargetGroupAssociation:
    load_balancer_arn = attributes['load_balancer_arn']
    target_group_arns = [action['target_group_arn'] for action in attributes['default_action']
                         if action['target_group_arn'] is not None]
    port = attributes['port']
    account = attributes['account_id']
    region = attributes['region']
    return LoadBalancerTargetGroupAssociation(target_group_arns, load_balancer_arn, port, account, region)


def build_load_balancer_target_group(attributes: dict) -> LoadBalancerTargetGroup:
    return LoadBalancerTargetGroup(port=attributes['port'],
                                   protocol=attributes['protocol'],
                                   vpc_id=attributes['vpc_id'],
                                   target_group_arn=attributes['arn'],
                                   target_group_name=attributes['name'],
                                   target_type=attributes['target_type'],
                                   account=attributes['account_id'],
                                   region=attributes['region']).with_aliases(attributes['id'])


def build_load_balancer_target(attributes: dict) -> LoadBalancerTarget:
    return LoadBalancerTarget(port=attributes['port'],
                              target_group_arn=attributes['target_group_arn'],
                              target_id=attributes['target_id'],
                              account=attributes['account_id'],
                              region=attributes['region'])


def build_inline_network_acl_rules(attributes: dict) -> List[NetworkAclRule]:
    rules = []
    egress = attributes['egress']
    ingress = attributes['ingress']
    network_acl_id = attributes['id']
    region = attributes['region']
    account = attributes['account_id']
    if isinstance(egress, list):
        for raw_rule in egress:
            raw_rule['egress'] = True
            raw_rule['network_acl_id'] = network_acl_id
            raw_rule['region'] = region
            raw_rule['account_id'] = account
            rules.append(build_network_acl_rule(raw_rule))
    if isinstance(ingress, list):
        for raw_rule in ingress:
            raw_rule['egress'] = False
            raw_rule['network_acl_id'] = network_acl_id
            raw_rule['region'] = region
            raw_rule['account_id'] = account
            rules.append(build_network_acl_rule(raw_rule))
    return rules


def build_network_acl_rule(attributes: dict):
    ip_protocol_type = IpProtocol(attributes['protocol'])
    if ip_protocol_type.__eq__('ALL'):
        from_port = 0
        to_port = 65535
    else:
        from_port = attributes.get('from_port')
        to_port = attributes.get('to_port')
    return NetworkAclRule(attributes['region'],
                          attributes['account_id'],
                          ip_protocol_type=ip_protocol_type,
                          from_port=from_port,
                          to_port=to_port,
                          cidr_block=_get_known_value(attributes, 'cidr_block'),
                          rule_action=RuleAction(attributes.get('rule_action') or attributes['action']),
                          rule_number=attributes.get('rule_number') or attributes['rule_no'],
                          rule_type=RuleType.OUTBOUND if attributes['egress'] else RuleType.INBOUND,
                          network_acl_id=attributes['network_acl_id'])


def build_network_acl(attributes: dict) -> NetworkAcl:
    return NetworkAcl(network_acl_id=attributes['id'],
                      vpc_id=attributes['vpc_id'],
                      is_default=False,
                      name=_get_name(attributes),
                      subnet_ids=_get_known_value(attributes, 'subnet_ids', []),
                      region=attributes['region'],
                      account=attributes['account_id'])

def build_default_network_acl(attributes: dict) -> NetworkAcl:
    vpc_id = attributes['vpc_id'] if _is_known_value(attributes, 'vpc_id') \
        else attributes['default_network_acl_id'].replace('.default_network_acl_id', '.id')
    return NetworkAcl(network_acl_id=attributes['default_network_acl_id'],
                      vpc_id=vpc_id,
                      is_default=True,
                      name=_get_name(attributes),
                      subnet_ids=_get_known_value(attributes, 'subnet_ids', []),
                      region=attributes['region'],
                      account=attributes['account_id']).with_aliases(attributes['id'])


def build_network_interface(attributes: dict) -> NetworkInterface:
    private_ip = _get_known_value(attributes, 'private_ip')
    private_ips = [ip for ip in _get_known_value(attributes, 'private_ips', []) if ip != private_ip]
    security_groups_ids = _get_known_value(attributes, 'security_groups', [])
    return NetworkInterface(eni_id=attributes['id'],
                            subnet_id=attributes['subnet_id'],
                            security_groups_ids=security_groups_ids,
                            primary_ip_address=private_ip,
                            secondary_ip_addresses=private_ips,
                            public_ip_address=None,
                            ipv6_ip_addresses=[],
                            description=attributes['description'],
                            is_primary=True,
                            availability_zone=None,
                            account=attributes['account_id'],
                            region=attributes['region'])


def build_s3_policy(attributes: dict) -> S3Policy:
    return S3Policy(account=attributes['account_id'],
                    bucket_name=attributes['bucket'],
                    statements=_build_policy_statements_from_str(attributes, 'policy'),
                    raw_document=_get_known_value(attributes, 'policy'))

def build_inline_s3_policy(attributes: dict) -> Optional[S3Policy]:
    if _is_known_value(attributes, 'policy') :
        return build_s3_policy(attributes)
    else:
        return None

def build_managed_policy(attributes: dict) -> ManagedPolicy:
    return ManagedPolicy(account=attributes['account_id'],
                         policy_id=attributes.get('policy_id'),
                         policy_name=attributes['name'],
                         arn=attributes['arn'],
                         statements=_build_policy_statements_from_str(attributes, 'policy'),
                         raw_document=_get_known_value(attributes, 'policy'))


def build_role_inline_policy(attributes: dict) -> InlinePolicy:
    return InlinePolicy(account=attributes['account_id'],
                        policy_name=attributes['name'],
                        owner_name=attributes['role'],
                        statements=_build_policy_statements_from_str(attributes, 'policy'),
                        raw_document=_get_known_value(attributes, 'policy'))


def build_iam_role_nested_policy(attributes: dict) -> InlinePolicy:
    if _get_known_value(attributes, 'inline_policy') and _get_known_value(attributes['inline_policy'][0], 'policy'):
        inline_role_policy = attributes['inline_policy'][0]
        return InlinePolicy(account=attributes['account_id'],
                            owner_name=attributes['id'],
                            policy_name=inline_role_policy['name'],
                            statements=_build_policy_statements_from_str(inline_role_policy, 'policy'),
                            raw_document=_get_known_value(inline_role_policy, 'policy'))
    return None


def build_group_inline_policy(attributes: dict) -> InlinePolicy:
    return InlinePolicy(account=attributes['account_id'],
                        owner_name=attributes['group'],
                        policy_name=attributes['name'],
                        statements=_build_policy_statements_from_str(attributes, 'policy'),
                        raw_document=_get_known_value(attributes, 'policy'))


def build_user_inline_policy(attributes: dict) -> InlinePolicy:
    return InlinePolicy(account=attributes['account_id'],
                        owner_name=attributes['user'],
                        policy_name=attributes['name'],
                        statements=_build_policy_statements_from_str(attributes, 'policy'),
                        raw_document=_get_known_value(attributes, 'policy'), )


def build_iam_group_membership(attributes: dict) -> IamGroupMembership:
    return IamGroupMembership(account=attributes['account_id'],
                              name=attributes['name'],
                              group=attributes['group'],
                              users=attributes['users'])


def build_iam_user_group_membership(attributes: dict) -> IamUserGroupMembership:
    return IamUserGroupMembership(account=attributes['account_id'],
                                  groups=attributes['groups'],
                                  user=attributes['user'])


def build_iam_instance_profile(attributes: dict) -> IamInstanceProfile:
    return IamInstanceProfile(account=attributes['account_id'],
                              region=attributes['region'],
                              role_name=attributes['role'],
                              iam_instance_profile_name=attributes['name'])


def build_route_table(attributes: dict) -> RouteTable:
    return RouteTable(route_table_id=attributes['id'],
                      vpc_id=attributes['vpc_id'],
                      name=_get_name(attributes),
                      region=attributes['region'],
                      account=attributes['account_id'],
                      is_main_route_table=False)


def build_default_route_table(attributes: dict) -> RouteTable:
    vpc_id = attributes['vpc_id'] if _is_known_value(attributes, 'vpc_id') \
        else attributes['default_route_table_id'].replace('.default_route_table_id', '.id').replace('.main_route_table_id', '.id')
    return RouteTable(route_table_id=attributes['default_route_table_id'],
                      vpc_id=vpc_id,
                      name=_get_name(attributes),
                      region=attributes['region'],
                      account=attributes['account_id'],
                      is_main_route_table=True).with_aliases(attributes['id'])


def build_route_table_associations(attributes: dict) -> RouteTableAssociation:
    route_table_id = attributes['route_table_id']
    subnet_id = attributes['subnet_id']
    return RouteTableAssociation(attributes['id'], subnet_id, route_table_id, attributes['region'], attributes['account_id'])


def build_main_route_table_association(attributes: dict) -> MainRouteTableAssociation:
    route_table_id = attributes['route_table_id']
    vpc_id = attributes['vpc_id']
    account = attributes['account_id']
    region = attributes['region']
    return MainRouteTableAssociation(vpc_id, route_table_id, account, region)


def build_inline_routes(raw_routes: dict, route_table_id: str, region: str, account: str) -> List[Route]:
    routes = []
    if not isinstance(raw_routes, list):
        return routes
    for raw_route in raw_routes:
        raw_route['route_table_id'] = route_table_id
        raw_route['region'] = region
        raw_route['account_id'] = account
        route = build_route(raw_route)
        routes.append(route)
    return routes


def build_route(attributes: dict) -> Route:
    route_table_id = attributes['route_table_id']
    cidr = _get_known_value(attributes, 'destination_cidr_block') or \
           _get_known_value(attributes, 'destination_ipv6_cidr_block') or \
           _get_known_value(attributes, 'cidr_block') or \
           _get_known_value(attributes, 'ipv6_cidr_block')
    route_key = None
    route_value = None
    if _is_known_value(attributes, 'gateway_id'):
        route_key = RouteTargetType.GATEWAY_ID
        route_value = attributes['gateway_id']
    if _is_known_value(attributes, 'nat_gateway_id'):
        route_key = RouteTargetType.NAT_GATEWAY_ID
        route_value = attributes['nat_gateway_id']
    if _is_known_value(attributes, 'instance_id'):
        route_key = RouteTargetType.INSTANCE_ID
        route_value = attributes['instance_id']
    if _is_known_value(attributes, 'egress_only_gateway_id'):
        route_key = RouteTargetType.EGRESS_ONLY_GATEWAY_ID
        route_value = attributes['egress_only_gateway_id']
    if _is_known_value(attributes, 'transit_gateway_id'):
        route_key = RouteTargetType.TRANSIT_GATEWAY_ID
        route_value = attributes['transit_gateway_id']
    if _is_known_value(attributes, 'vpc_peering_connection_id'):
        route_key = RouteTargetType.VPC_PEERING_ID
        route_value = attributes['vpc_peering_connection_id']

    return Route(route_table_id, cidr, route_key, route_value, attributes['region'], attributes['account_id'])


def build_s3_bucket(attributes: dict) -> S3Bucket:
    arn = build_arn('s3', None, None, None, None, attributes['bucket'])
    return S3Bucket(account=attributes['account_id'],
                    bucket_name=attributes['bucket'],
                    arn=arn,
                    region=attributes['region']) \
        .with_aliases(attributes['id'], attributes['bucket_regional_domain_name'])


def build_s3_acl(attributes: dict) -> List[S3ACL]:
    """
    Builds S3ACL object based on logic found on `AWS ACL overview page <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html>`_
    """
    bucket_name = attributes['bucket']
    grants_raw = attributes['grant']
    account = attributes['account_id']
    region = attributes['region']
    if grants_raw:
        grant_acls: List[S3ACL] = []
        for grant_raw in grants_raw:
            grantee_type = GranteeTypes(grant_raw['type'])
            grantee_value = GranteeTypes.get_type_value(grantee_type, grant_raw)
            for permission in grant_raw['permissions']:
                grant_acls.append(S3ACL(S3Permission[permission], grantee_type, grantee_value, bucket_name, account, region))
        return grant_acls
    else:
        canned_acl = attributes['acl']
        if canned_acl == 'public-read':
            return [S3ACL(S3Permission['READ'], GranteeTypes.GROUP, S3PredefinedGroups.ALL_USERS.value, bucket_name, account, region)]
        if canned_acl == 'public-read-write':
            return [S3ACL(S3Permission['READ'], GranteeTypes.GROUP, S3PredefinedGroups.ALL_USERS.value, bucket_name, account, region),
                    S3ACL(S3Permission['WRITE'], GranteeTypes.GROUP, S3PredefinedGroups.ALL_USERS.value, bucket_name, account, region)]
        if canned_acl == 'authenticated-read':
            return [S3ACL(S3Permission['READ'], GranteeTypes.GROUP, S3PredefinedGroups.AUTHENTICATED_USERS.value, bucket_name, account, region)]
        if canned_acl == 'log-delivery-write':
            return [S3ACL(S3Permission['WRITE'], GranteeTypes.GROUP, S3PredefinedGroups.LOG_DELIVERY.value, bucket_name, account, region),
                    S3ACL(S3Permission['READ_ACP'], GranteeTypes.GROUP, S3PredefinedGroups.LOG_DELIVERY.value, bucket_name, account, region)]
        return []


def build_s3_access_point(attributes: dict) -> S3BucketAccessPoint:
    return S3BucketAccessPoint(bucket_name=attributes['bucket'],
                               name=attributes['name'],
                               arn=attributes['arn'],
                               region=attributes['region'],
                               account=attributes['account_id'],
                               network_origin=_get_network_origin(
                                   attributes['network_origin'],
                                   attributes['vpc_configuration']),
                               policy=S3AccessPointPolicy(attributes['account_id'],
                                                          attributes['region'],
                                                          attributes['name'],
                                                          _build_policy_statements_from_str(attributes, 'policy'),
                                                          _get_known_value(attributes, 'policy')))


def build_s3_public_access_block_settings(attributes: dict) -> PublicAccessBlockSettings:
    level: PublicAccessBlockLevel = get_dict_value(attributes, "access_level", PublicAccessBlockLevel.BUCKET)
    bucket_name_or_account_id = attributes['bucket'] if level == PublicAccessBlockLevel.BUCKET else attributes['account_id']
    return PublicAccessBlockSettings(bucket_name_or_account_id=bucket_name_or_account_id,
                                     block_public_acls=attributes['block_public_acls'],
                                     block_public_policy=attributes['block_public_policy'],
                                     ignore_public_acls=attributes['ignore_public_acls'],
                                     restrict_public_buckets=attributes['restrict_public_buckets'],
                                     access_level=level,
                                     account=attributes['account_id'],
                                     region=attributes['region'])


def build_inline_security_group_rules(attributes: dict) -> List[SecurityGroupRule]:
    rules = []
    egress = _get_known_value(attributes, 'egress')
    ingress = _get_known_value(attributes, 'ingress')
    security_group_id = attributes['id']
    region = attributes['region']
    account = attributes['account_id']
    if egress:
        for raw_rule in egress:
            raw_rule['type'] = 'egress'
            raw_rule['security_group_id'] = security_group_id
            raw_rule['region'] = region
            raw_rule['account_id'] = account
            rules.extend(build_security_group_rule(raw_rule))
    if ingress:
        for raw_rule in ingress:
            raw_rule['type'] = 'ingress'
            raw_rule['security_group_id'] = security_group_id
            raw_rule['region'] = region
            raw_rule['account_id'] = account
            rules.extend(build_security_group_rule(raw_rule))
    return rules


def build_security_group_rule(attributes: dict) -> List[SecurityGroupRule]:
    security_group_id = attributes['security_group_id']
    ip_protocol = IpProtocol(attributes['protocol'])
    from_port: int
    to_port: int
    if ip_protocol == IpProtocol.ALL:
        from_port = 0
        to_port = 65535
    else:
        from_port = int(attributes.get('from_port'))
        to_port = int(attributes.get('to_port'))
    region = attributes['region']
    account = attributes['account_id']
    connection_type = ConnectionType.INBOUND if attributes['type'] == 'ingress' else ConnectionType.OUTBOUND
    rules: List[SecurityGroupRule] = []
    cidr_blocks = _get_known_value(attributes, 'cidr_blocks', [])
    has_description = bool(_get_known_value(attributes, 'description_hashcode'))
    # pylint: disable=E0601
    # (Due to pylint not fully-supporting walrus operator)
    source_security_group_id = [source] if \
        (source := _get_known_value(attributes, 'source_security_group_id')) else None or \
                                                                                  _get_known_value(attributes, 'security_groups', [security_group_id])

    if not cidr_blocks:
        for source_sg in source_security_group_id:
            property_type = SecurityGroupRulePropertyType.SECURITY_GROUP_ID
            property_value = source_sg
            rules.append(SecurityGroupRule(
                from_port, to_port, ip_protocol, property_type, property_value, has_description,
                connection_type, security_group_id, region, account))
    for cidr_block in cidr_blocks:
        property_type = SecurityGroupRulePropertyType.IP_RANGES
        property_value = cidr_block
        rules.append(
            SecurityGroupRule(from_port, to_port, ip_protocol, property_type, property_value, has_description, connection_type,
                              security_group_id, region, account))
    return rules


def build_security_group(attributes: dict, is_default: bool) -> SecurityGroup:
    has_description = True
    if not is_default:
        has_description = attributes.get('description_hashcode') and \
                          attributes.get('description_hashcode') != hash_utils.to_hashcode('Managed by Terraform', attributes.get('salt'))
    return SecurityGroup(security_group_id=attributes['id'], region=attributes['region'], account=attributes['account_id'],
                         name=attributes.get('name') or _get_name(attributes),
                         vpc_id=_get_known_value(attributes, 'vpc_id'), is_default=is_default, has_description=has_description)


def build_subnet(attributes: dict) -> Subnet:
    return Subnet(subnet_id=attributes['id'],
                  vpc_id=attributes.get('vpc_id'),
                  cidr_block=attributes['cidr_block'],
                  name=_get_name(attributes),
                  availability_zone=attributes.get('availability_zone'),
                  map_public_ip_on_launch=attributes.get('map_public_ip_on_launch'),
                  region=attributes['region'],
                  is_default=attributes["is_default"],
                  account=attributes['account_id'])


def build_peering_connection(attributes: dict) -> PeeringConnection:
    return PeeringConnection(
        peering_id=attributes['id'],
        status=_get_known_value(attributes, 'accept_status'),
        accepter_vpc_info=PeeringVpcInfo(_get_known_value(attributes, 'peer_vpc_id'), []),
        requester_vpc_info=PeeringVpcInfo(_get_known_value(attributes, 'vpc_id'), []),
        region=attributes['region'],
        account=attributes['account_id']
    )


def build_transit_gateway(attributes: dict) -> TransitGateway:
    return TransitGateway(name=_get_name(attributes),
                          tgw_id=attributes['id'],
                          state='available',
                          region=attributes['region'],
                          account=attributes['account_id'])


def build_transit_gateway_route(attributes: dict) -> TransitGatewayRoute:
    return TransitGatewayRoute(destination_cidr_block=attributes['destination_cidr_block'],
                               state=_get_transit_gateway_route_state(attributes['blackhole']),
                               route_type=TransitGatewayRouteType.STATIC,
                               route_table_id=attributes['transit_gateway_route_table_id'],
                               region=attributes['region'],
                               account=attributes['account_id'])


def build_transit_gateway_route_table(attributes: dict) -> TransitGatewayRouteTable:
    return TransitGatewayRouteTable(tgw_id=attributes['transit_gateway_id'],
                                    route_table_id=attributes['id'],
                                    region=attributes['region'],
                                    account=attributes['account_id'])


def build_transit_gateway_attachments(attributes: dict) -> TransitGatewayVpcAttachment:
    return TransitGatewayVpcAttachment(transit_gateway_id=attributes['transit_gateway_id'],
                                       attachment_id=attributes['id'],
                                       state='available',
                                       resource_type=TransitGatewayResourceType.VPC,
                                       resource_id=attributes['vpc_id'],
                                       name=_get_name(attributes),
                                       subnet_ids=attributes['subnet_ids'],
                                       region=attributes['region'],
                                       account=attributes['account_id'])


def build_transit_gateway_route_table_association(attributes: dict) -> TransitGatewayRouteTableAssociation:
    return TransitGatewayRouteTableAssociation(attributes['transit_gateway_attachment_id'],
                                               attributes['transit_gateway_route_table_id'],
                                               attributes['region'],
                                               attributes['account_id'])


def build_transit_gateway_route_table_propagation(attributes: dict) -> TransitGatewayRouteTablePropagation:
    return TransitGatewayRouteTablePropagation(attributes['transit_gateway_attachment_id'],
                                               attributes['transit_gateway_route_table_id'],
                                               attributes['region'],
                                               attributes['account_id'])


def build_vpc_attribute(raw_data: dict, assign_default_values: bool) -> List[VpcAttribute]:
    account: str = raw_data['account_id']
    region: str = raw_data['region']
    vpc_id: str = raw_data['id']
    enable_dns_support = _get_known_value(raw_data, 'enable_dns_support', True if assign_default_values else None)
    enable_dns_hostnames = _get_known_value(raw_data, 'enable_dns_hostnames', False if assign_default_values else None)
    return [VpcAttribute(account, region, vpc_id, 'EnableDnsSupport', enable_dns_support),
            VpcAttribute(account, region, vpc_id, 'EnableDnsHostnames', enable_dns_hostnames)]


def build_vpc(attributes: dict) -> Vpc:
    name = _get_name(attributes)
    ipv6_cidr_block = []
    if _get_known_value(attributes, 'assign_generated_ipv6_cidr_block'):
        ipv6_cidr_block = [attributes.get('ipv6_cidr_block')]
    return Vpc(vpc_id=attributes.get('id'),
               cidr_block=[attributes.get('cidr_block')],  # TODO: What cidr is assigned when this is blank?
               ipv6_cidr_block=ipv6_cidr_block,
               name=name,
               region=attributes['region'],
               account=attributes['account_id'],
               friendly_name=name,
               is_default=False) \
        .with_raw_data(attributes.get('main_route_table_id'),
                       attributes.get('default_route_table_id'),
                       attributes.get('default_security_group_id'))


def build_internet_gateway(attributes: dict) -> InternetGateway:
    return InternetGateway(tf_resource_type=attributes["tf_res_type"], vpc_id=attributes.get('vpc_id'),
                           igw_id=attributes.get('id'),
                           igw_type=attributes["igw_type"],
                           region=attributes['region'],
                           account=attributes['account_id'])


def build_vpc_gateway_attachment(attributes: dict) -> VpcGatewayAttachment:
    return VpcGatewayAttachment(gateway_id=attributes.get('id'),
                                vpc_id=attributes["vpc_id"],
                                region=attributes['region'],
                                account=attributes['account_id'])


def build_vpc_endpoint(attributes: dict) -> VpcEndpoint:
    service_name = attributes['service_name']
    region = attributes['region']
    account = attributes['account_id']
    vpc_id = attributes['vpc_id']
    state = attributes['state']
    vpce_id = attributes['id']
    full_access_statements: List[PolicyStatement] = [ALL_SERVICES_PUBLIC_FULL_ACCESS]
    full_access_policy: Policy = Policy(account, full_access_statements)
    policy = _build_policy(account, safe_json_loads(attributes['policy'])) \
        if _is_known_value(attributes, 'policy') else full_access_policy
    vpce_type: str = attributes['vpc_endpoint_type'] if 'vpc_endpoint_type' in attributes else 'Gateway'
    vpc_endpoint: VpcEndpoint

    if vpce_type == 'Gateway':
        vpc_endpoint_gateway: VpcEndpointGateway = VpcEndpointGateway(region=region,
                                                                      vpc_id=vpc_id,
                                                                      account=account,
                                                                      service_name=service_name,
                                                                      state=state,
                                                                      policy=policy,
                                                                      vpce_id=vpce_id)
        if isinstance(attributes['route_table_ids'], list):
            vpc_endpoint_gateway.route_table_ids = attributes['route_table_ids']
        vpc_endpoint = vpc_endpoint_gateway
    else:
        vpc_endpoint_interface: VpcEndpointInterface = VpcEndpointInterface(region=region,
                                                                            vpc_id=vpc_id,
                                                                            account=account,
                                                                            service_name=service_name,
                                                                            state=state,
                                                                            policy=policy,
                                                                            vpce_id=vpce_id)

        if isinstance(attributes['subnet_ids'], list):
            vpc_endpoint_interface.subnet_ids = attributes['subnet_ids']
        if isinstance(attributes['security_group_ids'], list):
            vpc_endpoint_interface.security_group_ids = attributes['security_group_ids']
        if isinstance(attributes['network_interface_ids'], list):
            vpc_endpoint_interface.network_interface_ids = attributes['network_interface_ids']
        vpc_endpoint = vpc_endpoint_interface

    if policy is None:
        vpc_endpoint.add_invalidation("failed to parse vpc endpoint policy")
    return vpc_endpoint


def build_policy_role_attachment(attributes: dict) -> PolicyRoleAttachment:
    return PolicyRoleAttachment(account=attributes['account_id'],
                                role_name=attributes['role'],
                                policy_arn=attributes['policy_arn'])


def build_policy_group_attachment(attributes: dict) -> PolicyGroupAttachment:
    return PolicyGroupAttachment(account=attributes['account_id'],
                                 group_id=attributes['group'],
                                 policy_arn=attributes['policy_arn'],
                                 group_name=attributes['group'])


def build_policy_user_attachment(attributes: dict) -> PolicyUserAttachment:
    return PolicyUserAttachment(account=attributes['account_id'],
                                user_id=attributes['user'],
                                policy_arn=attributes['policy_arn'],
                                user_name=attributes['user'])


def build_launch_configuration(attributes: dict) -> LaunchConfiguration:
    return LaunchConfiguration(arn=attributes['arn'],
                               image_id=attributes['image_id'],
                               instance_type=attributes['instance_type'],
                               key_name=attributes['key_name'],
                               name=attributes['name'],
                               security_group_ids=attributes['security_groups'],
                               http_tokens='optional',
                               iam_instance_profile=_get_known_value(attributes, 'iam_instance_profile'),
                               region=attributes['region'],
                               account=attributes['account_id'],
                               associate_public_ip_address=attributes.get('associate_public_ip_address', False),
                               ebs_optimized=_get_known_value(attributes, 'ebs_optimized', False),
                               monitoring_enabled=attributes.get('enable_monitoring')).with_aliases(attributes['id'])


def build_auto_scaling_group(attributes: dict) -> AutoScalingGroup:
    launch_template = l_t[0] if (l_t := _get_known_value(attributes, 'launch_template', {})) else {}  # pylint: disable=E0601

    return AutoScalingGroup(arn=attributes['arn'],
                            target_group_arns=attributes['target_group_arns'] or [],
                            name=attributes['name'],
                            availability_zones=_get_known_value(attributes, 'availability_zones', []),
                            subnet_ids=_get_known_value(attributes, 'vpc_zone_identifier', []),
                            region=attributes['region'],
                            account=attributes['account_id']) \
        .with_raw_data(launch_configuration_name=attributes['launch_configuration'],
                       launch_template_id=launch_template.get('id'),
                       launch_template_version=launch_template.get('version'),
                       launch_template_name=launch_template.get('name'))


def build_redshift_cluster(attributes: dict) -> RedshiftCluster:
    # If cluster_subnet_group_name not provided, then the redshift will be deployed outside a VPC (in an EC2-Classic platform)
    subnet_group_name = _get_known_value(attributes, 'cluster_subnet_group_name')
    vpc_security_group_ids = _get_known_value(attributes, 'vpc_security_group_ids', [])
    return RedshiftCluster(attributes['account_id'],
                           attributes['region'],
                           attributes['database_name'],
                           attributes['cluster_identifier'],
                           attributes['port'],
                           subnet_group_name,
                           vpc_security_group_ids,
                           attributes['publicly_accessible'],
                           get_dict_value(attributes, 'encrypted', False))


def build_redshift_logging(attributes: dict) -> RedshiftLogging:
    logging_enabled = False
    s3_bucket = None
    s3_prefix = None
    logging_config = _get_known_value(attributes, 'logging')
    if logging_config:
        logging_enabled = logging_config[0]['enable']
        s3_bucket = logging_config[0]['bucket_name']
        s3_prefix = logging_config[0]['s3_key_prefix']
    return RedshiftLogging(attributes['account_id'],
                           attributes['region'],
                           attributes['cluster_identifier'],
                           s3_bucket,
                           s3_prefix,
                           logging_enabled)


def build_redshift_subnet_group(attributes: dict) -> RedshiftSubnetGroup:
    return RedshiftSubnetGroup(attributes['name'], attributes['subnet_ids'], attributes['region'], attributes['account_id'])


def build_rds_cluster_instance(attributes: dict) -> RdsInstance:
    return RdsInstance(account=attributes['account_id'],
                       region=attributes['region'],
                       name=attributes['identifier'],
                       arn=attributes['arn'],
                       port=_get_known_value(attributes, "port") or get_port_by_engine(_get_known_value(attributes, "engine") or 'aurora'),
                       publicly_accessible=attributes['publicly_accessible'],
                       db_subnet_group_name=_get_known_value(attributes, "db_subnet_group_name"),
                       security_group_ids=_get_known_value(attributes, "vpc_security_group_ids", []),
                       db_cluster_id=_get_known_value(attributes, 'cluster_identifier'),
                       encrypted_at_rest=get_dict_value(attributes, 'storage_encrypted', False),
                       performance_insights_enabled=_get_known_value(attributes, 'performance_insights_enabled', False),
                       performance_insights_kms_key=_get_known_value(attributes, 'performance_insights_kms_key_id')
                       if _get_known_value(attributes, 'performance_insights_enabled', False) else None,
                       engine_type=_get_known_value(attributes, 'engine', 'aurora'),
                       engine_version=_get_known_value(attributes, 'engine_version'),
                       instance_id=None)


def build_rds_db_instance(attributes: dict) -> RdsInstance:
    rds_instance = RdsInstance(account=attributes['account_id'],
                               region=attributes['region'],
                               name=attributes['identifier'],
                               arn=attributes['arn'],
                               port=_get_known_value(attributes, "port") or get_port_by_engine(_get_known_value(attributes, "engine") or 'aurora'),
                               publicly_accessible=attributes['publicly_accessible'],
                               db_subnet_group_name=_get_known_value(attributes, "db_subnet_group_name"),
                               security_group_ids=_get_known_value(attributes, "vpc_security_group_ids", []),
                               db_cluster_id=None,
                               encrypted_at_rest=get_dict_value(attributes, 'storage_encrypted', False),
                               performance_insights_enabled=_get_known_value(attributes, 'performance_insights_enabled', False),
                               performance_insights_kms_key=_get_known_value(attributes, 'performance_insights_kms_key_id')
                               if _get_known_value(attributes, 'performance_insights_enabled', False) else None,
                               engine_type=_get_known_value(attributes, 'engine', 'mysql'),
                               engine_version=_get_known_value(attributes, 'engine_version'),
                               instance_id=_get_known_value(attributes, 'id'))
    rds_instance.backup_retention_period = _get_known_value(attributes, 'backup_retention_period', 0)
    rds_instance.iam_database_authentication_enabled = _get_known_value(attributes, 'iam_database_authentication_enabled', False)
    rds_instance.cloudwatch_logs_exports = _get_known_value(attributes, 'enabled_cloudwatch_logs_exports')
    return rds_instance


def build_db_subnet_group(attributes: dict) -> DbSubnetGroup:
    return DbSubnetGroup(attributes['name'],
                         attributes['subnet_ids'],
                         attributes['region'],
                         attributes['account_id'],
                         attributes['arn'])


def build_rds_cluster(attributes: dict) -> RdsCluster:
    return RdsCluster(account=attributes['account_id'],
                      region=attributes['region'],
                      cluster_id=attributes['id'],
                      arn=attributes['arn'],
                      port=_get_known_value(attributes, "port") or get_port_by_engine(_get_known_value(attributes, "engine", 'aurora')),
                      db_subnet_group_name=_get_known_value(attributes, "db_subnet_group_name"),
                      security_group_ids=_get_known_value(attributes, "vpc_security_group_ids", []),
                      encrypted_at_rest=_get_known_value(attributes, "storage_encrypted"),
                      backup_retention_period=_get_known_value(attributes, 'backup_retention_period', 1),
                      engine_type=_get_known_value(attributes, 'engine', 'aurora'),
                      engine_version=_get_known_value(attributes, 'engine_version'),
                      iam_database_authentication_enabled=_get_known_value(attributes, 'iam_database_authentication_enabled', False),
                      cloudwatch_logs_exports=_get_known_value(attributes, 'enabled_cloudwatch_logs_exports'))


def build_rds_global_cluster(attributes: dict) -> RdsGlobalCluster:
    if 'storage_encrypted' in attributes.keys():
        encrypted_at_rest_val = _get_known_value(attributes, "storage_encrypted")
    else:
        encrypted_at_rest_val = False
    return RdsGlobalCluster(account=attributes['account_id'],
                            region=attributes['region'],
                            cluster_id=attributes['global_cluster_identifier'],
                            encrypted_at_rest=encrypted_at_rest_val).with_raw_data(_get_known_value(attributes, "source_db_cluster_identifier"))


def _get_network_origin(network_origin: str, vpc_config: List) -> S3BucketAccessPointNetworkOrigin:
    if network_origin is S3BucketAccessPointNetworkOriginType.VPC:
        return S3BucketAccessPointNetworkOrigin(network_origin, vpc_config[0])
    else:
        return S3BucketAccessPointNetworkOrigin(network_origin, '')


def _build_policy(account: str, raw_data: dict) -> Optional[Policy]:
    if raw_data is None:
        return None
    elif 'Statement' in raw_data:
        statements = [build_policy_statement(raw_statement) for raw_statement in raw_data['Statement']]
        return Policy(account, statements)
    else:
        return Policy(account, [])


def _get_transit_gateway_route_state(is_blackhole: bool) -> TransitGatewayRouteState:
    if is_blackhole:
        return TransitGatewayRouteState.BLACKHOLE
    else:
        return TransitGatewayRouteState.ACTIVE


def _get_subnets(route_table_id, route_table_associations):
    subnets = set()
    for route_table_association in route_table_associations:
        if route_table_association['route_table_id'] == route_table_id:
            subnets.add(route_table_association['subnet_id'])
    return list(subnets)


def _get_load_balancer_scheme_type(attributes: dict) -> LoadBalancerSchemeType:
    key: str = "internal"
    if _is_known_value(attributes, key) and attributes[key]:
        return LoadBalancerSchemeType.INTERNAL
    else:
        return LoadBalancerSchemeType.INTERNET_FACING


def _get_name(attributes: dict) -> str:
    tags = _get_known_value(attributes, 'tags_all') or _get_known_value(attributes, 'tags', {})
    return _get_known_value(tags, 'Name')


def _is_known_value(attributes: dict, key: str) -> bool:
    address = attributes.get('tf_address', '')
    value = attributes.get(key)
    return isinstance(value, (bool, int)) or (value and (not isinstance(value, Iterable)
                                                         or not address or address not in value))


def _build_policy_statements_from_str(attributes, key) -> List[PolicyStatement]:
    return build_policy_statements_from_str(_get_known_value(attributes, key))


def _add_resource_for_es_domain_policy_statements(es_policies: List[PolicyStatement],
                                                  account: str, region: str, domain_name: str) -> List[PolicyStatement]:
    for policy in es_policies:
        if len(policy.resources) == 0:
            policy.resources = [f'arn:aws:es:{region}:{account}:domain/{domain_name}/*']
    return es_policies


def _get_known_value(attributes: dict, key: str, default=None):
    return attributes.get(key) if _is_known_value(attributes, key) else default


def build_ecs_cluster(attributes: dict) -> EcsCluster:
    is_container_insights_enabled = True
    if _is_known_value(attributes, 'setting'):
        is_container_insights_enabled = bool(attributes['setting'][0]['value'] == 'enabled')
    cluster: EcsCluster = EcsCluster(account=attributes['account_id'],
                                     region=attributes['region'],
                                     cluster_arn=attributes['arn'],
                                     cluster_id=attributes['id'],
                                     cluster_name=attributes['name'],
                                     is_container_insights_enabled=is_container_insights_enabled)
    return cluster


def build_ecs_service(attributes: dict) -> EcsService:
    network_conf_list: List[NetworkConfiguration] = \
        [NetworkConfiguration(conf["assign_public_ip"], conf["security_groups"], conf["subnets"])
         for conf in attributes["network_configuration"]]

    service: EcsService = EcsService(name=attributes["name"],
                                     launch_type=LaunchType(_get_known_value(attributes, "launch_type", "EC2")),
                                     cluster_arn=attributes["cluster"],
                                     account=attributes['account_id'],
                                     region=attributes['region'],
                                     network_conf_list=network_conf_list,
                                     task_definition_arn=attributes.get('task_definition', None))
    elb_list: dict = attributes["load_balancer"]
    for elb_dict in elb_list:
        elb: LoadBalancingConfiguration = LoadBalancingConfiguration(elb_dict["elb_name"],
                                                                     elb_dict["target_group_arn"],
                                                                     elb_dict["container_name"],
                                                                     elb_dict["container_port"])
        service.add_elb(elb)
    return service


def build_ecs_target(attributes: dict) -> CloudWatchEventTarget:
    ecs_target_list: List[EcsTarget] = []
    counter: int = 1
    for event_target_dict in attributes["ecs_target"]:
        network_conf_list: List[NetworkConfiguration] = \
            [NetworkConfiguration(conf["assign_public_ip"], conf["security_groups"], conf["subnets"])
             for conf in event_target_dict["network_configuration"]]
        target: EcsTarget = EcsTarget(attributes["tf_address"] + str(counter)
                                      if not _is_known_value(attributes, 'arn') else attributes['arn'].split(':')[-1] + '.target.name',
                                      attributes["target_id"],
                                      LaunchType(event_target_dict["launch_type"]),
                                      attributes['account_id'],
                                      attributes['region'],
                                      attributes["arn"],
                                      attributes["role_arn"],
                                      network_conf_list,
                                      event_target_dict.get("task_definition_arn", None))
        ecs_target_list.append(target)
        counter += 1
    if ecs_target_list:
        return CloudWatchEventTarget(account=attributes['account_id'],
                                    region=attributes['region'],
                                    name=attributes["tf_address"] if not _is_known_value(attributes, 'arn') else attributes['arn'].split(':')[-1],
                                    rule_name=attributes["rule"],
                                    target_id=attributes["target_id"],
                                    role_arn=attributes["role_arn"],
                                    cluster_arn=attributes["arn"],
                                    ecs_target_list=ecs_target_list)
    return None

def build_ecs_task_definition(attributes: dict) -> EcsTaskDefinition:
    network_mode: NetworkMode = NetworkMode(_get_known_value(attributes, 'network_mode', 'none'))
    container_definitions: List[ContainerDefinition] = []
    container_definitions_data = safe_json_loads(attributes['container_definitions'])
    if container_definitions_data:
        for container in container_definitions_data:
            port_mappings: List[PortMappings] = []
            for port_map in get_dict_value(container, 'portMappings', []):
                host_port: int = get_dict_value(port_map, 'hostPort', -1)
                container_port: int = get_dict_value(port_map, 'containerPort', -1)
                if network_mode == NetworkMode.AWS_VPC:
                    host_port = container_port
                port_mappings.append(PortMappings(container_port=container_port,
                                                  host_port=host_port,
                                                  protocol=IpProtocol(get_dict_value(port_map, 'protocol', ''))))
            container_definitions.append(ContainerDefinition(container_name=container['name'],
                                                             image=container['image'],
                                                             port_mappings=port_mappings))
    efs_volume_data = []
    for volume in attributes.get('volume', []):
        if volume.get('efs_volume_configuration', []):
            efs_volume_data.append(EfsVolume(volume['name'],
                                             volume['efs_volume_configuration'][0]['file_system_id'],
                                             bool(volume['efs_volume_configuration'][0].get('transit_encryption') == 'ENABLED')))
    ecs_task_definition = EcsTaskDefinition(task_arn=attributes['arn'],
                                            family=attributes['family'],
                                            revision=attributes['revision'],
                                            account=attributes['account_id'],
                                            region=attributes['region'],
                                            task_role_arn=get_dict_value(attributes, 'task_role_arn', None),
                                            execution_role_arn=attributes.get('execution_role_arn', None),
                                            network_mode=network_mode,
                                            container_definitions=container_definitions,
                                            efs_volume_data=efs_volume_data)
    if not ecs_task_definition.container_definitions:
        ecs_task_definition.add_invalidation("failed to retrieve container definitions data")
    return ecs_task_definition


def build_default_vpc(attributes: dict) -> Vpc:
    ipv6_cidr_block = []
    if _get_known_value(attributes, 'assign_generated_ipv6_cidr_block'):
        ipv6_cidr_block = [attributes.get('ipv6_cidr_block')]
    return Vpc(account=attributes['account_id'],
               region=attributes['region'],
               vpc_id=attributes['id'],
               cidr_block=[attributes['cidr_block']],
               name=_get_name(attributes),
               is_default=True,
               ipv6_cidr_block=ipv6_cidr_block) \
        .with_aliases(attributes['id'])


def build_elastic_search_domain(attributes: dict) -> ElasticSearchDomain:
    vpc_options = attributes['vpc_options']
    security_group_ids, subnet_ids = None, None
    if vpc_options:
        security_group_ids = vpc_options[0]['security_group_ids']
        subnet_ids = vpc_options[0]['subnet_ids']

    domain_endpoint_options = _get_known_value(attributes, 'domain_endpoint_options')
    enforce_https = False
    if domain_endpoint_options:
        enforce_https = domain_endpoint_options[0]['enforce_https']

    encrypt_at_rest_state = False
    encrypt_at_rest_options = _get_known_value(attributes, 'encrypt_at_rest')
    if encrypt_at_rest_options:
        encrypt_at_rest_state = encrypt_at_rest_options[0]['enabled']

    encrypt_node_to_node_state = False
    encrypt_node_to_node_options = _get_known_value(attributes, 'node_to_node_encryption')
    if encrypt_node_to_node_options:
        encrypt_node_to_node_state = encrypt_node_to_node_options[0]['enabled']

    log_publishing_options: Optional[List[LogPublishingOptions]] = []
    if _get_known_value(attributes, 'log_publishing_options'):
        for log in attributes['log_publishing_options']:
            log_publishing_options.append(LogPublishingOptions(log['log_type'],
                                                               log['cloudwatch_log_group_arn'],
                                                               log['enabled'] if log['enabled'] is not None else True))
    elasticsearch_version = _get_known_value(attributes, 'elasticsearch_version', '1.5')
    es_domain_cluster_instance_type = 'm4.large.elasticsearch'
    es_cluster_config = _get_known_value(attributes, 'cluster_config')
    if es_cluster_config:
        es_domain_cluster_instance_type = _get_known_value(es_cluster_config[0], 'instance_type', 'm4.large.elasticsearch')
    return_statement = ElasticSearchDomain(attributes['domain_id'],
                                           attributes['domain_name'],
                                           attributes['arn'],
                                           enforce_https,
                                           subnet_ids,
                                           security_group_ids,
                                           encrypt_at_rest_state,
                                           encrypt_node_to_node_state,
                                           attributes['account_id'],
                                           attributes['region'],
                                           log_publishing_options,
                                           elasticsearch_version,
                                           es_domain_cluster_instance_type)

    if not _get_known_value(attributes, 'access_policies'):
        return return_statement
    else:
        policy = _build_policy_statements_from_str(attributes, 'access_policies')
        _add_resource_for_es_domain_policy_statements(policy, attributes['account_id'], attributes['region'], attributes['domain_name'])
        return_statement.resource_based_policy = ElasticSearchDomainPolicy(attributes['domain_name'],
                                                                           policy,
                                                                           _get_known_value(attributes, 'access_policies'),
                                                                           attributes['account_id'])
        return return_statement


def build_load_balancer_listener(attributes: dict) -> LoadBalancerListener:
    default_action_type = attributes['default_action'][0]['type']
    redirect_action_protocol = None
    redirect_action_port = None
    if default_action_type.lower() == 'redirect':
        redirect_action_protocol = attributes['default_action'][0]['redirect'][0]['protocol']
        redirect_action_port = attributes['default_action'][0]['redirect'][0]['port']
    return LoadBalancerListener(listener_port=attributes['port'],
                                listener_protocol=attributes['protocol'],
                                listener_arn=attributes['arn'],
                                load_balancer_arn=attributes['load_balancer_arn'],
                                account=attributes['account_id'],
                                region=attributes['region'],
                                default_action_type=default_action_type,
                                redirect_action_protocol=redirect_action_protocol,
                                redirect_action_port=redirect_action_port)


def build_eks_cluster(attributes: dict) -> EksCluster:
    vpc_config = attributes['vpc_config'][0]
    public_access_cidrs = get_dict_value(vpc_config, 'public_access_cidrs', ['0.0.0.0/0'])
    security_group_ids = get_dict_value(vpc_config, 'security_group_ids', [])
    subnet_ids = get_dict_value(vpc_config, 'subnet_ids', [])
    endpoint_public_access = get_dict_value(vpc_config, 'endpoint_public_access', True)
    endpoint_private_access = get_dict_value(vpc_config, 'endpoint_private_access', False)

    return EksCluster(attributes['name'],
                      attributes['arn'],
                      attributes['role_arn'],
                      attributes['endpoint'],
                      security_group_ids,
                      vpc_config.get('cluster_security_group_id'),
                      subnet_ids,
                      endpoint_public_access,
                      endpoint_private_access,
                      public_access_cidrs,
                      attributes['account_id'],
                      attributes['region'])


def build_cloudfront_distribution_list(attributes: dict) -> CloudFrontDistribution:
    viewer_cert_dict = attributes['viewer_certificate'][0]  # must be only one
    viewer_cert: ViewerCertificate = ViewerCertificate(cloudfront_default_certificate=viewer_cert_dict['cloudfront_default_certificate'],
                                                       minimum_protocol_version=get_dict_value(viewer_cert_dict, 'minimum_protocol_version', 'TLSv1'))
    cache_behavior_list: List[CacheBehavior] = []
    order: int = 0
    for cache_behavior_dict in attributes['default_cache_behavior'] + get_dict_value(attributes, 'ordered_cache_behavior', []):
        cache_behavior: CacheBehavior = CacheBehavior(allowed_methods=cache_behavior_dict['allowed_methods'],
                                                      cached_methods=cache_behavior_dict['cached_methods'],
                                                      target_origin_id=cache_behavior_dict['target_origin_id'],
                                                      viewer_protocol_policy=cache_behavior_dict['viewer_protocol_policy'],
                                                      trusted_signers=cache_behavior_dict.get('trusted_signers', []),
                                                      precedence=order,
                                                      field_level_encryption_id=cache_behavior_dict.get('field_level_encryption_id'))

        if 'path_pattern' in cache_behavior_dict:
            cache_behavior.path_pattern = cache_behavior_dict['path_pattern']
        cache_behavior_list.append(cache_behavior)
        order += 1

    origin_config_list: List[OriginConfig] = []
    for origin_dict in attributes['origin']:
        oai_path: str = origin_dict['s3_origin_config'][0]['origin_access_identity'] if origin_dict['s3_origin_config'] else None
        origin_config: OriginConfig = OriginConfig(domain_name=origin_dict['domain_name'],
                                                   origin_id=origin_dict['origin_id'],
                                                   oai_path=oai_path)
        origin_config_list.append(origin_config)
    web_acl_id = attributes['web_acl_id']
    return CloudFrontDistribution(attributes['arn'],
                                  attributes['domain_name'],
                                  attributes['id'],
                                  attributes['account_id'],
                                  viewer_cert,
                                  cache_behavior_list,
                                  origin_config_list,
                                  web_acl_id)


def build_cloudfront_distribution_logging(attributes: dict) -> CloudfrontDistributionLogging:
    include_cookies = False
    s3_bucket = None
    prefix = None
    logging_enabled = False
    logging_config = _get_known_value(attributes, 'logging_config')
    if logging_config:
        include_cookies = _get_known_value(logging_config[0], 'include_cookies', False)
        s3_bucket = attributes['logging_config'][0]['bucket']
        prefix = _get_known_value(logging_config[0], 'prefix', None)
        logging_enabled = True
    return CloudfrontDistributionLogging(attributes['arn'],
                                         attributes['domain_name'],
                                         attributes['id'],
                                         attributes['account_id'],
                                         include_cookies,
                                         s3_bucket,
                                         prefix,
                                         logging_enabled)


def origin_access_identity_builder(attributes: dict) -> OriginAccessIdentity:
    return OriginAccessIdentity(attributes['account_id'], attributes['region'], attributes['id'],
                                attributes['cloudfront_access_identity_path'], attributes['iam_arn'],
                                attributes['s3_canonical_user_id'])


def build_elastic_ip(attributes: dict) -> ElasticIp:
    return ElasticIp(attributes['id'],
                     _get_known_value(attributes, 'public_ip'),
                     _get_known_value(attributes, 'private_ip'),
                     attributes['region'],
                     attributes['account_id'])


def build_launch_template(attributes: dict) -> LaunchTemplate:
    metadata_options = _get_known_value(attributes, 'metadata_options')
    ebs_optimized = bool(_get_known_value(attributes, 'ebs_optimized') == 'true')
    instance_type = attributes.get('instance_type')
    monitoring_enabled = False
    if _get_known_value(attributes, 'monitoring'):
        monitoring_enabled = attributes['monitoring'][0]['enabled']
    http_tokens = 'optional'
    if metadata_options:
        http_tokens = _get_known_value(metadata_options[0], 'http_tokens')
    security_group_ids = _get_known_value(attributes, 'vpc_security_group_ids') or _get_known_value(attributes, 'security_group_names') or []
    version = _get_known_value(attributes, 'latest_version', 1)
    network_configurations: List[NetworkConfiguration] = []
    for net_conf in get_dict_value(attributes, 'network_interfaces', []):
        assign_public_ip: Optional[bool] = get_dict_value(net_conf, 'associate_public_ip_address', None)
        security_groups: List[str] = get_dict_value(net_conf, 'security_groups', [])
        subnet_id: str = get_dict_value(net_conf, 'subnet_id', None)
        network_configurations.append(NetworkConfiguration(assign_public_ip=assign_public_ip, security_groups_ids=security_groups,
                                                           subnet_list_ids=[subnet_id] if subnet_id else []))

    return LaunchTemplate(template_id=attributes['id'], name=attributes['name'], http_token=http_tokens,
                          image_id=attributes['image_id'], security_group_ids=security_group_ids, version_number=version,
                          region=attributes["region"], account=attributes['account_id'],
                          iam_instance_profile=_get_known_value(attributes, 'iam_instance_profile'), network_configurations=network_configurations,
                          ebs_optimized=ebs_optimized, monitoring_enabled=monitoring_enabled, instance_type=instance_type)


def build_athena_workgroup(attributes: dict) -> AthenaWorkgroup:
    encryption_config = None
    kms_key = None
    encryption_option = None
    result_configuration = attributes['configuration'][0].get('result_configuration')

    if result_configuration:
        encryption_config = result_configuration[0].get('encryption_configuration')

    if encryption_config:
        encryption_option = encryption_config[0].get('encryption_option')
        kms_key = encryption_config[0].get('kms_key_arn') if encryption_config[0].get('kms_key_arn') else None
        if is_valid_arn(kms_key):
            kms_key = kms_key.split('/')[1]

    return AthenaWorkgroup(attributes['name'],
                           attributes['state'],
                           bool(encryption_config),
                           attributes['configuration'][0]['enforce_workgroup_configuration'],
                           encryption_option,
                           kms_key,
                           attributes['region'],
                           attributes['account_id'])


def build_rest_api_gw(attributes: dict) -> RestApiGw:
    agw_type = get_dict_value(attributes, 'endpoint_configuration', {})
    if agw_type:
        agw_type = get_dict_value(agw_type[0], 'types', [])
        agw_type = agw_type[0] if agw_type else 'EDGE'
        agw_type = ApiGatewayType(agw_type)
    else:
        agw_type = ApiGatewayType.EDGE
    rest_api_gw = RestApiGw(attributes['id'], attributes['name'], attributes['region'], attributes['account_id'], agw_type)
    if _get_known_value(attributes, 'policy'):
        rest_api_gw.resource_based_policy = rest_api_gw.assign_policy_data_for_tf(_build_policy_statements_from_str(attributes, 'policy'),
                                                                                  _get_known_value(attributes, 'policy'),
                                                                                  attributes['id'])
    return rest_api_gw


def build_api_gateway_method_settings(attributes: dict) -> ApiGatewayMethodSettings:
    caching_enabled = get_dict_value(attributes['settings'][0], 'caching_enabled', False)
    caching_encrypted = get_dict_value(attributes['settings'][0], 'cache_data_encrypted', False)
    method_path = attributes['method_path']
    http_method = method_path.split('/')[-1]
    http_method = RestApiMethod.ANY if http_method == '*' else RestApiMethod(http_method)
    return ApiGatewayMethodSettings(attributes['rest_api_id'],
                                    attributes['stage_name'],
                                    method_path,
                                    http_method,
                                    caching_enabled,
                                    caching_encrypted,
                                    attributes['region'],
                                    attributes['account_id'])


def build_api_gateway_method(attributes: dict) -> ApiGatewayMethod:
    return ApiGatewayMethod(account=attributes['account_id'], region=attributes['region'],
                            rest_api_id=attributes['rest_api_id'], resource_id=attributes['resource_id'],
                            http_method=RestApiMethod(attributes['http_method']),
                            authorization=attributes['authorization'])


def build_api_gateway_integration(attributes: dict) -> ApiGatewayIntegration:
    region: str = attributes['region']
    account_id = attributes['account_id']
    integration_http_method = attributes['integration_http_method']
    integration_http_method = integration_http_method if integration_http_method else None
    uri: str = get_dict_value(attributes, 'uri', None)
    if uri and uri.__contains__(AwsServiceName.AWS_LAMBDA_FUNCTION.value):  # currently support only Lambda integration
        lambda_func_arn = build_arn(service='lambda', region=region, account_id=account_id,
                                    resource_type='function', path='',
                                    resource_name=attributes['uri'].split('.')[1])
        uri = build_lambda_function_integration_endpoint_uri(region, lambda_func_arn)
    return ApiGatewayIntegration(account=account_id, region=region,
                                 rest_api_id=attributes['rest_api_id'], resource_id=attributes['resource_id'],
                                 request_http_method=RestApiMethod(attributes['http_method']),
                                 integration_http_method=RestApiMethod(integration_http_method),
                                 integration_type=IntegrationType(attributes['type']),
                                 uri=uri)


def build_api_gateway_stage(attributes: dict) -> ApiGatewayStage:
    access_logs: Optional[AccessLogsSettings] = None
    access_logs_data = _get_known_value(attributes, 'access_log_settings')
    if access_logs_data:
        access_logs = AccessLogsSettings(access_logs_data[0]['destination_arn'], access_logs_data[0]['format'])
    return ApiGatewayStage(attributes['account_id'],
                           attributes['region'],
                           attributes['rest_api_id'],
                           attributes['stage_name'],
                           _get_known_value(attributes, 'xray_tracing_enabled', False),
                           access_logs)


def build_dynamodb_table(attributes: dict) -> DynamoDbTable:
    fields: List[TableField] = [TableField(field_attr["name"], TableFieldType(field_attr["type"])) for field_attr in attributes["attribute"]]
    billing_mode: BillingMode = BillingMode(get_dict_value(attributes, "billing_mode", "PROVISIONED"))
    server_side_encryption = False
    kms_key_id = None
    if _get_known_value(attributes, 'server_side_encryption'):
        server_side_encryption = attributes['server_side_encryption'][0]['enabled']
        kms_key_id = attributes['server_side_encryption'][0].get('kms_key_arn')
    return DynamoDbTable(table_name=attributes["name"], region=attributes["region"], account=attributes['account_id'], table_arn=attributes["arn"],
                         billing_mode=billing_mode,
                         partition_key=attributes["hash_key"], sort_key=attributes.get("range_key"),
                         write_capacity=attributes.get("write_capacity") or 0, read_capacity=attributes.get("read_capacity") or 0,
                         fields_attributes=fields, server_side_encryption=server_side_encryption, kms_key_id=kms_key_id)


def build_nat_gateways(attributes: dict) -> NatGateways:
    return NatGateways(nat_gateway_id=attributes["id"], allocation_id=attributes["allocation_id"],
                       subnet_id=attributes["subnet_id"], eni_id=attributes["network_interface_id"],
                       private_ip=attributes["private_ip"], public_ip=attributes["public_ip"],
                       account=attributes['account_id'], region=attributes['region'])


def _build_ami_data(attributes: dict):
    is_public = False
    if _get_known_value(attributes, 'public'):
        is_public = attributes['public']
    return Ec2Image(attributes['id'],
                    is_public,
                    attributes['region'],
                    attributes['account_id'])


def build_ami(attributes: dict) -> Ec2Image:
    return _build_ami_data(attributes)


def build_ami_copy(attributes: dict) -> Ec2Image:
    return _build_ami_data(attributes)


def build_ami_from_instance(attributes: dict) -> Ec2Image:
    return _build_ami_data(attributes)


def build_dax_cluster(attributes: dict) -> DaxCluster:
    server_side_encryption = False
    if attributes.get('server_side_encryption'):
        server_side_encryption = attributes['server_side_encryption'][0].get('enabled')
    return DaxCluster(attributes['cluster_name'],
                      server_side_encryption,
                      attributes['arn'],
                      attributes['region'],
                      attributes['account_id'])


def build_docdb_cluster(attributes: dict) -> DocumentDbCluster:
    return DocumentDbCluster(attributes.get('cluster_identifier'),
                             get_dict_value(attributes, 'storage_encrypted', False),
                             attributes.get('db_cluster_parameter_group_name'),
                             _get_known_value(attributes, 'kms_key_id'),
                             attributes['region'],
                             attributes['account_id'],
                             attributes['arn'],
                             _get_known_value(attributes, 'enabled_cloudwatch_logs_exports', []))


def build_docdb_cluster_parameter_group(attributes: dict) -> DocDbClusterParameterGroup:
    list_parameters = []
    for parameter in attributes['parameter']:
        list_parameters.append(DocDbClusterParameter(parameter.get('name'), parameter.get('value')))
    return DocDbClusterParameterGroup(list_parameters,
                                      _get_known_value(attributes, 'name'),
                                      attributes['account_id'],
                                      attributes['region']).with_raw_data(attributes.get("id"))


def build_s3_bucket_encryption(attributes: dict) -> S3BucketEncryption:
    encrypted = False
    if attributes['server_side_encryption_configuration']:
        encrypted = True
    return S3BucketEncryption(attributes['bucket'],
                              encrypted,
                              attributes['region'],
                              attributes['account_id'])


def build_s3_bucket_versioning(attributes: dict) -> S3BucketVersioning:
    versioning = False
    if _get_known_value(attributes, 'versioning') is not None and attributes['versioning'][0]['enabled']:
        versioning = True
    return S3BucketVersioning(attributes['bucket'],
                              versioning,
                              attributes['account_id'],
                              attributes['region'])


def build_s3_bucket_object(attributes: dict) -> S3BucketObject:
    encrypted = False
    if attributes['server_side_encryption'] and attributes['server_side_encryption'] in ['AES256', 'aws:kms']:
        encrypted = True
    return S3BucketObject(attributes['bucket'],
                          attributes['key'],
                          encrypted,
                          attributes['account_id'],
                          attributes['region'])


def build_code_build_projects(attributes: dict) -> CodeBuildProject:
    vpc_config: Optional[NetworkConfiguration] = None
    if _get_known_value(attributes, 'vpc_config'):
        vpc_config = NetworkConfiguration(False, attributes['vpc_config'][0]['security_group_ids'],
                                          attributes['vpc_config'][0]['subnets'])
    return CodeBuildProject(attributes['name'],
                            attributes['encryption_key'],
                            attributes['arn'],
                            attributes['account_id'],
                            attributes['region'],
                            vpc_config)


def build_code_build_report_group(attributes: dict) -> CodeBuildReportGroup:
    return CodeBuildReportGroup(attributes['account_id'],
                                attributes['region'],
                                attributes['name'],
                                attributes['export_config'][0]['type'],
                                _get_known_value(attributes['export_config'][0]['s3_destination'][0], 'bucket'),
                                _get_known_value(attributes['export_config'][0]['s3_destination'][0], 'encryption_key'),
                                attributes['export_config'][0]['s3_destination'][0]['encryption_disabled'],
                                attributes['arn'])


def build_cloudtrail(attributes: dict) -> CloudTrail:
    kms_encryption = False
    if attributes['kms_key_id']:
        kms_encryption = True
    return CloudTrail(attributes['name'],
                      kms_encryption,
                      attributes['arn'],
                      attributes['enable_log_file_validation'],
                      attributes['region'],
                      attributes['account_id'],
                      attributes['is_multi_region_trail'])


def build_cloud_watch_log_groups(attributes: dict) -> CloudWatchLogGroup:
    return CloudWatchLogGroup(attributes['name'],
                              attributes.get('kms_key_id'),
                              attributes['arn'],
                              attributes.get('retention_in_days'),
                              attributes['region'],
                              attributes['account_id'])


def build_kms_key(attributes: dict) -> KmsKey:
    kms_key_id = attributes.get('key_id')
    account = attributes['account_id']
    region = attributes['region']
    kms_key_arn = attributes['arn']
    if not is_valid_arn(kms_key_arn):
        kms_key_arn = build_arn('kms', region, account,'key', None, kms_key_arn)
    return KmsKey(kms_key_id,
                  kms_key_arn,
                  KeyManager('CUSTOMER'),
                  region,
                  account)


def build_vpc_endpoint_route_table_association(attributes: dict) -> VpcEndpointRouteTableAssociation:
    return VpcEndpointRouteTableAssociation(attributes['route_table_id'], attributes['vpc_endpoint_id'],
                                            attributes['region'], attributes['account_id'])


def build_sqs_queue(attributes: dict) -> SqsQueue:
    return_statement = SqsQueue(attributes.get('arn'),
                                attributes.get('name'),
                                bool(attributes.get('kms_master_key_id')),
                                attributes['account_id'],
                                attributes['region'],
                                attributes['id'])
    if _get_known_value(attributes, 'policy'):
        return_statement.resource_based_policy = SqsQueuePolicy(attributes.get('name'),
                                                                _build_policy_statements_from_str(attributes, 'policy'),
                                                                _get_known_value(attributes, 'policy'),
                                                                attributes['account_id'])
    if return_statement.encrypted_at_rest:
        return_statement.kms_key = attributes.get('kms_master_key_id')
    return return_statement


def build_elasti_cache_replication_group(attributes: dict) -> ElastiCacheReplicationGroup:
    elacticache_replication_group = ElastiCacheReplicationGroup(attributes['replication_group_id'],
                                                                _get_known_value(attributes, 'at_rest_encryption_enabled', False),
                                                                _get_known_value(attributes, 'transit_encryption_enabled', False),
                                                                attributes['region'],
                                                                attributes['account_id'])
    elacticache_replication_group.subnet_group_name = _get_known_value(attributes, 'subnet_group_name', 'default')
    elacticache_replication_group.elasticache_security_group_ids = _get_known_value(attributes, 'security_group_ids')
    elacticache_replication_group.is_in_default_vpc = elacticache_replication_group.subnet_group_name == 'default' or not \
        elacticache_replication_group.subnet_group_name
    elacticache_replication_group.with_aliases(attributes['id'],
                                               attributes['replication_group_id'] + attributes['account_id'] + attributes['region'])
    return elacticache_replication_group


def build_sns_topic(attributes: dict) -> SnsTopic:
    encrypted_at_rest = False
    sns_topic_resource = SnsTopic(attributes['arn'],
                                  get_dict_value(attributes, 'name', attributes.get('name_prefix')),
                                  encrypted_at_rest,
                                  attributes['region'],
                                  attributes['account_id'])
    if attributes.get('kms_master_key_id'):
        sns_topic_resource.encrypted_at_rest = True
        sns_topic_resource.kms_key = attributes.get('kms_master_key_id')
    return sns_topic_resource


def build_sqs_queue_policy(attributes: dict) -> SqsQueuePolicy:
    policy_statements = _build_policy_statements_from_str(attributes, 'policy')
    return SqsQueuePolicy(attributes['queue_url'].split('/')[-1] if '/' in attributes['queue_url'] else attributes['queue_url'],
                          policy_statements,
                          _get_known_value(attributes, 'policy'),
                          attributes['account_id'])


def build_neptune_cluster(attributes: dict) -> NeptuneCluster:
    neptune_cluster_resource = NeptuneCluster(attributes['cluster_identifier'],
                                              attributes['arn'],
                                              attributes['storage_encrypted'],
                                              attributes['region'],
                                              attributes['account_id'],
                                              attributes['port'],
                                              _get_known_value(attributes, 'neptune_subnet_group_name', 'default'),
                                              _get_known_value(attributes, 'vpc_security_group_ids'),
                                              attributes.get('id'),
                                              _get_known_value(attributes, 'enable_cloudwatch_logs_exports'))
    if attributes.get('kms_key_arn'):
        neptune_cluster_resource.kms_key = attributes.get('kms_key_arn')
    return neptune_cluster_resource


def build_neptune_instance(attributes: dict) -> NeptuneInstance:
    return NeptuneInstance(attributes['account_id'],
                           attributes['region'],
                           attributes.get('identifier'),
                           attributes.get('arn'),
                           attributes['port'],
                           attributes.get('cluster_identifier'),
                           attributes['publicly_accessible'],
                           attributes.get('identifier'))


def build_ecr_repository(attributes: dict) -> EcrRepository:
    is_image_scan_on_push = False
    if len(attributes['image_scanning_configuration']) > 0 and attributes['image_scanning_configuration'][0].get('scan_on_push'):
        is_image_scan_on_push = attributes['image_scanning_configuration'][0]['scan_on_push']
    encryption_type = 'AES256'
    kms_key_id = None
    encryption_settings = _get_known_value(attributes, 'encryption_configuration')
    if encryption_settings:
        encryption_type = 'AES256' if encryption_settings[0].get('encryption_type') is None else encryption_settings[0]['encryption_type']
        kms_key_id = _get_known_value(encryption_settings[0], 'kms_key')
    return EcrRepository(attributes['name'],
                         attributes['arn'],
                         attributes['region'],
                         attributes['account_id'],
                         attributes['image_tag_mutability'],
                         is_image_scan_on_push,
                         encryption_type,
                         kms_key_id)


def build_ecr_repository_policy(attributes: dict) -> EcrRepositoryPolicy:
    return EcrRepositoryPolicy(attributes['repository'],
                               _build_policy_statements_from_str(attributes, 'policy'),
                               _get_known_value(attributes, 'policy'),
                               attributes['account_id'],
                               attributes['region'])


def build_cloudwatch_logs_destination(attributes: dict) -> CloudWatchLogsDestination:
    return CloudWatchLogsDestination(attributes['account_id'],
                                     attributes['region'],
                                     attributes['name'],
                                     attributes['arn'])


def build_cloudwatch_logs_policy_destination(attributes: dict) -> CloudWatchLogsDestinationPolicy:
    return CloudWatchLogsDestinationPolicy(attributes['destination_name'],
                                           _build_policy_statements_from_str(attributes, 'access_policy'),
                                           _get_known_value(attributes, 'access_policy'),
                                           attributes['region'],
                                           attributes['account_id'])


def build_rest_api_gw_policy(attributes: dict) -> RestApiGwPolicy:
    return RestApiGwPolicy(attributes['rest_api_id'],
                           _build_policy_statements_from_str(attributes, 'policy'),
                           json.dumps(_get_known_value(attributes, 'policy')),
                           attributes['account_id'])


def build_kms_key_policy(attributes: dict) -> KmsKeyPolicy:
    policy = [PolicyStatement(StatementEffect.ALLOW, ['kms:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))]
    if _get_known_value(attributes, 'policy'):
        policy = _build_policy_statements_from_str(attributes, 'policy')
    return KmsKeyPolicy(attributes.get('key_id'),
                        policy,
                        _get_known_value(attributes, 'policy'),
                        attributes['account_id'])


def build_elastic_search_domain_policy(attributes: dict) -> ElasticSearchDomainPolicy:
    policy = []
    raw_document = None
    if _get_known_value(attributes, 'access_policies'):
        policy = _build_policy_statements_from_str(attributes, 'access_policies')
        _add_resource_for_es_domain_policy_statements(policy, attributes['account_id'], attributes['region'], attributes['domain_name'])
        raw_document = _get_known_value(attributes, 'access_policies')
    return ElasticSearchDomainPolicy(attributes['domain_name'],
                                     policy,
                                     raw_document,
                                     attributes['account_id'])


def build_lambda_function(attributes: dict) -> LambdaFunction:
    vpc_config: Optional[NetworkConfiguration] = None
    for vpc_config_dict in attributes['vpc_config']:
        if vpc_config is None:
            vpc_config = NetworkConfiguration(False, vpc_config_dict['security_group_ids'],
                                              vpc_config_dict['subnet_ids'])
        else:
            vpc_config.security_groups_ids.extend(vpc_config_dict['security_group_ids'])
            vpc_config.subnet_list_ids.extend(vpc_config_dict['subnet_ids'])
    xray_tracing_enabled = False
    if _get_known_value(attributes, 'tracing_config'):
        xray_tracing_enabled = bool(attributes['tracing_config'][0]['mode'] == 'Active')
    lambda_func_version = _get_known_value(attributes, 'version', '$LATEST')
    return LambdaFunction(account=attributes['account_id'],
                          region=attributes['region'],
                          function_name=attributes['function_name'],
                          lambda_func_version=lambda_func_version,
                          arn=attributes['arn'],
                          qualified_arn=attributes.get('qualified_arn'),
                          role_arn=attributes['role'],
                          handler=attributes['handler'],
                          runtime=attributes['runtime'],
                          vpc_config=vpc_config,
                          xray_tracing_enabled=xray_tracing_enabled)


def build_lambda_policy(attributes: dict) -> LambdaPolicy:
    condition_block: List[StatementCondition] = [StatementCondition("ArnLike", "AWS:SourceArn", [attributes.get('source_arn')])] \
        if attributes.get('source_arn', None) else []
    if attributes.get('source_account', None):
        condition_block.append(StatementCondition("StringEquals", "AWS:SourceAccount", [attributes.get('source_account')]))
    principal_type: PrincipalType = PrincipalType.NO_PRINCIPAL
    if attributes['principal'].isnumeric() or ':' in attributes['principal']:
        principal_type = PrincipalType.AWS
    elif attributes['principal'].endswith(".com"):
        principal_type = PrincipalType.SERVICE

    qualifier: str = _get_known_value(attributes, 'qualifier')
    principal: Principal = Principal(principal_type, [attributes['principal']])
    account = attributes['account_id']
    for index, value in enumerate(principal.principal_values):
        if value == account:
            principal.principal_values[index] = f'arn:aws:iam::{account}:root'
    lambda_function_name = get_lambda_function_name_for_lambda_policy(attributes['function_name'], qualifier)
    statement: PolicyStatement = PolicyStatement(effect=StatementEffect.ALLOW,
                                                 actions=[attributes['action']],
                                                 resources=[create_lambda_function_arn(account, attributes['region'],
                                                                                       lambda_function_name, qualifier)
                                                            ],
                                                 principal=principal,
                                                 statement_id=attributes['statement_id'],
                                                 condition_block=condition_block)
    return LambdaPolicy(account=account,
                        region=attributes['region'],
                        function_name=lambda_function_name,
                        statements=[statement],
                        qualifier=qualifier)

def get_lambda_function_name_for_lambda_policy(raw_lambda_function_name: str, qualifier: Optional[str]) -> str:
    if ':' in raw_lambda_function_name:
        if qualifier and qualifier in raw_lambda_function_name:
            return raw_lambda_function_name.split(':')[-2]
        else:
            return raw_lambda_function_name.split(':')[-1]
    return raw_lambda_function_name

def build_lambda_alias(attributes: dict) -> LambdaAlias:
    return LambdaAlias(account=attributes['account_id'],
                       region=attributes['region'],
                       arn=attributes['arn'],
                       name=attributes['name'],
                       function_name_or_arn=attributes['function_name'],
                       function_version=attributes['function_version'],
                       description=attributes.get('', None))


def build_glacier_vault(attributes: dict) -> GlacierVault:
    return GlacierVault(attributes['name'],
                        attributes['arn'],
                        attributes['region'],
                        attributes['account_id'])


def build_glacier_vault_policy(attributes: dict) -> GlacierVaultPolicy:
    policy = []
    if attributes.get('access_policy') and isinstance(json.loads(attributes['access_policy']), dict):
        policy = _build_policy_statements_from_str(attributes, 'access_policy')
    return GlacierVaultPolicy(attributes['arn'],
                              policy,
                              _get_known_value(attributes, 'access_policy'),
                              attributes['account_id'])


def build_efs(attributes: dict) -> ElasticFileSystem:
    return ElasticFileSystem(attributes.get('creation_token'),
                             attributes.get('id'),
                             attributes.get('arn'),
                             bool(_get_known_value(attributes, 'encrypted')),
                             attributes['region'],
                             attributes['account_id'])


def build_efs_policy(attributes: dict) -> EfsPolicy:
    return EfsPolicy(attributes['file_system_id'],
                     _build_policy_statements_from_str(attributes, 'policy'),
                     _get_known_value(attributes, 'policy'),
                     attributes['account_id'],
                     attributes['region'])


def build_glue_data_catalog_policy(attributes: dict) -> GlueDataCatalogPolicy:
    return GlueDataCatalogPolicy(_build_policy_statements_from_str(attributes, 'policy'),
                                 _get_known_value(attributes, 'policy'),
                                 attributes['account_id'],
                                 attributes['region'])


def build_secrets_manager_secret(attributes: dict) -> SecretsManagerSecret:
    secrets_manager_secret_resource = SecretsManagerSecret(attributes['name'], attributes['arn'], attributes['region'], attributes['account_id'])
    if _get_known_value(attributes, 'policy'):
        secrets_manager_secret_resource.resource_based_policy = SecretsManagerSecretPolicy(attributes['arn'],
                                                                                           build_policy_statements_from_str(attributes['policy']),
                                                                                           _get_known_value(attributes, 'policy'),
                                                                                           attributes['account_id'])
    if attributes.get('kms_key_id'):
        secrets_manager_secret_resource.kms_key = attributes.get('kms_key_id')
    return secrets_manager_secret_resource


def build_secrets_manager_secret_policy(attributes: dict) -> SecretsManagerSecretPolicy:
    return SecretsManagerSecretPolicy(attributes['secret_arn'],
                                      _build_policy_statements_from_str(attributes, 'policy'),
                                      _get_known_value(attributes, 'policy'),
                                      attributes['account_id'])


def build_rest_api_gw_mapping(attributes: dict) -> RestApiGwMapping:
    return RestApiGwMapping(attributes['api_id'],
                            attributes['domain_name'],
                            attributes['region'],
                            attributes['account_id'])


def build_rest_api_gw_domain(attributes: dict) -> RestApiGwDomain:
    security_policy = 'TLS_1_0'
    if _get_known_value(attributes, 'security_policy'):
        security_policy = attributes['security_policy']
    return RestApiGwDomain(attributes['domain_name'],
                           security_policy,
                           attributes['account_id'],
                           attributes['region'])


def build_kinesis_stream(attributes: dict) -> KinesisStream:
    return KinesisStream(attributes['name'],
                         attributes['arn'],
                         _get_known_value(attributes, 'encryption_type') == 'KMS',
                         attributes['region'],
                         attributes['account_id'])


def build_glue_data_catalog_crawler(attributes: dict) -> GlueCrawler:
    return GlueCrawler(attributes['name'],
                       attributes['database_name'],
                       attributes['account_id'],
                       attributes['region'])


def build_glue_data_catalog_table(attributes: dict) -> GlueDataCatalogTable:
    return GlueDataCatalogTable(attributes['name'],
                                attributes['database_name'],
                                attributes['account_id'],
                                attributes['region'])


def build_xray_encryption(attributes: dict) -> XrayEncryption:
    return XrayEncryption(attributes.get('key_id'),
                          attributes['region'],
                          attributes['account_id'])


def build_kinesis_firehose_stream(attributes: dict) -> KinesisFirehoseStream:
    es_domain_arn = None
    es_vpc_config: NetworkConfiguration = None
    if _get_known_value(attributes, 'elasticsearch_configuration'):
        es_domain_config = attributes['elasticsearch_configuration'][0]
        es_domain_arn = es_domain_config['domain_arn']
        if _get_known_value(es_domain_config, 'vpc_config'):
            es_vpc_configurations = es_domain_config['vpc_config'][0]
            es_vpc_config = NetworkConfiguration(False, es_vpc_configurations['security_group_ids'], es_vpc_configurations['subnet_ids'])
    return KinesisFirehoseStream(attributes['name'],
                                 attributes['arn'],
                                 any(item['enabled'] for item in attributes.get('server_side_encryption')),
                                 attributes['account_id'],
                                 attributes['region'],
                                 es_domain_arn,
                                 es_vpc_config)


def build_workspace(attributes: dict) -> Workspace:
    return Workspace(attributes['region'],
                     attributes['account_id'],
                     attributes['id'],
                     _get_known_value(attributes, 'root_volume_encryption_enabled'),
                     _get_known_value(attributes, 'user_volume_encryption_enabled'),
                     get_dict_value(attributes, 'volume_encryption_key', None))


def build_kms_alias(attributes: dict) -> KmsAlias:
    return KmsAlias(attributes['name'],
                    attributes['target_key_id'],
                    attributes['arn'],
                    attributes['account_id'],
                    attributes['region'])


def build_iam_password_policy(attributes: dict) -> IamPasswordPolicy:
    return IamPasswordPolicy(_get_known_value(attributes, 'minimum_password_length'),
                             _get_known_value(attributes, 'require_lowercase_characters'),
                             _get_known_value(attributes, 'require_numbers'),
                             _get_known_value(attributes, 'require_uppercase_characters'),
                             _get_known_value(attributes, 'require_symbols'),
                             _get_known_value(attributes, 'allow_users_to_change_password'),
                             _get_known_value(attributes, 'max_password_age'),
                             _get_known_value(attributes, 'password_reuse_prevention'),
                             attributes['account_id'])


def build_iam_policy_attachment(attributes: dict) -> IamPolicyAttachment:
    return IamPolicyAttachment(attributes['account_id'],
                               attributes['policy_arn'],
                               attributes['name'],
                               _get_known_value(attributes, 'users', []),
                               _get_known_value(attributes, 'roles', []),
                               _get_known_value(attributes, 'groups', []))


def build_ssm_parameter(attributes: dict) -> SsmParameter:
    return SsmParameter(attributes['name'],
                        attributes['type'],
                        _get_known_value(attributes, 'key_id', 'alias/aws/ssm'),
                        attributes['account_id'],
                        attributes['region'])


def build_dms_replication_instance(attributes: dict) -> DmsReplicationInstance:
    return DmsReplicationInstance(attributes['account_id'],
                                  attributes['region'],
                                  attributes['replication_instance_id'],
                                  attributes['replication_instance_arn'],
                                  attributes['publicly_accessible'],
                                  _get_known_value(attributes, 'replication_subnet_group_id'),
                                  _get_known_value(attributes, 'vpc_security_group_ids', []))


def build_dms_replication_instance_subnet_group(attributes: dict) -> DmsReplicationInstanceSubnetGroup:
    replication_subnet_group_id = attributes['replication_subnet_group_id']
    return DmsReplicationInstanceSubnetGroup(attributes['account_id'],
                                             attributes['region'],
                                             replication_subnet_group_id,
                                             attributes['subnet_ids'],
                                             attributes['vpc_id']).with_aliases(attributes['id'],
                                                                                replication_subnet_group_id + attributes['account_id'] + attributes[
                                                                                    'region'])


def build_sagemaker_endpoint_config(attributes: dict) -> SageMakerEndpointConfig:
    return SageMakerEndpointConfig(attributes['name'],
                                   attributes['arn'],
                                   bool(attributes.get('kms_key_arn')),
                                   attributes['region'],
                                   attributes['account_id'])


def build_sagemaker_notebook_instance(attributes: dict) -> SageMakerNotebookInstance:
    return SageMakerNotebookInstance(attributes['name'],
                                     attributes['arn'],
                                     _get_known_value(attributes, 'kms_key_id'),
                                     attributes['region'],
                                     attributes['account_id'],
                                     bool(attributes['direct_internet_access'] == 'Enabled'))


def build_elasticache_cluster(attributes: dict) -> ElastiCacheCluster:
    engine = 'redis'
    if _get_known_value(attributes, 'replication_group_id') is None:
        engine = attributes['engine']
    return ElastiCacheCluster(attributes['region'],
                              attributes['account_id'],
                              attributes['cluster_id'],
                              attributes['arn'],
                              _get_known_value(attributes, 'replication_group_id'),
                              _get_known_value(attributes, 'security_group_ids'),
                              _get_known_value(attributes, 'snapshot_retention_limit', 0),
                              engine,
                              _get_known_value(attributes, 'subnet_group_name', 'default'))


def build_elasticache_subnet_group(attributes: dict) -> ElastiCacheSubnetGroup:
    return ElastiCacheSubnetGroup(attributes['account_id'],
                                  attributes['region'],
                                  attributes['name'],
                                  attributes['subnet_ids'])


def build_efs_mount_target(attributes: dict) -> EfsMountTarget:
    return EfsMountTarget(attributes['account_id'],
                          attributes['region'],
                          attributes['file_system_id'],
                          attributes['id'],
                          attributes['network_interface_id'],
                          attributes['subnet_id'],
                          _get_known_value(attributes, 'security_groups'))


def build_workspaces_directory(attributes: dict) -> WorkspaceDirectory:
    security_group_ids_value = _get_known_value(attributes, 'workspace_security_group_id')
    if security_group_ids_value:
        security_group_ids = [_get_known_value(attributes, 'workspace_security_group_id')]
    else:
        security_group_ids = []
    if _get_known_value(attributes, 'workspace_creation_properties') \
            and _get_known_value(attributes['workspace_creation_properties'][0], 'custom_security_group_id'):
        security_group_ids.append(_get_known_value(attributes['workspace_creation_properties'][0], 'custom_security_group_id'))
    return WorkspaceDirectory(attributes['account_id'],
                              attributes['region'],
                              attributes['directory_id'],
                              _get_known_value(attributes, 'subnet_ids'),
                              security_group_ids)


def build_directory_service(attributes: dict) -> DirectoryService:
    security_group_ids_value = _get_known_value(attributes, 'security_group_id')
    if security_group_ids_value:
        security_group_ids = [_get_known_value(attributes, 'security_group_id')]
    else:
        security_group_ids = []
    vpc_settings = _get_known_value(attributes, 'vpc_settings')
    if vpc_settings:
        vpc_config = NetworkConfiguration(False, security_group_ids, attributes['vpc_settings'][0]['subnet_ids'])
        vpc_id = attributes['vpc_settings'][0]['vpc_id']
    else:
        vpc_config = NetworkConfiguration(False, security_group_ids, attributes['connect_settings'][0]['subnet_ids'])
        vpc_id = attributes['connect_settings'][0]['vpc_id']
    return DirectoryService(attributes['account_id'],
                            attributes['region'],
                            attributes['name'],
                            attributes['id'],
                            vpc_id,
                            _get_known_value(attributes, 'type', 'SimpleAD'),
                            vpc_config)


def build_load_balancer_attributes(attributes: dict) -> LoadBalancerAttributes:
    lb_access_logs = LoadBalancerAccessLogs('', '', False)
    lb_access_logs_raw_data = _get_known_value(attributes, 'access_logs')
    if lb_access_logs_raw_data:
        lb_access_logs = LoadBalancerAccessLogs(lb_access_logs_raw_data[0]['bucket'] if lb_access_logs_raw_data[0]['bucket'] else '',
                                                lb_access_logs_raw_data[0]['prefix'] if lb_access_logs_raw_data[0]['prefix'] is not None else '',
                                                lb_access_logs_raw_data[0]['enabled'] if lb_access_logs_raw_data[0]['prefix'] is not None else False)
    return LoadBalancerAttributes(attributes['account_id'],
                                  attributes['region'],
                                  attributes['arn'],
                                  get_dict_value(attributes, 'drop_invalid_header_fields', False),
                                  lb_access_logs)


def build_batch_compute_environment(attributes: dict) -> BatchComputeEnvironment:
    vpc_config: NetworkConfiguration = None
    batch_settings = _get_known_value(attributes, 'compute_resources')
    if batch_settings:
        vpc_config = NetworkConfiguration(False, batch_settings[0]['security_group_ids'], batch_settings[0]['subnets'])
    return BatchComputeEnvironment(attributes['compute_environment_name'],
                                   attributes['arn'],
                                   attributes['account_id'],
                                   attributes['region'],
                                   vpc_config)


def build_mq_broker(attributes: dict) -> MqBroker:
    return MqBroker(attributes['broker_name'],
                    attributes['arn'],
                    attributes['id'],
                    attributes['account_id'],
                    attributes['region'],
                    attributes['deployment_mode'],
                    NetworkConfiguration(attributes['publicly_accessible'],
                                         _get_known_value(attributes, 'security_groups', []),
                                         _get_known_value(attributes, 'subnet_ids', [])))


def build_api_gateway(attributes: dict) -> ApiGateway:
    return ApiGateway(attributes['account_id'],
                      attributes['region'],
                      attributes['id'],
                      attributes['name'],
                      attributes['protocol_type'],
                      _get_known_value(attributes, 'arn'))


def build_api_gateway_v2_integration(attributes: dict) -> ApiGatewayV2Integration:
    return ApiGatewayV2Integration(attributes['account_id'],
                                   attributes['region'],
                                   attributes['api_id'],
                                   attributes['connection_id'],
                                   attributes['id'],
                                   RestApiMethod(attributes.get('integration_method')),
                                   IntegrationType(attributes['integration_type']),
                                   attributes.get('integration_uri'))


def build_api_gateway_v2_vpc_link(attributes: dict) -> ApiGatewayVpcLink:
    return ApiGatewayVpcLink(attributes['account_id'],
                             attributes['region'],
                             attributes['id'],
                             attributes['name'],
                             attributes['arn'],
                             attributes['security_group_ids'],
                             attributes['subnet_ids'])


def build_emr_cluster(attributes: dict) -> EmrCluster:
    master_sg_id = ''
    slave_sg_id = ''
    vpc_config: Optional[NetworkConfiguration] = None
    ec2_settings = attributes.get('ec2_attributes')
    if ec2_settings:
        subnet_ids_list = [ec2_settings[0].get('subnet_id')]
        if ec2_settings[0].get('subnet_ids'):
            subnet_ids_list.extend(ec2_settings[0]['subnet_ids'])
        master_sg_id = get_dict_value(ec2_settings[0], 'emr_managed_master_security_group', None)
        slave_sg_id = get_dict_value(ec2_settings[0], 'emr_managed_slave_security_group', None)
        security_group_ids_list = [master_sg_id,
                                   slave_sg_id,
                                   ec2_settings[0].get('service_access_security_group')]
        additional_master_security_groups = ec2_settings[0].get('additional_master_security_groups')
        if additional_master_security_groups:
            if ',' in additional_master_security_groups:
                additional_master_security_groups = additional_master_security_groups.split(',')
            else:
                additional_master_security_groups = [additional_master_security_groups]
            security_group_ids_list.extend(additional_master_security_groups)
        additional_slave_security_groups = ec2_settings[0].get('additional_slave_security_groups')
        if additional_slave_security_groups:
            if ',' in additional_slave_security_groups:
                additional_slave_security_groups = additional_slave_security_groups.split(',')
            else:
                additional_slave_security_groups = [additional_slave_security_groups]
            security_group_ids_list.extend(additional_slave_security_groups)
        subnet_ids = [subnet_id for subnet_id in subnet_ids_list if subnet_id]
        security_group_ids = [sg for sg in security_group_ids_list if sg]
        vpc_config = NetworkConfiguration(None, security_group_ids, subnet_ids)
    return EmrCluster(attributes['account_id'],
                      attributes['region'],
                      attributes['name'],
                      attributes['id'],
                      attributes['arn'],
                      vpc_config,
                      master_sg_id,
                      slave_sg_id)


def build_global_accelerator(attributes: dict) -> GlobalAccelerator:
    return GlobalAccelerator(attributes['account_id'],
                             attributes['name'],
                             attributes['id'])


def build_global_accelerator_listener(attributes: dict) -> GlobalAcceleratorListener:
    return GlobalAcceleratorListener(attributes['account_id'],
                                     attributes['id'],
                                     attributes['accelerator_arn'])


def build_global_accelerator_endpoint_group(attributes: dict) -> GlobalAcceleratorEndpointGroup:
    endpoint_config = attributes.get('endpoint_configuration', [{}])
    return GlobalAcceleratorEndpointGroup(attributes['account_id'],
                                          attributes['listener_arn'],
                                          attributes['arn'],
                                          endpoint_config[0].get('endpoint_id'),
                                          endpoint_config[0].get('client_ip_preservation_enabled'),
                                          _get_known_value(attributes, 'endpoint_group_region'))


def build_cloudhsm_v2_cluster_builder(attributes: dict) -> CloudHsmV2Cluster:
    return CloudHsmV2Cluster(attributes['hsm_type'],
                             attributes['subnet_ids'],
                             attributes['cluster_id'],
                             _get_known_value(attributes, 'vpc_id'),
                             _get_known_value(attributes, 'security_group_id'),
                             attributes['account_id'],
                             attributes['region'])


def build_cloudhsm_v2_hsm(attributes: dict) -> CloudHsmV2Hsm:
    return CloudHsmV2Hsm(attributes['cluster_id'],
                         attributes['hsm_id'],
                         attributes['subnet_id'],
                         attributes['availability_zone'],
                         attributes['hsm_state'],
                         attributes['region'],
                         attributes['account_id'])


def build_s3outpost_endpoint(attributes: dict) -> S3OutpostEndpoint:
    return S3OutpostEndpoint(attributes['outpost_id'],
                             attributes['arn'],
                             attributes['account_id'],
                             attributes['region'],
                             NetworkConfiguration(False, [attributes['security_group_id']], [attributes['subnet_id']]))


def build_worklink_fleet(attributes: dict) -> WorkLinkFleet:
    vpc_config: Optional[NetworkConfiguration] = None
    vpc_settings = _get_known_value(attributes, 'network')
    if vpc_settings:
        vpc_config = NetworkConfiguration(False, vpc_settings[0]['security_group_ids'], vpc_settings[0]['subnet_ids'])
    return WorkLinkFleet(attributes['name'],
                         attributes['arn'],
                         attributes['account_id'],
                         attributes['region'],
                         vpc_config)


def build_glue_connection(attributes: dict) -> GlueConnection:
    vpc_config: Optional[NetworkConfiguration] = None
    vpc_settings = _get_known_value(attributes, 'physical_connection_requirements')
    if vpc_settings:
        vpc_config = NetworkConfiguration(False, _get_known_value(vpc_settings[0], 'security_group_id_list'), [vpc_settings[0]['subnet_id']])
    return GlueConnection(attributes['name'],
                          attributes['arn'],
                          attributes['account_id'],
                          attributes['region'],
                          vpc_config)


def build_config_aggregator(attributes: dict) -> ConfigAggregator:
    account_aggregation_used = False
    account_aggregation_all_regions_enabled = None
    organization_aggregation_used = False
    organization_aggregation_all_regions_enabled = None
    if _get_known_value(attributes, 'account_aggregation_source'):
        account_aggregation_used = True
        account_aggregation_all_regions_enabled = attributes['account_aggregation_source'][0]['all_regions']
    if _get_known_value(attributes, 'organization_aggregation_source'):
        organization_aggregation_used = True
        organization_aggregation_all_regions_enabled = attributes['organization_aggregation_source'][0]['all_regions']
    return ConfigAggregator(attributes['account_id'],
                            attributes['region'],
                            attributes['name'],
                            attributes['arn'],
                            account_aggregation_used,
                            organization_aggregation_used,
                            account_aggregation_all_regions_enabled,
                            organization_aggregation_all_regions_enabled)


def build_global_accelerator_attribute(attributes: dict) -> GlobalAcceleratorAttribute:
    flow_logs_enabled = False
    flow_logs_s3_bucket = None
    flow_logs_s3_prefix = None
    gac_attributes = _get_known_value(attributes, 'attributes')
    if gac_attributes:
        flow_logs_enabled = gac_attributes[0]['flow_logs_enabled']
        flow_logs_s3_bucket = gac_attributes[0].get('flow_logs_s3_bucket')
        flow_logs_s3_prefix = gac_attributes[0].get('flow_logs_s3_prefix')
    return GlobalAcceleratorAttribute(attributes['account_id'],
                                      flow_logs_enabled,
                                      flow_logs_s3_bucket,
                                      flow_logs_s3_prefix,
                                      attributes['id'])


def build_s3_bucket_logging(attributes: dict) -> Optional[S3BucketLogging]:
    if _get_known_value(attributes, 'logging'):
        target_bucket = attributes['logging'][0]['target_bucket']
        target_prefix = _get_known_value(attributes['logging'][0], 'target_prefix')
        return S3BucketLogging(attributes['bucket'],
                               target_bucket,
                               target_prefix,
                               attributes['account_id'],
                               attributes['region'])
    else:
        return None


def build_athena_database(attributes: dict) -> AthenaDatabase:
    encryption_option = None
    kms_key_encryption = None
    encryption_configuration = _get_known_value(attributes, 'encryption_configuration')
    if encryption_configuration:
        encryption_option = encryption_configuration[0]['encryption_option']
        kms_key_encryption = encryption_configuration[0].get('kms_key')
    return AthenaDatabase(attributes['name'],
                          attributes['bucket'],
                          encryption_option,
                          kms_key_encryption,
                          attributes['region'],
                          attributes['account_id'])

def build_fsx_windows_file_system(attributes: dict) -> FsxWindowsFileSystem:
    return FsxWindowsFileSystem(attributes['region'],
                                attributes['account_id'],
                                attributes['id'],
                                _get_known_value(attributes, 'kms_key_id'),
                                attributes['arn'])
