import ast
import json
import re
import os
import urllib
from typing import List, Optional, Tuple

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
from cloudrail.knowledge.context.aws.resources.athena.athena_workgroup import AthenaWorkgroup
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_configuration import AutoScalingGroup, LaunchConfiguration
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.resources.batch.batch_compute_environment import BatchComputeEnvironment
from cloudrail.knowledge.context.aws.resources.cloudformation.cloudformation_resource_info import CloudformationResourceInfo
from cloudrail.knowledge.context.aws.resources.cloudformation.cloudformation_resource_status import CloudformationResourceStatus
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_list import CacheBehavior, CloudFrontDistribution, OriginConfig, \
    ViewerCertificate
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_logging import CloudfrontDistributionLogging
from cloudrail.knowledge.context.aws.resources.cloudfront.origin_access_identity import OriginAccessIdentity
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
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance_type import EbsInfo, Ec2InstanceType
from cloudrail.knowledge.context.aws.resources.ec2.elastic_ip import ElasticIp
from cloudrail.knowledge.context.aws.resources.ec2.igw_type import IgwType
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
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_vpc_attachment import TransitGatewayVpcAttachment
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc, VpcAttribute
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpoint, VpcEndpointGateway, VpcEndpointInterface
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
from cloudrail.knowledge.context.aws.resources.efs.efs_mount_target import EfsMountTarget, MountTargetSecurityGroups
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
from cloudrail.knowledge.context.aws.resources.emr.emr_public_access_config import EmrPublicAccessConfiguration
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain, LogPublishingOptions
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain_policy import ElasticSearchDomainPolicy
from cloudrail.knowledge.context.aws.resources.fsx.fsx_windows_file_system import FsxWindowsFileSystem
from cloudrail.knowledge.context.aws.resources.glacier.glacier_vault import GlacierVault
from cloudrail.knowledge.context.aws.resources.glacier.glacier_vault_policy import GlacierVaultPolicy
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator import GlobalAccelerator
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator_attributes import GlobalAcceleratorAttribute
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator_endpoint_group import GlobalAcceleratorEndpointGroup
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator_listener import GlobalAcceleratorListener
from cloudrail.knowledge.context.aws.resources.glue.glue_data_catalog_crawler import GlueCrawler
from cloudrail.knowledge.context.aws.resources.glue.glue_data_catalog_policy import GlueDataCatalogPolicy
from cloudrail.knowledge.context.aws.resources.glue.glue_data_catalog_table import GlueDataCatalogTable
from cloudrail.knowledge.context.aws.resources.iam.iam_group import IamGroup
from cloudrail.knowledge.context.aws.resources.iam.iam_instance_profile import IamInstanceProfile
from cloudrail.knowledge.context.aws.resources.iam.iam_password_policy import IamPasswordPolicy
from cloudrail.knowledge.context.aws.resources.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.resources.iam.iam_user_group_membership import IamUserGroupMembership
from cloudrail.knowledge.context.aws.resources.iam.iam_users_login_profile import IamUsersLoginProfile
from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy, InlinePolicy, ManagedPolicy, Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_group_attachment import PolicyGroupAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_role_attachment import PolicyRoleAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.iam.policy_user_attachment import PolicyUserAttachment
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.iam.role_last_used import RoleLastUsed
from cloudrail.knowledge.context.aws.resources.kinesis.kinesis_firehose_stream import KinesisFirehoseStream
from cloudrail.knowledge.context.aws.resources.kinesis.kinesis_stream import KinesisStream
from cloudrail.knowledge.context.aws.resources.kms.kms_alias import KmsAlias
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KeyManager, KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_policy import KmsKeyPolicy
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import LambdaAlias
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_policy import LambdaPolicy
from cloudrail.knowledge.context.aws.resources.mq.mq_broker import MqBroker
from cloudrail.knowledge.context.aws.resources.neptune.neptune_cluster import NeptuneCluster
from cloudrail.knowledge.context.aws.resources.neptune.neptune_instance import NeptuneInstance
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.prefix_lists import PrefixList, PrefixLists
from cloudrail.knowledge.context.aws.resources.rds.db_subnet_group import DbSubnetGroup
from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_global_cluster import RdsGlobalCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.aws.resources.redshift.redshift_logging import RedshiftLogging
from cloudrail.knowledge.context.aws.resources.redshift.redshift_subnet_group import RedshiftSubnetGroup
from cloudrail.knowledge.context.aws.resources.resourcegroupstaggingapi.resource_tag_mapping_list import ResourceTagMappingList
from cloudrail.knowledge.context.aws.resources.s3.public_access_block_settings import PublicAccessBlockLevel, PublicAccessBlockSettings
from cloudrail.knowledge.context.aws.resources.s3.s3_acl import GranteeTypes, S3ACL, S3Permission
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_access_point import S3BucketAccessPoint, S3BucketAccessPointNetworkOrigin
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_encryption import S3BucketEncryption
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_logging import S3BucketLogging
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_versioning import S3BucketVersioning
from cloudrail.knowledge.context.aws.resources.s3.s3_access_point_policy import S3AccessPointPolicy
from cloudrail.knowledge.context.aws.resources.s3.s3_policy import S3Policy
from cloudrail.knowledge.context.aws.resources.sagemaker.sagemaker_endpoint_config import SageMakerEndpointConfig
from cloudrail.knowledge.context.aws.resources.sagemaker.sagemaker_notebook_instance import SageMakerNotebookInstance
from cloudrail.knowledge.context.aws.resources.secretsmanager.secrets_manager_secret import SecretsManagerSecret
from cloudrail.knowledge.context.aws.resources.secretsmanager.secrets_manager_secret_policy import SecretsManagerSecretPolicy
from cloudrail.knowledge.context.aws.resources.sns.sns_topic import SnsTopic
from cloudrail.knowledge.context.aws.resources.sqs.sqs_queue import SqsQueue
from cloudrail.knowledge.context.aws.resources.sqs.sqs_queue_policy import SqsQueuePolicy
from cloudrail.knowledge.context.aws.resources.ssm.ssm_parameter import SsmParameter
from cloudrail.knowledge.context.aws.resources.workspaces.workspace_directory import WorkspaceDirectory
from cloudrail.knowledge.context.aws.resources.workspaces.workspace import Workspace
from cloudrail.knowledge.context.aws.resources.xray.xray_encryption import XrayEncryption
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.port_utils import get_port_by_engine
from cloudrail.knowledge.utils.utils import flat_list
from cloudrail.knowledge.context.environment_context.common_component_builder import build_policy_statement, build_policy_statements_from_str, get_dict_value, extract_attribute_from_file_path
from cloudrail.knowledge.utils.arn_utils import is_valid_arn
from cloudrail.knowledge.utils.tags_utils import extract_name_from_tags
from setuptools.namespaces import flatten


def build_vpc_attribute(raw_data: dict) -> VpcAttribute:
    account: str = raw_data['Account']
    region: str = raw_data['Region']
    raw_data = raw_data['Value']
    vpc_id: str = raw_data['VpcId']
    enable: bool
    attribute_name: str
    if 'EnableDnsSupport' in raw_data:
        enable = raw_data['EnableDnsSupport']['Value']
        attribute_name = 'EnableDnsSupport'
    else:
        enable = raw_data['EnableDnsHostnames']['Value']
        attribute_name = 'EnableDnsHostnames'
    return VpcAttribute(account, region, vpc_id, attribute_name, enable)


def build_vpc(raw_data: dict) -> Vpc:
    vpc_id = raw_data['VpcId']
    cidr_block: List[str] = [x['CidrBlock'] for x in raw_data['CidrBlockAssociationSet'] if
                             x['CidrBlockState']['State'] == 'associated']
    ipv6_cidr_block = []
    if raw_data.get('Ipv6CidrBlockAssociationSet'):
        ipv6_cidr_block = [x['Ipv6CidrBlock'] for x in raw_data['Ipv6CidrBlockAssociationSet'] if
                           x['Ipv6CidrBlockState']['State'] == 'associated']
    name = extract_name_from_tags(raw_data)
    region = raw_data['Region']
    account = raw_data['Account']
    friendly_name = name
    is_default: bool = raw_data["IsDefault"]
    return Vpc(vpc_id=vpc_id, cidr_block=cidr_block, name=name, region=region, ipv6_cidr_block=ipv6_cidr_block,
               account=account, friendly_name=friendly_name, is_default=is_default)


def build_subnet(raw_data: dict) -> Subnet:
    subnet_id = raw_data['SubnetId']
    vpc_id = raw_data['VpcId']
    cidr_block = raw_data['CidrBlock']
    name = extract_name_from_tags(raw_data)
    availability_zone = raw_data['AvailabilityZone']
    region = raw_data['AvailabilityZone'][:-1]
    map_public_ip_on_launch = bool(raw_data['MapPublicIpOnLaunch'])
    is_az_default = raw_data["DefaultForAz"]
    return Subnet(subnet_id=subnet_id, vpc_id=vpc_id, cidr_block=cidr_block, name=name, availability_zone=availability_zone,
                  map_public_ip_on_launch=map_public_ip_on_launch, region=region, is_default=is_az_default, account=raw_data['Account'])


def build_vpc_endpoint(raw_data: dict) -> VpcEndpoint:
    account = raw_data['Account']
    region = raw_data['Region']
    vpc_id = raw_data['VpcId']
    service_name = raw_data['ServiceName']
    state = raw_data['State']
    vpce_id = raw_data['VpcEndpointId']
    raw_policy = json.loads(raw_data['PolicyDocument'])
    policy = build_policy(raw_policy, account)

    if raw_data['VpcEndpointType'] == 'Gateway':
        vpc_endpoint_gateway: VpcEndpointGateway = VpcEndpointGateway(region=region,
                                                                      vpc_id=vpc_id,
                                                                      account=account,
                                                                      service_name=service_name,
                                                                      state=state,
                                                                      policy=policy,
                                                                      vpce_id=vpce_id)
        vpc_endpoint_gateway.route_table_ids = raw_data['RouteTableIds']
        return vpc_endpoint_gateway
    else:
        vpc_endpoint_interface: VpcEndpointInterface = VpcEndpointInterface(region=region,
                                                                            vpc_id=vpc_id,
                                                                            account=account,
                                                                            service_name=service_name,
                                                                            state=state,
                                                                            policy=policy,
                                                                            vpce_id=vpce_id)
        vpc_endpoint_interface.subnet_ids = raw_data['SubnetIds']
        vpc_endpoint_interface.security_group_ids = [group['GroupId'] for group in raw_data['Groups']]
        vpc_endpoint_interface.network_interface_ids = raw_data['NetworkInterfaceIds']
        return vpc_endpoint_interface


def build_policy(raw_data: dict, account: str) -> Policy:
    statements = [build_policy_statement(raw_policy_statement) for raw_policy_statement in raw_data['Statement']]
    return Policy(account, statements)


def build_managed_policy(raw_data: dict) -> ManagedPolicy:
    account = raw_data['Account']
    policy_id = raw_data['PolicyId']
    policy_name = raw_data['PolicyName']
    arn = raw_data['Arn']
    raw_statements = list(
        flatten([s['Document']['Statement'] for s in raw_data['PolicyVersionList']
                 if isinstance(s['Document']['Statement'], list)]))
    statements = [build_policy_statement(raw_statement) for raw_statement in raw_statements]
    raw_document = raw_data['PolicyVersionList'] and raw_data['PolicyVersionList'][0]['Document']
    return ManagedPolicy(account, policy_id, policy_name, arn, statements, raw_document)


def build_iam_user(raw_data: dict) -> IamUser:
    name = raw_data['UserName']
    user_id = raw_data['UserId']
    arn = raw_data['Arn']
    permission_boundary_arn = get_dict_value(raw_data, 'PermissionsBoundary', {}).get('PermissionsBoundaryArn', None)
    return IamUser(raw_data['Account'], name, user_id, arn, permission_boundary_arn, arn)


def build_user_login_profile(raw_data: dict) -> IamUsersLoginProfile:
    return IamUsersLoginProfile(raw_data['Value']['UserName'],
                                raw_data['Account'])


def build_iam_user_inline_policies(raw_data: dict) -> List[InlinePolicy]:
    username = raw_data['UserName']
    account = raw_data['Account']
    if not raw_data.get('UserPolicyList'):
        return []
    policies = [build_inline_policy(inline_policy, username, account) for inline_policy in raw_data['UserPolicyList']]
    return policies


def build_policy_user_attachments(raw_data: dict) -> List[PolicyUserAttachment]:
    account = raw_data['Account']
    user_id = raw_data['UserId']
    user_name = raw_data['UserName']
    return [PolicyUserAttachment(account, x['PolicyArn'], user_id, user_name) for x in raw_data['AttachedManagedPolicies']]


def build_iam_group(raw_data: dict) -> IamGroup:
    account = raw_data['Account']
    name = raw_data['GroupName']
    group_id = raw_data['GroupId']
    arn = raw_data['Arn']
    return IamGroup(account, name, group_id, arn, arn)


def build_policy_group_attachments(raw_data: dict) -> List[PolicyGroupAttachment]:
    group_id = raw_data['GroupId']
    account = raw_data['Account']
    group_name = raw_data['GroupName']
    return [PolicyGroupAttachment(account, x['PolicyArn'], group_id, group_name) for x in raw_data['AttachedManagedPolicies']]


def build_user_group_membership(raw_data: dict) -> IamUserGroupMembership:
    return IamUserGroupMembership(raw_data['Account'], raw_data['UserName'], raw_data['GroupList'])


def build_iam_group_inline_policies(raw_data: dict) -> List[InlinePolicy]:
    group_id = raw_data['GroupId']
    account = raw_data['Account']
    policies = [build_inline_policy(inline_policy, group_id, account) for inline_policy in raw_data['GroupPolicyList']]
    return policies


def build_s3_policy(raw_data: dict, attributes: dict) -> S3Policy:
    account = attributes['Account']
    bucket_name = raw_data['BucketName']
    statements = [build_policy_statement(raw_statement) for raw_statement in raw_data['Statement']]
    return S3Policy(account, bucket_name, statements, json.dumps({'Id': raw_data.get('Id'),
                                                                  'Statement': raw_data.get('Statement'),
                                                                  'Version': raw_data.get('Version')}))


def build_inline_policy(raw_data: dict, owner_id: str, account: str) -> InlinePolicy:
    policy_name = raw_data['PolicyName']
    statements = _build_policy_statements(raw_data['PolicyDocument']['Statement'])
    return InlinePolicy(account, owner_id, policy_name, statements, raw_data['PolicyDocument'])


def _build_policy_statements(statements_list: dict) -> List[PolicyStatement]:
    return [build_policy_statement(raw_statement) for raw_statement in statements_list]


def build_s3_access_point_policy(raw_data: dict) -> S3AccessPointPolicy:
    account = raw_data['Account']
    region = raw_data['Region']
    access_point_name = os.path.basename(raw_data['FilePath'])
    policy_data = json.loads(raw_data['Value'])
    statements = [build_policy_statement(raw_statement) for raw_statement in policy_data['Statement']]
    return S3AccessPointPolicy(account, region, access_point_name, statements, raw_data['Value'])


def build_s3_public_access_block_settings(raw_data: dict) -> PublicAccessBlockSettings:
    settings_dict: dict = raw_data['Value']
    level: PublicAccessBlockLevel = get_dict_value(raw_data, "access_level", PublicAccessBlockLevel.BUCKET)
    bucket_name_or_account_id: str = raw_data['Account']
    if level == PublicAccessBlockLevel.BUCKET:
        bucket_name_or_account_id = extract_attribute_from_file_path(raw_data['FilePath'], ['Bucket-'])
    return PublicAccessBlockSettings(bucket_name_or_account_id=bucket_name_or_account_id,
                                     block_public_acls=settings_dict["BlockPublicAcls"],
                                     block_public_policy=settings_dict["BlockPublicPolicy"],
                                     ignore_public_acls=settings_dict["IgnorePublicAcls"],
                                     restrict_public_buckets=settings_dict["RestrictPublicBuckets"],
                                     access_level=level,
                                     account=raw_data['Account'],
                                     region=raw_data['Region'])


def build_peering_connection(raw_data: dict) -> PeeringConnection:
    peering_id = raw_data['VpcPeeringConnectionId']
    accepter_vpc_raw = raw_data['AccepterVpcInfo']
    requester_vpc_raw = raw_data['RequesterVpcInfo']

    accepter_vpc_cidrs = [cidr['CidrBlock'] for cidr in get_dict_value(accepter_vpc_raw, 'CidrBlockSet', {})]
    if accepter_vpc_raw.get('Ipv6CidrBlockSet'):
        accepter_vpc_cidrs.extend([cidr['Ipv6CidrBlock'] for cidr in accepter_vpc_raw.get('Ipv6CidrBlockSet')])

    requester_vpc_cidrs = [cidr['CidrBlock'] for cidr in get_dict_value(requester_vpc_raw, 'CidrBlockSet', {})]
    if requester_vpc_raw.get('Ipv6CidrBlockSet'):
        accepter_vpc_cidrs.extend([cidr['Ipv6CidrBlock'] for cidr in requester_vpc_raw.get('Ipv6CidrBlockSet')])

    status = raw_data['Status']['Code']
    return PeeringConnection(peering_id,
                             PeeringVpcInfo(accepter_vpc_raw['VpcId'], accepter_vpc_cidrs),
                             PeeringVpcInfo(requester_vpc_raw['VpcId'], requester_vpc_cidrs),
                             status,
                             raw_data['Region'],
                             raw_data['Account'])


def build_load_balancer_target(raw_data: dict) -> LoadBalancerTarget:
    target_group_arn = raw_data['TargetGroupArn']
    target_id = raw_data['Target'].get('Id')
    port = raw_data['Target'].get('Port')
    account = raw_data['Account']
    region = raw_data['Region']
    return LoadBalancerTarget(target_group_arn, target_id, port, account, region)


def build_load_balancer_target_group(raw_data: dict) -> LoadBalancerTargetGroup:
    port = raw_data.get('Port')
    protocol = raw_data.get('Protocol')
    vpc_id = raw_data.get('VpcId')
    target_group_arn = raw_data['TargetGroupArn']
    target_group_name = raw_data['TargetGroupName']
    target_type = raw_data['TargetType']
    account = raw_data['Account']
    region = raw_data['Region']
    return LoadBalancerTargetGroup(port, protocol, vpc_id, target_group_arn, target_group_name, target_type, account, region)


def build_load_balancer_target_group_associations(raw_data: dict) -> List[LoadBalancerTargetGroupAssociation]:
    target_group_arns = [raw_data['TargetGroupArn']]
    port = get_dict_value(raw_data, 'Port', -1)
    account = raw_data['Account']
    region = raw_data['Region']
    return [LoadBalancerTargetGroupAssociation(target_group_arns, load_balancer_arn, port, account, region) for load_balancer_arn in
            raw_data['LoadBalancerArns']]


def build_load_balancer(raw_data: dict) -> LoadBalancer:
    account = raw_data['Account']
    region = raw_data['Region']
    name = raw_data['LoadBalancerName']
    scheme_type = LoadBalancerSchemeType(raw_data['Scheme'])
    load_balancer_type = LoadBalancerType(raw_data['Type'])
    load_balancer_arn = raw_data['LoadBalancerArn']
    return LoadBalancer(account, region, name, scheme_type, load_balancer_type, load_balancer_arn) \
        .with_raw_data(subnets_ids=[az['SubnetId'] for az in raw_data['AvailabilityZones']],
                       security_groups_ids=raw_data.get('SecurityGroups')).with_aliases(load_balancer_arn)


def build_ec2_instance(raw_data: dict) -> Optional[Ec2Instance]:
    state = get_dict_value(raw_data, 'State', {}).get('Name')
    if state != 'running':
        return None
    account = raw_data['Account']
    region = raw_data['Region']
    instance_id = raw_data['InstanceId']
    name = extract_name_from_tags(raw_data)
    network_interfaces_ids = list(map(lambda ni: ni.get('NetworkInterfaceId'), raw_data['NetworkInterfaces']))
    state = raw_data['State']['Name']
    image_id = raw_data['ImageId']
    iam_profile = raw_data.get('IamInstanceProfile')
    iam_profile_name = iam_profile['Arn'].split('/').pop() if iam_profile else None
    http_tokens = get_dict_value(get_dict_value(raw_data, 'MetadataOptions', {}), 'HttpTokens', 'optional')
    availability_zone = raw_data['Placement']['AvailabilityZone']
    instance_type = raw_data['InstanceType']
    ebs_optimized = raw_data.get('EbsOptimized')
    monitoring_enabled = False
    if raw_data.get('Monitoring'):
        monitoring_enabled = bool(raw_data['Monitoring']['State'] == 'enabled')

    return Ec2Instance(account,
                       region,
                       instance_id,
                       name,
                       network_interfaces_ids,
                       state,
                       image_id,
                       iam_profile_name,
                       http_tokens,
                       availability_zone,
                       {},
                       instance_type,
                       ebs_optimized,
                       monitoring_enabled).with_raw_data(subnet_id=raw_data.get('SubnetId'),
                                                         security_groups_ids=[sg['GroupId'] for sg in raw_data.get('SecurityGroups', [])],
                                                         private_ip_address=raw_data.get('PrivateIpAddress'))


def _build_network_acl_rule(raw_data: dict, network_acl_id: str, region: str, account: str) -> NetworkAclRule:
    ipv6_block = raw_data.get('Ipv6CidrBlock')
    ipv4_block = raw_data.get('CidrBlock')
    cidr_block = ipv4_block if ipv4_block else ipv6_block
    from_port = 0
    to_port = 65535
    ip_protocol_type = IpProtocol(raw_data["Protocol"])
    if 'PortRange' in raw_data and ip_protocol_type != IpProtocol.ALL:
        from_port = raw_data['PortRange'].get('From')
        to_port = raw_data['PortRange'].get('To')
    rule_action = RuleAction(raw_data['RuleAction'])
    rule_number = raw_data['RuleNumber']
    rule_type = RuleType.OUTBOUND if raw_data['Egress'] else RuleType.INBOUND
    return NetworkAclRule(region, account, network_acl_id, cidr_block, from_port, to_port, rule_action, rule_number, rule_type, ip_protocol_type)


def build_network_acl_rules(raw_data: dict) -> List[NetworkAclRule]:
    network_acl_id = raw_data['NetworkAclId']
    region = raw_data['Region']
    account = raw_data['Account']
    return list(map(lambda rule: _build_network_acl_rule(rule, network_acl_id, region, account), raw_data['Entries']))


def build_network_acl(raw_data: dict) -> NetworkAcl:
    network_acl_id = raw_data['NetworkAclId']
    vpc_id = raw_data['VpcId']
    is_default = raw_data['IsDefault']
    name = extract_name_from_tags(raw_data)
    subnets: List[str] = list(
        filter(None.__ne__, map(lambda association: association.get('SubnetId'), raw_data['Associations'])))
    return NetworkAcl(network_acl_id, vpc_id, is_default, name, subnets, raw_data['Region'], raw_data['Account'])


def build_security_group(raw_data: dict) -> SecurityGroup:
    security_group_id = raw_data['GroupId']
    name = raw_data['GroupName']
    vpc_id = raw_data.get('VpcId')
    is_default = raw_data.get('GroupName') == 'default'
    has_description = True
    if not is_default:
        has_description = raw_data.get('Description') and raw_data.get('Description') != 'Managed by Terraform'
    region = raw_data['Region']
    account = raw_data['Account']
    return SecurityGroup(security_group_id, region, account, name, vpc_id, is_default, has_description)


def _build_security_group_rules(raw_data: dict,
                                security_group_id: str,
                                connection_type: ConnectionType,
                                region: str,
                                account: str) -> List[SecurityGroupRule]:
    from_port = raw_data.get('FromPort')
    to_port = raw_data.get('ToPort')
    ip_protocol = IpProtocol(raw_data['IpProtocol'])
    rules: List[SecurityGroupRule] = []
    for user_id_group_pair in raw_data['UserIdGroupPairs']:
        property_type = SecurityGroupRulePropertyType.SECURITY_GROUP_ID
        property_value = user_id_group_pair['GroupId']
        has_description = bool(user_id_group_pair.get('Description'))
        rules.append(SecurityGroupRule(from_port, to_port, ip_protocol, property_type, property_value,
                                       has_description, connection_type, security_group_id, region, account))
    for ip_range_pair in raw_data['IpRanges']:
        property_type = SecurityGroupRulePropertyType.IP_RANGES
        property_value = ip_range_pair['CidrIp']
        has_description = bool(ip_range_pair.get('Description'))
        rules.append(SecurityGroupRule(from_port, to_port, ip_protocol, property_type, property_value,
                                       has_description, connection_type, security_group_id, region, account))
    for prefix_list_pair in raw_data['PrefixListIds']:
        property_type = SecurityGroupRulePropertyType.PREFIX_LIST_ID
        property_value = prefix_list_pair['PrefixListId']
        has_description = bool(prefix_list_pair.get('Description'))
        rules.append(SecurityGroupRule(from_port, to_port, ip_protocol, property_type, property_value,
                                       has_description, connection_type, security_group_id, region, account))
    return rules


def build_security_group_rules(raw_data: dict) -> List[SecurityGroupRule]:
    security_group_id = raw_data['GroupId']
    region = raw_data['Region']
    account = raw_data['Account']
    inbound_permissions = flat_list(list(map(
        lambda security_group_rule: _build_security_group_rules(security_group_rule, security_group_id,
                                                                ConnectionType.INBOUND, region, account),
        raw_data['IpPermissions'])))
    outbound_permissions = flat_list(list(map(
        lambda security_group_rule: _build_security_group_rules(security_group_rule, security_group_id,
                                                                ConnectionType.OUTBOUND, region, account),
        raw_data['IpPermissionsEgress'])))
    return inbound_permissions + outbound_permissions


def _build_route(raw_data: dict, route_table_id: str, region: str, account: str) -> Route:
    ipv6_block = raw_data.get('DestinationIpv6CidrBlock')
    ipv4_block = raw_data.get('DestinationCidrBlock')
    prefix_list_id = raw_data.get('DestinationPrefixListId')
    destination = ipv4_block or ipv6_block or prefix_list_id
    for destination_type in RouteTargetType:
        if destination_type.value in raw_data:
            target = raw_data[destination_type.value]
            return Route(route_table_id, destination, destination_type, target, region, account)
    raise Exception('Unknown route {}'.format(raw_data))


def build_routes(raw_data: dict) -> List[Route]:
    route_table_id = raw_data['RouteTableId']
    region = raw_data['Region']
    account = raw_data['Account']
    return list(map(lambda route: _build_route(route, route_table_id, region, account), raw_data['Routes']))


def build_route_table_association(raw_data: dict) -> List[RouteTableAssociation]:
    route_table_id = raw_data['RouteTableId']
    return list(filter(None.__ne__,
                       map(lambda association: RouteTableAssociation(association.get('RouteTableAssociationId'), association.get('SubnetId'),
                                                                     route_table_id, raw_data['Region'], raw_data['Account']),
                           raw_data['Associations'])))


def build_main_route_table_association(raw_data: dict) -> List[MainRouteTableAssociation]:
    route_table_id = raw_data['RouteTableId']
    vpc_id = raw_data['VpcId']
    account = raw_data['Account']
    region = raw_data['Region']
    is_main: bool = any(association['Main'] for association in raw_data['Associations'])
    if is_main:
        return [MainRouteTableAssociation(vpc_id, route_table_id, account, region)]
    else:
        return []


def build_route_table(raw_data: dict) -> RouteTable:
    route_table_id = raw_data['RouteTableId']
    vpc_id = raw_data['VpcId']
    name = extract_name_from_tags(raw_data)
    is_main = any(association['Main'] for association in raw_data.get('Associations', []))
    return RouteTable(route_table_id, vpc_id, name, raw_data['Region'], raw_data['Account'], is_main)


def build_policy_role_attachments(raw_data: dict) -> List[PolicyRoleAttachment]:
    account = raw_data['Account']
    role_name = raw_data['RoleName']
    return [PolicyRoleAttachment(account, x['PolicyArn'], role_name) for x in raw_data['AttachedManagedPolicies']]


def build_iam_role(raw_data: dict) -> Role:
    arn = raw_data['Arn']
    role_name = raw_data['RoleName']
    role_id = raw_data['RoleId']
    permission_boundary_arn = get_dict_value(raw_data, 'PermissionsBoundary', {}).get('PermissionsBoundaryArn', None)
    creation_date = raw_data['CreateDate']
    return Role(raw_data['Account'], arn, role_name, role_id, permission_boundary_arn, creation_date, arn)


def build_iam_assume_role_policy(raw_data: dict) -> AssumeRolePolicy:
    return AssumeRolePolicy(raw_data['Account'], raw_data['RoleName'], raw_data['Arn'],
                            [build_policy_statement(raw_statement) for raw_statement in raw_data['AssumeRolePolicyDocument']['Statement']],
                            raw_data['AssumeRolePolicyDocument'])


def build_iam_instance_profile(raw_data: dict) -> List[IamInstanceProfile]:
    account = raw_data['Account']
    region = raw_data['Region']
    role_name = raw_data['RoleName']
    instance_profile_names = [x['InstanceProfileName'] for x in raw_data['InstanceProfileList']]
    return [IamInstanceProfile(account, region, role_name, instance_profile_name) for instance_profile_name in instance_profile_names]


def build_iam_role_inline_policies(raw_data: dict) -> List[InlinePolicy]:
    account = raw_data['Account']
    role_name = raw_data['RoleName']
    policies = [build_inline_policy(inline_policy, role_name, account) for inline_policy in raw_data['RolePolicyList']]
    return policies


def build_iam_role_last_used(attributes: dict) -> RoleLastUsed:
    return RoleLastUsed(attributes['Account'],
                        attributes['Region'],
                        attributes['RoleName'],
                        attributes['Arn'],
                        attributes['RoleLastUsed'].get('LastUsedDate'))


def build_transit_gateway_vpc_attachment(raw_data: dict) -> TransitGatewayVpcAttachment:
    state: str = raw_data['State']
    resource_type: TransitGatewayResourceType = TransitGatewayResourceType.VPC
    resource_id: str = raw_data['VpcId']
    name: str = extract_name_from_tags(raw_data)
    attachment_id = raw_data['TransitGatewayAttachmentId']
    transit_gateway_id = raw_data['TransitGatewayId']
    subnet_ids = raw_data['SubnetIds']
    region = raw_data['Region']
    account = raw_data['Account']
    return TransitGatewayVpcAttachment(transit_gateway_id, attachment_id, state, resource_type, resource_id, name, subnet_ids, region, account)


def build_transit_gateway_route_table_association(raw_data: dict) -> TransitGatewayRouteTableAssociation:
    return TransitGatewayRouteTableAssociation(raw_data['TransitGatewayAttachmentId'],
                                               raw_data['RouteTableId'],
                                               raw_data['Region'],
                                               raw_data['Account'])


def build_transit_gateway(raw_data: dict) -> TransitGateway:
    name = extract_name_from_tags(raw_data)
    tgw_id = raw_data['TransitGatewayId']
    state = raw_data['State']
    region = raw_data['Region']
    account = raw_data['Account']
    return TransitGateway(name, tgw_id, state, region, account)


def build_transit_gateway_route_table(raw_data: dict) -> TransitGatewayRouteTable:
    return TransitGatewayRouteTable(raw_data['TransitGatewayId'],
                                    raw_data['TransitGatewayRouteTableId'],
                                    raw_data['Region'],
                                    raw_data['Account'])


def build_transit_gateway_route(raw_data: dict) -> TransitGatewayRoute:
    ipv6_block = raw_data.get('DestinationIpv6CidrBlock')
    ipv4_block = raw_data.get('DestinationCidrBlock')
    destination_cidr_block = ipv4_block if ipv4_block else ipv6_block
    state = TransitGatewayRouteState(raw_data['State'])
    route_type = TransitGatewayRouteType(raw_data['Type'])
    route_table_id = raw_data['RouteTableId']
    return TransitGatewayRoute(destination_cidr_block,
                               state,
                               route_type,
                               route_table_id,
                               raw_data['Region'],
                               raw_data['Account'])


def build_s3_bucket(raw_data: dict) -> S3Bucket:
    bucket_name = raw_data['Name']
    account = raw_data['Account']
    arn = 'arn:aws:s3:::{}'.format(bucket_name)
    return S3Bucket(account, bucket_name, arn, raw_data['Region'])


def build_s3_acl(raw_data: dict) -> List[S3ACL]:
    acl_dict: dict = raw_data['Value']
    grants_array: dict = acl_dict['Grants']
    acl_list: List[S3ACL] = []
    for grantee in grants_array:
        actions = S3Permission[grantee['Permission']]
        grantee_type = GranteeTypes(grantee['Grantee']['Type'])
        type_value = GranteeTypes.get_type_value(grantee_type, grantee['Grantee'])
        bucket_name = raw_data['BucketName']
        owner_id = acl_dict["Owner"]["ID"]
        owner_name = get_dict_value(acl_dict["Owner"], "DisplayName", "")
        acl_list.append(S3ACL(actions, grantee_type, type_value, bucket_name, raw_data['Account'], raw_data['Region'], owner_id, owner_name))
    return acl_list


def build_s3_bucket_access_point_network_origin(raw_data: dict) -> S3BucketAccessPointNetworkOrigin:
    if raw_data['NetworkOrigin'] == 'VPC':
        access_type = 'vpc'
        vpc_id = raw_data['VpcConfiguration']['VpcId']
    else:
        access_type = 'internet'
        vpc_id = None
    return S3BucketAccessPointNetworkOrigin(access_type, vpc_id)


def build_s3_bucket_access_point(raw_data: dict) -> S3BucketAccessPoint:
    bucket_name = raw_data['Bucket']
    name = raw_data['Name']
    network_origin = build_s3_bucket_access_point_network_origin(raw_data)
    account = raw_data['Account']
    arn = 'arn:aws:{}:{}:accesspoint/{}'.format(raw_data['Region'], account, name)
    return S3BucketAccessPoint(bucket_name, name, network_origin, arn, raw_data['Region'], raw_data['Account'])


def build_eni_instance(raw_data: dict) -> Optional[NetworkInterface]:
    if not raw_data.get('Status') == 'in-use':
        return None
    eni_id = raw_data['NetworkInterfaceId']
    subnet_id = raw_data['SubnetId']
    primary_private_ip = next(x['PrivateIpAddress'] for x in raw_data['PrivateIpAddresses'] if x['Primary'])
    secondary_private_ips = [x['PrivateIpAddress'] for x in raw_data['PrivateIpAddresses'] if not x['Primary']]
    ipv6_ip_addresses = [x['Ipv6Address'] for x in raw_data['Ipv6Addresses']]
    association = raw_data.get('Association')
    if association:
        public_ip = association.get('PublicIp')
    else:
        public_ip = None
    security_groups_ids = [x['GroupId'] for x in raw_data['Groups']]
    description = raw_data['Description']
    is_primary = raw_data.get('Attachment') and raw_data['Attachment'].get('Status') == 'attached' and raw_data[
        'Attachment'].get('DeviceIndex') == 0
    availability_zone = raw_data['AvailabilityZone']
    return NetworkInterface(eni_id, subnet_id, primary_private_ip, secondary_private_ips, public_ip, ipv6_ip_addresses,
                            security_groups_ids, description, is_primary, availability_zone, raw_data['Account'], raw_data['Region'])


def build_auto_scaling_group(raw_data: dict) -> AutoScalingGroup:
    launch_template = get_dict_value(raw_data, 'LaunchTemplate', {})
    subnet_ids = [subnet_id for subnet_id in raw_data['VPCZoneIdentifier'].split(',') if subnet_id]
    return AutoScalingGroup(
        arn=raw_data['AutoScalingGroupARN'],
        target_group_arns=raw_data['TargetGroupARNs'],
        name=raw_data['AutoScalingGroupName'],
        availability_zones=raw_data['AvailabilityZones'],
        subnet_ids=subnet_ids,
        region=raw_data['Region'],
        account=raw_data['Account']) \
        .with_raw_data(launch_configuration_name=raw_data.get('LaunchConfigurationName'),
                       launch_template_id=launch_template.get('LaunchTemplateId'),
                       launch_template_version=launch_template.get('Version'),
                       launch_template_name=launch_template.get('LaunchTemplateName'))


def build_launch_configuration(raw_data: dict) -> LaunchConfiguration:
    monitoring_enabled = False
    if raw_data.get('InstanceMonitoring'):
        monitoring_enabled = raw_data['InstanceMonitoring']['Enabled']
    iam_instance_profile = raw_data.get('IamInstanceProfile')
    if iam_instance_profile:
        iam_instance_profile = raw_data['IamInstanceProfile'].split('/')[1] if 'arn:' in iam_instance_profile else iam_instance_profile
    return LaunchConfiguration(
        arn=raw_data['LaunchConfigurationARN'],
        image_id=raw_data['ImageId'],
        instance_type=raw_data['InstanceType'],
        key_name=raw_data['KeyName'],
        name=raw_data['LaunchConfigurationName'],
        security_group_ids=raw_data['SecurityGroups'],
        http_tokens=get_dict_value(get_dict_value(raw_data, 'MetadataOptions', {}), 'HttpTokens', 'optional'),
        iam_instance_profile=iam_instance_profile,
        region=raw_data['Region'],
        account=raw_data['Account'],
        associate_public_ip_address=raw_data.get('AssociatePublicIpAddress', False),
        ebs_optimized=raw_data.get('EbsOptimized'),
        monitoring_enabled=monitoring_enabled)


def build_redshift_cluster(raw_data: dict) -> RedshiftCluster:
    subnet_group_name = raw_data.get('ClusterSubnetGroupName')
    return RedshiftCluster(raw_data['Account'],
                           raw_data['Region'],
                           raw_data['DBName'],
                           raw_data['ClusterIdentifier'],
                           raw_data['Endpoint']['Port'],
                           subnet_group_name,
                           [security_group_details['VpcSecurityGroupId']
                            for security_group_details in raw_data['VpcSecurityGroups']
                            if security_group_details['Status'] == 'active'],
                           raw_data['PubliclyAccessible'],
                           raw_data['Encrypted'])


def build_redshift_subnet_group(raw_data: dict) -> RedshiftSubnetGroup:
    return RedshiftSubnetGroup(raw_data['ClusterSubnetGroupName'],
                               [x['SubnetIdentifier'] for x in raw_data['Subnets']],
                               raw_data['Region'],
                               raw_data['Account'])


def build_redshift_logging(attributes: dict) -> RedshiftLogging:
    logs_data = attributes['Value']
    return RedshiftLogging(attributes['Account'],
                           attributes['Region'],
                           extract_attribute_from_file_path(attributes['FilePath'], ['ClusterIdentifier-']),
                           logs_data.get('BucketName'),
                           logs_data.get('S3KeyPrefix'),
                           logs_data['LoggingEnabled'])


def build_ecs_cluster(raw_data: dict) -> EcsCluster:
    container_insights_enabled = True
    if raw_data['settings']:
        container_insights_enabled = bool(raw_data['settings'][0]['value'] == 'enabled')
    ecs_cluster: EcsCluster = EcsCluster(raw_data['Account'], raw_data['Region'],
                                         raw_data["clusterArn"], raw_data["clusterName"],
                                         container_insights_enabled, None)
    return ecs_cluster


def build_ecs_service(raw_data: dict) -> EcsService:
    network_conf_list: List[NetworkConfiguration] = []
    for deployment in raw_data["deployments"]:
        conf_dict: dict = deployment["networkConfiguration"]["awsvpcConfiguration"]
        conf: NetworkConfiguration = NetworkConfiguration(conf_dict["assignPublicIp"] == "ENABLED",
                                                          conf_dict["securityGroups"], conf_dict["subnets"])
        network_conf_list.append(conf)
    ecs_service: EcsService = EcsService(raw_data["serviceName"],
                                         LaunchType(raw_data["deployments"][0]["launchType"]),
                                         raw_data["clusterArn"],
                                         raw_data['Account'],
                                         raw_data['Region'],
                                         network_conf_list,
                                         raw_data.get('taskDefinition', None))

    elb_list: dict = raw_data["loadBalancers"]
    for elb_dict in elb_list:
        elb: LoadBalancingConfiguration = LoadBalancingConfiguration("",
                                                                     elb_dict["targetGroupArn"],
                                                                     elb_dict["containerName"],
                                                                     elb_dict["containerPort"])
        ecs_service.add_elb(elb)
    return ecs_service


def build_cloud_watch_event_target(raw_data: dict) -> Optional[CloudWatchEventTarget]:
    target_list: List[EcsTarget] = []
    if "EcsParameters" in raw_data:
        conf_dict: dict = raw_data["EcsParameters"]["NetworkConfiguration"]["awsvpcConfiguration"]
        conf: NetworkConfiguration = NetworkConfiguration(conf_dict["AssignPublicIp"] == "ENABLED",
                                                          conf_dict["SecurityGroups"],
                                                          conf_dict["Subnets"])
        target: EcsTarget = EcsTarget(name=raw_data["Arn"].split(':')[-1] + ".target.name",
                                      target_id=raw_data["Id"],
                                      launch_type=LaunchType(raw_data["EcsParameters"]["LaunchType"]),
                                      account=raw_data['Account'],
                                      region=raw_data['Region'],
                                      cluster_arn=raw_data["Arn"],
                                      role_arn=raw_data["RoleArn"],
                                      network_conf_list=[conf],
                                      task_definition_arn=raw_data["EcsParameters"]["TaskDefinitionArn"])
        target_list.append(target)

    if target_list:
        rule_name = extract_attribute_from_file_path(raw_data['FilePath'], ['Rule-'])
        cluster_arn = raw_data["Arn"]
        event_target: CloudWatchEventTarget = CloudWatchEventTarget(account=raw_data['Account'],
                                                                    region=raw_data['Region'],
                                                                    name=cluster_arn.split(':')[-1],
                                                                    rule_name=rule_name,
                                                                    target_id=raw_data['Id'],
                                                                    role_arn=target_list[0].role_arn,
                                                                    cluster_arn=cluster_arn,
                                                                    ecs_target_list=target_list)
        return event_target
    return None


def build_ecs_task_definition(attributes: dict) -> EcsTaskDefinition:
    account = attributes['Account']
    region = attributes['Region']
    attributes = attributes['Value']
    network_mode: NetworkMode = NetworkMode(get_dict_value(attributes, 'networkMode', 'none'))
    container_definitions: List[ContainerDefinition] = []
    efs_volume_data = []
    for volume in attributes.get('volumes', []):
        if volume.get('efsVolumeConfiguration', {}):
            efs_volume_data.append(EfsVolume(volume['name'],
                                             volume['efsVolumeConfiguration']['fileSystemId'],
                                             bool(volume['efsVolumeConfiguration'].get('transitEncryption') == 'ENABLED')))
    for container in attributes['containerDefinitions']:
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
    return EcsTaskDefinition(task_arn=attributes['taskDefinitionArn'],
                             family=attributes['family'],
                             revision=attributes['revision'],
                             account=account,
                             region=region,
                             task_role_arn=attributes.get('taskRoleArn', None),
                             execution_role_arn=attributes.get('executionRoleArn', None),
                             network_mode=network_mode,
                             container_definitions=container_definitions,
                             efs_volume_data=efs_volume_data)


def build_rds_instance(raw_data: dict) -> RdsInstance:
    rds_instance = RdsInstance(raw_data['Account'],
                               raw_data['Region'],
                               raw_data['DBInstanceIdentifier'],
                               raw_data['DBInstanceArn'],
                               raw_data.get('Endpoint', {}).get('Port') or get_port_by_engine(raw_data.get('Engine').lower()),
                               raw_data['PubliclyAccessible'],
                               raw_data['DBSubnetGroup']['DBSubnetGroupName'],
                               [security_group_details['VpcSecurityGroupId']
                                for security_group_details in raw_data['VpcSecurityGroups']
                                if security_group_details['Status'] == 'active'],
                               raw_data.get('DBClusterIdentifier'),
                               raw_data['StorageEncrypted'],
                               raw_data.get('PerformanceInsightsEnabled', False),
                               raw_data.get('PerformanceInsightsKMSKeyId') if raw_data.get('PerformanceInsightsEnabled', False) else None,
                               raw_data['Engine'],
                               raw_data['EngineVersion'],
                               None if raw_data.get('DBClusterIdentifier') else raw_data['DBInstanceIdentifier'])
    rds_instance.backup_retention_period = raw_data.get('BackupRetentionPeriod')
    rds_instance.iam_database_authentication_enabled = raw_data.get('IAMDatabaseAuthenticationEnabled')
    rds_instance.cloudwatch_logs_exports = raw_data.get('EnabledCloudwatchLogsExports')
    return rds_instance


def build_db_subnet_group(raw_data: dict) -> DbSubnetGroup:
    return DbSubnetGroup(raw_data['DBSubnetGroupName'],
                         [x['SubnetIdentifier'] for x in raw_data['Subnets']],
                         raw_data['Region'],
                         raw_data['Account'],
                         raw_data['DBSubnetGroupArn'])


def build_rds_cluster(raw_data: dict) -> RdsCluster:
    return RdsCluster(raw_data['Account'],
                      raw_data['Region'],
                      raw_data['DBClusterIdentifier'],
                      raw_data['DBClusterArn'],
                      raw_data['Port'],
                      raw_data['DBSubnetGroup'],
                      [x['VpcSecurityGroupId'] for x in raw_data['VpcSecurityGroups'] if x['Status'] == 'active'],
                      get_dict_value(raw_data, 'StorageEncrypted', False),
                      raw_data['BackupRetentionPeriod'],
                      raw_data['Engine'],
                      raw_data['EngineVersion'],
                      raw_data['IAMDatabaseAuthenticationEnabled'],
                      raw_data.get('EnabledCloudwatchLogsExports'))


def build_rds_global_cluster(raw_data: dict) -> RdsGlobalCluster:
    return RdsGlobalCluster(raw_data['Account'],
                            raw_data['Region'],
                            raw_data['GlobalClusterIdentifier'],
                            raw_data['StorageEncrypted'])


def build_elastic_search_domain(raw_data: dict) -> ElasticSearchDomain:
    vpc_options = raw_data.get('VPCOptions')
    security_group_ids, subnet_ids = None, None
    if vpc_options:
        security_group_ids = vpc_options['SecurityGroupIds']
        subnet_ids = vpc_options['SubnetIds']

    enforce_https = False
    domain_endpoint_options = raw_data.get('DomainEndpointOptions')
    if domain_endpoint_options:
        enforce_https = domain_endpoint_options['EnforceHTTPS']

    encrypt_at_rest_state = False
    encrypt_at_rest_options = raw_data.get('EncryptionAtRestOptions')
    if encrypt_at_rest_options:
        encrypt_at_rest_state = encrypt_at_rest_options['Enabled']

    encrypt_node_to_node_state = False
    encrypt_node_to_node_options = raw_data.get('NodeToNodeEncryptionOptions')
    if encrypt_node_to_node_options:
        encrypt_node_to_node_state = encrypt_node_to_node_options['Enabled']

    log_publishing_options: Optional[List[LogPublishingOptions]] = []
    if raw_data.get('LogPublishingOptions'):
        for key, value in raw_data['LogPublishingOptions'].items():
            log_publishing_options.append(LogPublishingOptions(key, value['CloudWatchLogsLogGroupArn'], value['Enabled']))
    return ElasticSearchDomain(raw_data['DomainId'],
                               raw_data['DomainName'],
                               raw_data['ARN'],
                               enforce_https,
                               subnet_ids, security_group_ids,
                               encrypt_at_rest_state,
                               encrypt_node_to_node_state,
                               raw_data['Account'],
                               raw_data['Region'],
                               log_publishing_options,
                               raw_data['ElasticsearchVersion'],
                               raw_data['ElasticsearchClusterConfig']['InstanceType'])


def build_internet_gateway(igw_attribute, igw_type: IgwType, igw_key: str) -> InternetGateway:
    vpc_id: str = ""
    for attach in igw_attribute["Attachments"]:
        if "VpcId" in attach:
            vpc_id = attach["VpcId"]
            break
    return InternetGateway(vpc_id=vpc_id, igw_id=igw_attribute[igw_key], igw_type=igw_type,
                           region=igw_attribute['Region'], account=igw_attribute['Account'])


def build_vpc_internet_gateway_attachment(attributes: dict) -> List[VpcGatewayAttachment]:
    attachments: list = []
    for attach in attributes.get("Attachments", []):
        attachments.append(VpcGatewayAttachment(region=attributes['Region'],
                                                account=attributes['Account'],
                                                vpc_id=attach.get('VpcId'),
                                                gateway_id=attributes.get('InternetGatewayId')))
    return attachments


def build_load_balancer_listeners(raw_data: dict) -> LoadBalancerListener:
    listener_port = raw_data.get('Port')
    listener_protocol = raw_data.get('Protocol')
    listener_arn = raw_data['ListenerArn']
    load_balancer_arn = raw_data['LoadBalancerArn']
    default_action_type = raw_data['DefaultActions'][0]['Type']
    redirect_action_protocol = None
    redirect_action_port = None
    if default_action_type.lower() == 'redirect':
        redirect_action_protocol = raw_data['DefaultActions'][0]['RedirectConfig']['Protocol']
        redirect_action_port = raw_data['DefaultActions'][0]['RedirectConfig']['Port']
    return LoadBalancerListener(listener_arn,
                                listener_port,
                                listener_protocol,
                                load_balancer_arn,
                                raw_data['Account'],
                                raw_data['Region'],
                                default_action_type,
                                redirect_action_protocol,
                                redirect_action_port)


def build_eks_cluster(raw_data: dict) -> EksCluster:
    vpc_config = raw_data['Value']['resourcesVpcConfig']
    return EksCluster(raw_data['Value']['name'],
                      raw_data['Value']['arn'],
                      raw_data['Value']['roleArn'],
                      raw_data['Value']['endpoint'],
                      vpc_config['securityGroupIds'],
                      vpc_config['clusterSecurityGroupId'],
                      vpc_config['subnetIds'],
                      vpc_config['endpointPublicAccess'],
                      vpc_config['endpointPrivateAccess'],
                      vpc_config['publicAccessCidrs'],
                      raw_data['Account'],
                      raw_data['Region'])


def build_cloudfront_distribution_list(raw_data: dict) -> List[CloudFrontDistribution]:
    distributions: List[CloudFrontDistribution] = []

    for attributes in get_dict_value(raw_data['Value'], 'Items', []):
        web_acl_id = attributes['WebACLId']
        viewer_cert_dict = attributes['ViewerCertificate']
        viewer_cert: ViewerCertificate = ViewerCertificate(cloudfront_default_certificate=viewer_cert_dict.get('CloudFrontDefaultCertificate', False),
                                                           minimum_protocol_version=get_dict_value(viewer_cert_dict,
                                                                                                   'MinimumProtocolVersion', 'TLSv1'))
        cache_behavior_list: List[CacheBehavior] = []
        order: int = 0
        for cache_behavior_dict in [attributes['DefaultCacheBehavior']] + \
                                   get_dict_value(get_dict_value(attributes, 'CacheBehaviors', []), 'Items', []):
            cache_behavior: CacheBehavior = CacheBehavior(allowed_methods=cache_behavior_dict['AllowedMethods']['Items'],
                                                          cached_methods=cache_behavior_dict['AllowedMethods']['CachedMethods']['Items'],
                                                          target_origin_id=cache_behavior_dict['TargetOriginId'],
                                                          viewer_protocol_policy=cache_behavior_dict['ViewerProtocolPolicy'],
                                                          trusted_signers=get_dict_value(cache_behavior_dict.get('TrustedSigners'), 'Items', []),
                                                          precedence=order,
                                                          field_level_encryption_id=cache_behavior_dict.get('FieldLevelEncryptionId'))

            if 'PathPattern' in cache_behavior_dict:
                cache_behavior.path_pattern = cache_behavior_dict['PathPattern']
            cache_behavior_list.append(cache_behavior)
            order += 1

        origin_config_list: List[OriginConfig] = []
        for origin_dict in attributes['Origins']['Items']:
            oai_path: str = origin_dict['S3OriginConfig']['OriginAccessIdentity'] if 'S3OriginConfig' in origin_dict else None
            origin_config: OriginConfig = OriginConfig(domain_name=origin_dict['DomainName'],
                                                       origin_id=origin_dict['Id'],
                                                       oai_path=oai_path)
            origin_config_list.append(origin_config)
        distributions.append(CloudFrontDistribution(attributes['ARN'],
                                                    attributes['DomainName'],
                                                    attributes['Id'],
                                                    raw_data['Account'],
                                                    viewer_cert,
                                                    cache_behavior_list,
                                                    origin_config_list,
                                                    web_acl_id))
    return distributions


def build_cloudfront_distribution_logging(attributes: dict) -> CloudfrontDistributionLogging:
    logging_attributes = attributes['Value']
    return CloudfrontDistributionLogging(logging_attributes['ARN'],
                                         logging_attributes['DomainName'],
                                         logging_attributes['Id'],
                                         attributes['Account'],
                                         logging_attributes['DistributionConfig']['Logging']['IncludeCookies'],
                                         get_dict_value(logging_attributes['DistributionConfig']['Logging'], 'Bucket', None),
                                         get_dict_value(logging_attributes['DistributionConfig']['Logging'], 'Prefix', None),
                                         logging_attributes['DistributionConfig']['Logging']['Enabled'])


def origin_access_identity_builder(attributes: dict) -> List[OriginAccessIdentity]:
    return [OriginAccessIdentity(attributes['Account'],
                                 attributes['Region'],
                                 item['Id'],
                                 "origin-access-identity/cloudfront/{}".format(item['Id']),
                                 "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {}".format(item['Id']),
                                 item['S3CanonicalUserId']) for item in attributes['Value']['Items']]


def build_launch_template(raw_data: dict) -> LaunchTemplate:
    template_data = raw_data['LaunchTemplateData']
    http_token = get_dict_value(get_dict_value(template_data, 'MetadataOptions', {}), 'HttpTokens', 'optional')
    image_id = template_data.get('ImageId')
    instance_type = template_data.get('InstanceType')
    ebs_optimized = template_data.get('EbsOptimized', False)
    monitoring_enabled = False
    if template_data.get('Monitoring'):
        monitoring_enabled = template_data['Monitoring']['Enabled']
    security_group_ids = get_dict_value(template_data, 'SecurityGroupIds', [])
    iam_instance_profile = get_dict_value(template_data, 'IamInstanceProfile', {}).get('Name')
    network_configurations: List[NetworkConfiguration] = []

    for net_conf in get_dict_value(template_data, 'NetworkInterfaces', []):
        assign_public_ip: Optional[bool] = get_dict_value(net_conf, 'AssociatePublicIpAddress', None)
        security_groups: List[str] = get_dict_value(net_conf, 'Groups', [])
        subnet_id: str = get_dict_value(net_conf, 'SubnetId', None)
        network_configurations.append(NetworkConfiguration(assign_public_ip=assign_public_ip, security_groups_ids=security_groups,
                                                           subnet_list_ids=[subnet_id] if subnet_id else []))
    return LaunchTemplate(raw_data['LaunchTemplateId'],
                          raw_data['LaunchTemplateName'],
                          http_token,
                          image_id,
                          security_group_ids,
                          raw_data['VersionNumber'],
                          raw_data["Region"],
                          raw_data['Account'],
                          iam_instance_profile,
                          ebs_optimized,
                          monitoring_enabled,
                          instance_type,
                          network_configurations)


def build_prefix_lists(raw_data: dict) -> PrefixLists:
    pl_lists: PrefixLists = PrefixLists(raw_data["Region"])
    for pl_dict in raw_data["Value"]["PrefixLists"]:
        pl_lists.prefix_lists.append(PrefixList(pl_id=pl_dict["PrefixListId"],
                                                pl_name=pl_dict["PrefixListName"],
                                                cidr_list=pl_dict["Cidrs"],
                                                region=raw_data["Region"]))
    return pl_lists


def build_athena_workgroup(raw_data: dict) -> AthenaWorkgroup:
    workgroup = raw_data['Value']
    kms_key_id = get_dict_value(workgroup['Configuration']['ResultConfiguration'], 'EncryptionConfiguration', {}).get('KmsKey')
    if kms_key_id and is_valid_arn(kms_key_id):
        kms_key_id = kms_key_id.split('/')[1]
    return AthenaWorkgroup(workgroup['Name'],
                           workgroup['State'],
                           bool(workgroup['Configuration']['ResultConfiguration'].get('EncryptionConfiguration')),
                           workgroup['Configuration']['EnforceWorkGroupConfiguration'],
                           get_dict_value(workgroup['Configuration']['ResultConfiguration'], 'EncryptionConfiguration', {}).get('EncryptionOption'),
                           kms_key_id,
                           raw_data['Region'],
                           raw_data['Account'])


def build_rest_api_gw(raw_data: dict) -> RestApiGw:
    api_gw_type = ApiGatewayType.EDGE.value
    if raw_data.get('endpointConfiguration', {}).get('types'):
        api_gw_type = ApiGatewayType(raw_data['endpointConfiguration']['types'][0])
    return RestApiGw(raw_data['id'],
                     raw_data['name'],
                     raw_data['Region'],
                     raw_data['Account'],
                     api_gw_type)


def build_api_gateway_method_settings(raw_data: dict) -> Optional[List[ApiGatewayMethodSettings]]:
    # First validate that the item has methods, otherwise, no point to check anything.
    rest_api_gw_method_settings: List[ApiGatewayMethodSettings] = []
    api_gw_id = str(raw_data['FilePath']).split('apigateway-get-stages/')[1].replace('restApiId-', '').replace('.json', '')
    for method_path in raw_data.get('methodSettings', {}):
        method_settings = raw_data['methodSettings'][method_path]
        http_method = method_path.split('/')[-1]
        http_method = RestApiMethod.ANY if http_method == '*' else RestApiMethod(http_method)
        caching_enabled = method_settings['cachingEnabled']
        caching_encrypted = method_settings['cacheDataEncrypted']
        rest_api_gw_method_settings.append(ApiGatewayMethodSettings(api_gw_id,
                                                                    raw_data['stageName'],
                                                                    method_path,
                                                                    http_method,
                                                                    caching_enabled,
                                                                    caching_encrypted,
                                                                    raw_data['Region'],
                                                                    raw_data['Account']))
    return rest_api_gw_method_settings


def build_api_gateway_stage(attributes: dict) -> ApiGatewayStage:
    access_logs: Optional[AccessLogsSettings] = None
    access_logs_data = attributes.get('accessLogSettings')
    if access_logs_data:
        access_logs = AccessLogsSettings(access_logs_data['destinationArn'], access_logs_data['format'])
    return ApiGatewayStage(attributes['Account'],
                           attributes['Region'],
                           str(attributes['FilePath']).split('apigateway-get-stages/')[1].replace('restApiId-', '').replace('.json', ''),
                           attributes['stageName'],
                           attributes['tracingEnabled'],
                           access_logs)


def build_api_gateway_method(attributes: dict) -> ApiGatewayMethod:
    rest_api_id, resource_id = _parse_apigateway_params_from_file_name(attributes)
    region: str = attributes['Region']
    account_id = attributes['Account']
    attributes = attributes['Value']
    return ApiGatewayMethod(account=account_id, region=region,
                            rest_api_id=rest_api_id, resource_id=resource_id,
                            http_method=RestApiMethod(attributes['httpMethod']),
                            authorization=attributes['authorizationType'])


def build_api_gateway_integration(attributes: dict) -> ApiGatewayIntegration:
    rest_api_id, resource_id = _parse_apigateway_params_from_file_name(attributes)
    region: str = attributes['Region']
    account_id = attributes['Account']
    request_http_method = attributes['request_http_method']
    attributes = attributes['Value'].get('methodIntegration')
    integration_type = IntegrationType(attributes.get('type')) if attributes else IntegrationType.NONE
    uri: str = attributes.get('uri') if attributes else None
    integration_http_method = attributes.get('httpMethod') if attributes else None
    integration_http_method = integration_http_method if integration_http_method else None
    return ApiGatewayIntegration(account=account_id, region=region,
                                 rest_api_id=rest_api_id, resource_id=resource_id,
                                 request_http_method=RestApiMethod(request_http_method),
                                 integration_http_method=RestApiMethod(integration_http_method),
                                 integration_type=integration_type,
                                 uri=uri)


def _parse_apigateway_params_from_file_name(attributes: dict) -> Tuple[str, str]:
    file_name: str = os.path.basename(attributes['FilePath'])
    params = file_name.replace('restApiId-', '')
    params = params[0:params.index('_httpMethod-')]
    params = params.split('_resourceId-')
    rest_api_id: str = params[0]
    resource_id: str = params[1]
    return rest_api_id, resource_id


def build_dynamodb_table(attributes: dict) -> DynamoDbTable:
    region = attributes["Region"]
    account = attributes["Account"]
    attributes = attributes["Value"]
    fields: List[TableField] = [TableField(field_attr["AttributeName"], TableFieldType(field_attr["AttributeType"]))
                                for field_attr in attributes["AttributeDefinitions"]]
    write_capacity: int = 0
    read_capacity: int = 0
    if "ProvisionedThroughput" in attributes:
        write_capacity = attributes["ProvisionedThroughput"]["WriteCapacityUnits"]
        read_capacity = attributes["ProvisionedThroughput"]["ReadCapacityUnits"]
    billing_mode: BillingMode = BillingMode.PROVISIONED
    if "BillingModeSummary" in attributes:
        billing_mode = BillingMode(attributes["BillingModeSummary"]["BillingMode"])
    partition_key: str = ""
    sort_key: Optional[str] = None
    for key_attr in attributes["KeySchema"]:
        if key_attr["KeyType"] == "HASH":
            partition_key = key_attr["AttributeName"]
        else:
            sort_key = key_attr["AttributeName"]

    server_side_encryption = False
    kms_key_id = None
    if 'SSEDescription' in attributes:
        server_side_encryption = bool(attributes['SSEDescription']['Status'] == 'ENABLED')
        kms_key_id = attributes['SSEDescription']['KMSMasterKeyArn']
    return DynamoDbTable(table_name=attributes["TableName"],
                         region=region,
                         account=account,
                         table_arn=attributes["TableArn"],
                         billing_mode=billing_mode, partition_key=partition_key,
                         sort_key=sort_key, write_capacity=write_capacity,
                         read_capacity=read_capacity, fields_attributes=fields,
                         server_side_encryption=server_side_encryption, kms_key_id=kms_key_id)


def build_nat_gateways(attributes: dict) -> NatGateways:
    addresses: dict = attributes["NatGatewayAddresses"][0]
    return NatGateways(nat_gateway_id=attributes["NatGatewayId"], allocation_id=addresses["AllocationId"],
                       subnet_id=attributes["SubnetId"], eni_id=addresses["NetworkInterfaceId"],
                       private_ip=addresses["PrivateIp"], public_ip=addresses["PublicIp"],
                       account=attributes['Account'], region=attributes['Region'])


def build_ec2_image(attributes: dict) -> Ec2Image:
    return Ec2Image(attributes['ImageId'],
                    attributes['Public'],
                    attributes['Region'],
                    attributes['Account'])


def build_dax_cluster(attributes: dict) -> DaxCluster:
    server_side_encryption = False
    if attributes['SSEDescription']:
        if 'ENABL' in attributes['SSEDescription']['Status']:
            server_side_encryption = True
    return DaxCluster(attributes['ClusterName'],
                      server_side_encryption,
                      attributes['ClusterArn'],
                      attributes['Region'],
                      attributes['Account'])


def build_docdb_cluster(attributes: dict) -> DocumentDbCluster:
    return DocumentDbCluster(attributes['DBClusterIdentifier'],
                             attributes['StorageEncrypted'],
                             attributes['DBClusterParameterGroup'],
                             attributes.get('KmsKeyId'),
                             attributes['Region'],
                             attributes['Account'],
                             attributes['DBClusterArn'],
                             attributes.get('EnabledCloudwatchLogsExports', []))


def build_docdb_cluster_parameter_group(attributes: dict) -> DocDbClusterParameterGroup:
    list_parameters = []
    for parameter in attributes['Value']['Parameters']:
        list_parameters.append(DocDbClusterParameter(parameter.get('ParameterName'), parameter.get('ParameterValue')))
    return DocDbClusterParameterGroup(list_parameters,
                                      extract_attribute_from_file_path(attributes['FilePath'], ['DBClusterParameterGroupName-']),
                                      attributes['Account'],
                                      attributes['Region'])


def build_s3_bucket_encryption(attributes: dict) -> S3BucketEncryption:
    return S3BucketEncryption(extract_attribute_from_file_path(attributes['FilePath'], ['Bucket-']),
                              True,
                              attributes['Region'],
                              attributes['Account'])


def build_s3_bucket_versioning(attributes: dict) -> S3BucketVersioning:
    bucket_versioning = False
    if get_dict_value(attributes, 'Value', {}).get('Status') == 'Enabled':
        bucket_versioning = True
    return S3BucketVersioning(extract_attribute_from_file_path(attributes['FilePath'], ['Bucket-']),
                              bucket_versioning,
                              attributes['Account'],
                              attributes['Region'])


def build_code_build_projects(attributes: dict) -> CodeBuildProject:
    vpc_config: Optional[NetworkConfiguration] = None
    if attributes.get('vpcConfig'):
        vpc_config = NetworkConfiguration(False, attributes['vpcConfig']['securityGroupIds'],
                                          attributes['vpcConfig']['subnets'])
    return CodeBuildProject(attributes['name'],
                            attributes['encryptionKey'],
                            attributes['arn'],
                            attributes['Account'],
                            attributes['Region'],
                            vpc_config)


def build_code_build_report_group(attributes: dict) -> CodeBuildReportGroup:
    return CodeBuildReportGroup(attributes['Account'],
                                attributes['Region'],
                                attributes['name'],
                                attributes['exportConfig']['exportConfigType'],
                                attributes['exportConfig']['s3Destination']['bucket'],
                                attributes['exportConfig']['s3Destination']['encryptionKey'],
                                attributes['exportConfig']['s3Destination']['encryptionDisabled'],
                                attributes['arn'])


def build_cloudtrail(attributes: dict) -> CloudTrail:
    kms_encryption = False
    if attributes.get('KmsKeyId'):
        kms_encryption = True
    return CloudTrail(attributes['Name'],
                      kms_encryption,
                      attributes['TrailARN'],
                      attributes['LogFileValidationEnabled'],
                      attributes['Region'],
                      attributes['Account'],
                      attributes['IsMultiRegionTrail'])


def build_cloud_watch_log_groups(attributes: dict) -> CloudWatchLogGroup:
    arn: str = attributes['arn']
    if arn.endswith(':*'):
        arn = arn[:-2]
    return CloudWatchLogGroup(attributes['logGroupName'],
                              attributes.get('kmsKeyId'),
                              arn,
                              attributes.get('retentionInDays'),
                              attributes['Region'],
                              attributes['Account'])


def build_kms_key(attributes: dict) -> KmsKey:
    key = attributes['Value']
    return KmsKey(key['KeyId'],
                  key['Arn'],
                  KeyManager(key['KeyManager']),
                  attributes['Region'],
                  attributes['Account'])


def build_sqs_queue(attributes: dict) -> SqsQueue:
    encrypted_at_rest = False
    sqs_queue_resource = SqsQueue(attributes['Value']['QueueArn'],
                                  attributes['Value']['QueueArn'].split(':')[-1],
                                  encrypted_at_rest,
                                  attributes['Account'],
                                  attributes['Region'],
                                  urllib.parse.unquote(extract_attribute_from_file_path(attributes['FilePath'], ['QueueUrl-', '_AttributeNames'])))
    if attributes['Value'].get('KmsMasterKeyId'):
        sqs_queue_resource.encrypted_at_rest = True
        sqs_queue_resource.kms_key = attributes['Value'].get('KmsMasterKeyId')
    return sqs_queue_resource


def build_elasti_cache_replication_group(attributes: dict) -> ElastiCacheReplicationGroup:
    return ElastiCacheReplicationGroup(attributes['ReplicationGroupId'],
                                       attributes['AtRestEncryptionEnabled'],
                                       attributes['TransitEncryptionEnabled'],
                                       attributes['Region'],
                                       attributes['Account']).with_aliases(attributes['ReplicationGroupId']
                                                                           + attributes['Account'] + attributes['Region'])


def build_sns_topic(attributes: dict) -> SnsTopic:
    sns_topic = attributes['Value']
    encrypted_at_rest = False
    sns_topic_resource = SnsTopic(sns_topic['TopicArn'],
                                  sns_topic['TopicArn'].split(':')[-1],
                                  encrypted_at_rest,
                                  attributes['Region'],
                                  attributes['Account'])
    if sns_topic.get('KmsMasterKeyId'):
        sns_topic_resource.encrypted_at_rest = True
        sns_topic_resource.kms_key = sns_topic.get('KmsMasterKeyId')
    return sns_topic_resource


def build_sqs_queue_policy(attributes: dict) -> SqsQueuePolicy:
    policy_statements = []
    if attributes['Value'].get('Policy'):
        policy_statements = _build_policy_statements(json.loads(attributes['Value']['Policy'])['Statement'])
    return SqsQueuePolicy(attributes['Value']['QueueArn'].split(':')[-1],
                          policy_statements,
                          attributes['Value'].get('Policy', []),
                          attributes['Account'])


def build_neptune_cluster(attributes: dict) -> NeptuneCluster:
    neptune_cluster_resource = NeptuneCluster(attributes['DBClusterIdentifier'],
                                              attributes['DBClusterArn'],
                                              attributes['StorageEncrypted'],
                                              attributes['Region'],
                                              attributes['Account'],
                                              attributes['Port'],
                                              attributes['DBSubnetGroup'],
                                              [x['VpcSecurityGroupId'] for x in attributes['VpcSecurityGroups'] if x['Status'] == 'active'],
                                              attributes['DBClusterIdentifier'],
                                              attributes.get('EnabledCloudwatchLogsExports'))
    if attributes.get('KmsKeyId'):
        neptune_cluster_resource.kms_key = attributes['KmsKeyId']
    return neptune_cluster_resource


def build_neptune_instance(attributes: dict) -> List[NeptuneInstance]:
    neptune_instances_list: List[NeptuneInstance] = []
    neptune_instances = [instance_data for instance_data in attributes['Value']['DBInstances'] if 'neptune' in instance_data['Endpoint']['Address']]
    for instance_data in neptune_instances:
        neptune_instances_list.append(NeptuneInstance(attributes['Account'],
                                                      attributes['Region'],
                                                      instance_data['DBInstanceIdentifier'],
                                                      instance_data['DBInstanceArn'],
                                                      instance_data['Endpoint']['Port'],
                                                      instance_data['DBClusterIdentifier'],
                                                      instance_data['PubliclyAccessible'],
                                                      instance_data['DBInstanceIdentifier']))
    return neptune_instances_list

def build_ecr_repository(attributes: dict) -> EcrRepository:
    return EcrRepository(attributes['repositoryName'],
                         attributes['repositoryArn'],
                         attributes['Region'],
                         attributes['Account'],
                         attributes['imageTagMutability'],
                         attributes['imageScanningConfiguration']['scanOnPush'],
                         attributes['encryptionConfiguration']['encryptionType'],
                         attributes['encryptionConfiguration'].get('kmsKey'))


def build_ecr_repository_policy(attributes: dict) -> EcrRepositoryPolicy:
    return EcrRepositoryPolicy(attributes['Value']['repositoryName'],
                               _build_policy_statements(json.loads(attributes['Value']['policyText'])['Statement']),
                               attributes['Value']['policyText'],
                               attributes['Account'],
                               attributes['Region'])


def build_cloudwatch_logs_destination(attributes: dict) -> CloudWatchLogsDestination:
    return CloudWatchLogsDestination(attributes['Account'],
                                     attributes['Region'],
                                     attributes['destinationName'],
                                     attributes['arn'])


def build_cloudwatch_logs_policy_destination(attributes: dict) -> CloudWatchLogsDestinationPolicy:
    policy = []
    if attributes.get('accessPolicy'):
        policy = _build_policy_statements(json.loads(attributes['accessPolicy'])['Statement'])
    return CloudWatchLogsDestinationPolicy(attributes['destinationName'],
                                           policy,
                                           attributes['accessPolicy'],
                                           attributes['Region'],
                                           attributes['Account'])


def build_rest_api_gw_policy(attributes: dict) -> RestApiGwPolicy:
    policy = []
    raw_document = ''
    if attributes.get('policy'):
        policy_string = attributes['policy']
        raw_document = f'"{policy_string}"'
        policy = _build_policy_statements(ast.literal_eval(json.loads(raw_document))['Statement'])
    return RestApiGwPolicy(attributes['id'],
                           policy,
                           raw_document,
                           attributes['Account'])


def build_kms_key_policy(attributes: dict) -> KmsKeyPolicy:
    key_id = os.path.basename(attributes['FilePath'])
    find_key_id = re.search(r'KeyId-(.*)_.*', key_id)
    if find_key_id:
        key_id = find_key_id.group(1)
    return KmsKeyPolicy(os.path.basename(key_id),
                        _build_policy_statements(json.loads(attributes['Value']['Policy'])['Statement']),
                        attributes['Value']['Policy'],
                        attributes['Account'])


def build_elastic_search_domain_policy(attributes: dict) -> ElasticSearchDomainPolicy:
    policy = []
    if attributes.get('AccessPolicies'):
        policy = _build_policy_statements(json.loads(attributes['AccessPolicies'])['Statement'])
    return ElasticSearchDomainPolicy(attributes['DomainName'],
                                     policy,
                                     attributes['AccessPolicies'],
                                     attributes['Account'])


def build_lambda_function(attributes: dict) -> LambdaFunction:
    vpc_config: Optional[NetworkConfiguration] = None
    if 'VpcConfig' in attributes:
        vpc_config = NetworkConfiguration(False, attributes['VpcConfig']['SecurityGroupIds'],
                                          attributes['VpcConfig']['SubnetIds'])
    arn = qualified_arn = attributes['FunctionArn']
    return LambdaFunction(account=attributes['Account'],
                          region=attributes['Region'],
                          function_name=attributes['FunctionName'],
                          lambda_func_version=attributes['Version'],
                          arn=arn,
                          qualified_arn=qualified_arn,
                          role_arn=attributes['Role'],
                          handler=attributes['Handler'],
                          runtime=attributes['Runtime'],
                          vpc_config=vpc_config,
                          xray_tracing_enabled=bool(attributes['TracingConfig']['Mode'] == 'Active'))


def build_lambda_policy(attributes: dict) -> LambdaPolicy:
    lambda_function_name: str = extract_attribute_from_file_path(attributes['FilePath'], ['FunctionName-']).split('_Qualifier')[0]
    statements: List[PolicyStatement] = build_policy_statements_from_str(attributes['Value'])
    # each statement should contains exactly 1 one resource (lambda arn itself)
    qualifier: Optional[str] = LambdaFunction.parse_qualifier_from_arn(statements[0].resources[0])
    return LambdaPolicy(account=attributes['Account'],
                                  region=attributes['Region'],
                                  function_name=lambda_function_name,
                                  statements=statements,
                                  qualifier=qualifier)


def build_lambda_alias(attributes: dict) -> LambdaAlias:
    lambda_function_name = extract_attribute_from_file_path(attributes['FilePath'], ['FunctionName-'])
    return LambdaAlias(account=attributes['Account'],
                       region=attributes['Region'],
                       arn=attributes['AliasArn'],
                       name=attributes['Name'],
                       function_name_or_arn=lambda_function_name,
                       function_version=attributes['FunctionVersion'],
                       description=attributes.get('Description', None))


def build_glacier_vault(attributes: dict) -> GlacierVault:
    return GlacierVault(attributes['VaultName'],
                        attributes['VaultARN'],
                        attributes['Region'],
                        attributes['Account'])


def build_glacier_vault_policy(attributes: dict) -> GlacierVaultPolicy:
    policy = build_policy_statements_from_str(attributes['Value']['Policy'])
    return GlacierVaultPolicy(policy[0].resources[0],
                              policy,
                              attributes['Value']['Policy'],
                              attributes['Account'])


def build_efs(attributes: dict) -> ElasticFileSystem:
    return ElasticFileSystem(attributes['CreationToken'],
                             attributes['FileSystemId'],
                             attributes.get('FileSystemArn'),
                             bool(attributes.get('Encrypted')),
                             attributes['Region'],
                             attributes['Account'])


def build_efs_policy(attributes: dict) -> EfsPolicy:
    return EfsPolicy(attributes['Value']['FileSystemId'],
                     build_policy_statements_from_str(attributes['Value']['Policy']),
                     attributes['Value']['Policy'],
                     attributes['Account'],
                     attributes['Region'])


def build_glue_data_catalog_policy(attributes: dict) -> GlueDataCatalogPolicy:
    return GlueDataCatalogPolicy(build_policy_statements_from_str(attributes['Value']['PolicyInJson']),
                                 attributes['Value']['PolicyInJson'],
                                 attributes['Account'],
                                 attributes['Region'])


def build_secrets_manager_secret(attributes: dict) -> SecretsManagerSecret:
    secrets_manager_secret_resource = SecretsManagerSecret(attributes['Name'],
                                                           attributes['ARN'],
                                                           attributes['Region'],
                                                           attributes['Account'])
    if attributes.get('KmsKeyId'):
        secrets_manager_secret_resource.kms_key = attributes['KmsKeyId']
    return secrets_manager_secret_resource


def build_secrets_manager_secret_policy(attributes: dict) -> SecretsManagerSecretPolicy:
    return SecretsManagerSecretPolicy(attributes['Value']['ARN'],
                                      build_policy_statements_from_str(attributes['Value'].get('ResourcePolicy')),
                                      attributes['Value'].get('ResourcePolicy'),
                                      attributes['Account'])


def build_rest_api_gw_mapping(attributes: dict) -> RestApiGwMapping:
    return RestApiGwMapping(attributes['restApiId'],
                            extract_attribute_from_file_path(attributes['FilePath'], ['domainName-']),
                            attributes['Region'],
                            attributes['Account'])


def build_rest_api_gw_domain(attributes: dict) -> RestApiGwDomain:
    return RestApiGwDomain(attributes['domainName'],
                           attributes['securityPolicy'],
                           attributes['Account'],
                           attributes['Region'])


def build_kinesis_stream(attributes: dict) -> KinesisStream:
    kinesis = attributes['Value']
    return KinesisStream(kinesis['StreamName'],
                         kinesis['StreamARN'],
                         bool(kinesis['EncryptionType'] == 'KMS'),
                         attributes['Region'],
                         attributes['Account'])


def build_glue_data_catalog_crawler(attributes: dict) -> GlueCrawler:
    return GlueCrawler(attributes['Name'],
                       attributes['DatabaseName'],
                       attributes['Account'],
                       attributes['Region'])


def build_glue_data_catalog_table(attributes: dict) -> GlueDataCatalogTable:
    return GlueDataCatalogTable(attributes['Name'],
                                attributes['DatabaseName'],
                                attributes['Account'],
                                attributes['Region'])


def build_xray_encryption(attributes: dict) -> XrayEncryption:
    xray = attributes['Value']
    return XrayEncryption(xray.get('KeyId'),
                          attributes['Region'],
                          attributes['Account'])


def build_kinesis_firehose_stream(attributes: dict) -> KinesisFirehoseStream:
    es_domain_arn = None
    es_vpc_config: NetworkConfiguration = None
    if attributes['Value']['Destinations'][0].get('ElasticsearchDestinationDescription'):
        es_domain_config = attributes['Value']['Destinations'][0]['ElasticsearchDestinationDescription']
        es_domain_arn = es_domain_config['DomainARN']
        if es_domain_config.get('VpcConfigurationDescription'):
            es_vpc_configurations = es_domain_config['VpcConfigurationDescription']
            es_vpc_config = NetworkConfiguration(False, es_vpc_configurations['SecurityGroupIds'], es_vpc_configurations['SubnetIds'])
    return KinesisFirehoseStream(attributes['Value']['DeliveryStreamName'],
                                 attributes['Value']['DeliveryStreamARN'],
                                 attributes['Value']['DeliveryStreamEncryptionConfiguration']['Status'] == 'ENABLED',
                                 attributes['Account'],
                                 attributes['Region'],
                                 es_domain_arn,
                                 es_vpc_config)


def build_workspace(attributes: dict) -> Workspace:
    return Workspace(attributes['Region'],
                     attributes['Account'],
                     attributes['WorkspaceId'],
                     get_dict_value(attributes, 'RootVolumeEncryptionEnabled', False),
                     get_dict_value(attributes, 'UserVolumeEncryptionEnabled', False),
                     attributes.get('VolumeEncryptionKey'))


def build_kms_alias(attributes: dict) -> KmsAlias:
    return KmsAlias(attributes['AliasName'],
                    attributes.get('TargetKeyId'),
                    attributes['AliasArn'],
                    attributes['Account'],
                    attributes['Region'])


def build_iam_password_policy(attributes: dict) -> IamPasswordPolicy:
    return IamPasswordPolicy(attributes['Value'].get('MinimumPasswordLength'),
                             attributes['Value'].get('RequireLowercaseCharacters'),
                             attributes['Value'].get('RequireNumbers'),
                             attributes['Value'].get('RequireUppercaseCharacters'),
                             attributes['Value'].get('RequireSymbols'),
                             attributes['Value'].get('AllowUsersToChangePassword'),
                             attributes['Value'].get('MaxPasswordAge', 0),
                             attributes['Value'].get('PasswordReusePrevention', 0),
                             attributes['Account'])


def build_resources_tagging_list(attributes: dict) -> ResourceTagMappingList:
    return ResourceTagMappingList(attributes['ResourceARN'],
                                  attributes['Region'],
                                  attributes['Account'])


def build_ssm_parameter(attributes: dict) -> SsmParameter:
    return SsmParameter(attributes['Name'],
                        attributes['Type'],
                        attributes.get('KeyId'),
                        attributes['Account'],
                        attributes['Region'])


def build_dms_replication_instance(attributes: dict) -> DmsReplicationInstance:
    subnet_group_data = attributes['ReplicationSubnetGroup']
    return DmsReplicationInstance(attributes['Account'],
                                  attributes['Region'],
                                  attributes['ReplicationInstanceIdentifier'],
                                  attributes['ReplicationInstanceArn'],
                                  attributes['PubliclyAccessible'],
                                  subnet_group_data.get('ReplicationSubnetGroupIdentifier'),
                                  [sg['VpcSecurityGroupId'] for sg in attributes['VpcSecurityGroups'] if sg['Status'] == 'active'])


def build_dms_replication_instance_subnet_group(attributes: dict) -> DmsReplicationInstanceSubnetGroup:
    return DmsReplicationInstanceSubnetGroup(attributes['Account'],
                                             attributes['Region'],
                                             attributes.get('ReplicationSubnetGroupIdentifier'),
                                             [subnet['SubnetIdentifier'] for subnet in attributes['Subnets']
                                              if subnet['SubnetStatus'] == 'Active'],
                                             attributes['VpcId']).with_aliases(attributes.get('ReplicationSubnetGroupIdentifier')
                                                                               + attributes['Account'] + attributes['Region'])


def build_sagemaker_endpoint_config(attributes: dict) -> SageMakerEndpointConfig:
    return SageMakerEndpointConfig(attributes['Value']['EndpointConfigName'],
                                   attributes['Value']['EndpointConfigArn'],
                                   bool(attributes['Value'].get('KmsKeyId')),
                                   attributes['Region'],
                                   attributes['Account'])


def build_sagemaker_notebook_instance(attributes: dict) -> SageMakerNotebookInstance:
    return SageMakerNotebookInstance(attributes['Value']['NotebookInstanceName'],
                                     attributes['Value']['NotebookInstanceArn'],
                                     attributes['Value'].get('KmsKeyId'),
                                     attributes['Region'],
                                     attributes['Account'],
                                     bool(attributes['Value']['DirectInternetAccess'] == 'Enabled'))


def build_elasticache_cluster(attributes: dict) -> ElastiCacheCluster:
    engine = 'redis'
    if attributes.get('ReplicationGroupId') is None:
        engine = attributes['Engine']
    return ElastiCacheCluster(attributes['Region'],
                              attributes['Account'],
                              attributes['CacheClusterId'],
                              attributes['ARN'],
                              attributes.get('ReplicationGroupId'),
                              [security_group_details['SecurityGroupId']
                               for security_group_details in attributes.get('SecurityGroups', {})
                               if security_group_details and security_group_details['Status'] == 'active'],
                              attributes['SnapshotRetentionLimit'],
                              engine,
                              attributes['CacheSubnetGroupName'])


def build_elasticache_subnet_group(attributes: dict) -> ElastiCacheSubnetGroup:
    return ElastiCacheSubnetGroup(attributes['Account'],
                                  attributes['Region'],
                                  attributes['CacheSubnetGroupName'],
                                  [subnet['SubnetIdentifier'] for subnet in attributes['Subnets']])


def build_efs_mount_target_base(attributes: dict) -> EfsMountTarget:
    return EfsMountTarget(attributes['Account'],
                          attributes['Region'],
                          attributes['FileSystemId'],
                          attributes['MountTargetId'],
                          attributes['NetworkInterfaceId'],
                          attributes['SubnetId'],
                          None)


def build_efs_mount_target_security_groups(attributes: dict) -> MountTargetSecurityGroups:
    return MountTargetSecurityGroups(attributes['Value']['SecurityGroups'],
                                     extract_attribute_from_file_path(attributes['FilePath'], ['MountTargetId-']))


def build_workspaces_directory(attributes: dict) -> WorkspaceDirectory:
    security_group_ids = [attributes['WorkspaceSecurityGroupId']]
    if attributes['WorkspaceCreationProperties'].get('CustomSecurityGroupId'):
        security_group_ids.append(attributes['WorkspaceCreationProperties']['CustomSecurityGroupId'])
    return WorkspaceDirectory(attributes['Account'],
                              attributes['Region'],
                              attributes['DirectoryId'],
                              attributes['SubnetIds'],
                              security_group_ids)


def build_directory_service(attributes: dict) -> DirectoryService:
    vpc_settings = attributes.get('VpcSettings')
    if vpc_settings:
        vpc_config = NetworkConfiguration(False, [vpc_settings['SecurityGroupId']], vpc_settings['SubnetIds'])
        vpc_id = vpc_settings['VpcId']
    else:
        vpc_settings = attributes['OwnerDirectoryDescription']['VpcSettings']
        vpc_config = NetworkConfiguration(False, [], vpc_settings['SubnetIds'])
        vpc_id = vpc_settings['VpcId']
    return DirectoryService(attributes['Account'],
                            attributes['Region'],
                            attributes['Name'],
                            attributes['DirectoryId'],
                            vpc_id,
                            attributes['Type'],
                            vpc_config)


def build_load_balancer_attributes(attributes: dict) -> LoadBalancerAttributes:
    attributes_dict = {}
    for attribute in attributes['Value']['Attributes']:
        if attribute['Value'] == 'true':
            attributes_dict.update({attribute['Key']: True})
        elif attribute['Value'] == 'false':
            attributes_dict.update({attribute['Key']: False})
        else:
            attributes_dict.update({attribute['Key']: attribute['Value']})
    lb_access_logs = LoadBalancerAccessLogs(attributes_dict['access_logs.s3.bucket'],
                                            attributes_dict['access_logs.s3.prefix'],
                                            attributes_dict['access_logs.s3.enabled'])
    return LoadBalancerAttributes(attributes['Account'],
                                  attributes['Region'],
                                  urllib.parse.unquote(extract_attribute_from_file_path(attributes['FilePath'], ['LoadBalancerArn-'])),
                                  attributes_dict.get('routing.http.drop_invalid_header_fields.enabled', False),
                                  lb_access_logs)


def build_batch_compute_environment(attributes: dict) -> BatchComputeEnvironment:
    vpc_config: NetworkConfiguration = None
    if attributes.get('computeResources', {}).get('securityGroupIds'):
        batch_settings = attributes['computeResources']
        vpc_config = NetworkConfiguration(False, batch_settings['securityGroupIds'], batch_settings['subnets'])
    return BatchComputeEnvironment(attributes['computeEnvironmentName'],
                                   attributes['computeEnvironmentArn'],
                                   attributes['Account'],
                                   attributes['Region'],
                                   vpc_config)


def build_mq_broker(attributes: dict) -> MqBroker:
    broker_fields = attributes['Value']
    return MqBroker(broker_fields['BrokerName'],
                    broker_fields['BrokerArn'],
                    broker_fields['BrokerId'],
                    attributes['Account'],
                    attributes['Region'],
                    broker_fields['DeploymentMode'],
                    NetworkConfiguration(broker_fields['PubliclyAccessible'],
                                         broker_fields['SecurityGroups'],
                                         broker_fields['SubnetIds']))


def build_api_gateway(attributes: dict) -> ApiGateway:
    return ApiGateway(attributes['Account'],
                      attributes['Region'],
                      attributes['ApiId'],
                      attributes['Name'],
                      attributes['ProtocolType'],
                      None)


def build_api_gateway_v2_integration(attributes: dict) -> ApiGatewayV2Integration:
    rest_api_id = extract_attribute_from_file_path(attributes['FilePath'], ['ApiId-'])
    return ApiGatewayV2Integration(attributes['Account'],
                                   attributes['Region'],
                                   rest_api_id,
                                   attributes.get('ConnectionId'),
                                   attributes['IntegrationId'],
                                   RestApiMethod(attributes.get('IntegrationMethod')),
                                   IntegrationType(attributes['IntegrationType']),
                                   attributes.get('IntegrationUri'))


def build_api_gateway_v2_vpc_link(attributes: dict) -> ApiGatewayVpcLink:
    return ApiGatewayVpcLink(attributes['Account'],
                             attributes['Region'],
                             attributes['VpcLinkId'],
                             attributes['Name'],
                             None,
                             attributes['SecurityGroupIds'],
                             attributes['SubnetIds'])


def build_emr_cluster(attributes: dict) -> EmrCluster:
    master_sg_id = ''
    slave_sg_id = ''
    vpc_config: Optional[NetworkConfiguration] = None
    emr_attributes = attributes['Value']
    ec2_settings = emr_attributes.get('Ec2InstanceAttributes')
    if ec2_settings:
        subnet_ids = ec2_settings.get('RequestedEc2SubnetIds')
        master_sg_id = ec2_settings['EmrManagedMasterSecurityGroup']
        slave_sg_id = ec2_settings['EmrManagedSlaveSecurityGroup']
        security_group_ids_list = [master_sg_id,
                                   slave_sg_id,
                                   ec2_settings.get('ServiceAccessSecurityGroup')]
        security_group_ids_list.extend(ec2_settings.get('AdditionalMasterSecurityGroups'))
        security_group_ids_list.extend(ec2_settings.get('AdditionalSlaveSecurityGroups'))
        security_group_ids = [sg for sg in security_group_ids_list if sg]
        vpc_config = NetworkConfiguration(None, security_group_ids, subnet_ids)
    return EmrCluster(attributes['Account'],
                      attributes['Region'],
                      emr_attributes['Name'],
                      emr_attributes['Id'],
                      emr_attributes['ClusterArn'],
                      vpc_config,
                      master_sg_id,
                      slave_sg_id)


def build_emr_public_access_config(attributes: dict) -> EmrPublicAccessConfiguration:
    return EmrPublicAccessConfiguration(attributes['Account'],
                                        attributes['Region'],
                                        attributes['Value']['BlockPublicAccessConfiguration']['BlockPublicSecurityGroupRules'])


def build_global_accelerator(attributes: dict) -> GlobalAccelerator:
    return GlobalAccelerator(attributes['Account'],
                             attributes['Name'],
                             attributes['AcceleratorArn'])


def build_global_accelerator_listener(attributes: dict) -> GlobalAcceleratorListener:
    return GlobalAcceleratorListener(attributes['Account'],
                                     attributes['ListenerArn'],
                                     urllib.parse.unquote(extract_attribute_from_file_path(attributes['FilePath'], ['AcceleratorArn-']))
                                     .replace('.json', ''))


def build_global_accelerator_endpoint_group(attributes: dict) -> GlobalAcceleratorEndpointGroup:
    endpoint_config = attributes.get('EndpointDescriptions', [{}])
    return GlobalAcceleratorEndpointGroup(attributes['Account'],
                                          urllib.parse.unquote(extract_attribute_from_file_path(attributes['FilePath'], ['ListenerArn-'])),
                                          attributes['EndpointGroupArn'],
                                          endpoint_config[0].get('EndpointId'),
                                          endpoint_config[0].get('ClientIPPreservationEnabled', False),
                                          attributes['EndpointGroupRegion'])


def build_elastic_ip(attributes: dict) -> ElasticIp:
    return ElasticIp(attributes['AllocationId'],
                     attributes.get('PublicIp'),
                     attributes.get('PrivateIpAddress'),
                     attributes['Region'],
                     attributes['Account'])


def build_ec2_instance_type(attributes: dict) -> Ec2InstanceType:
    ebs_info = attributes['EbsInfo']
    return Ec2InstanceType(attributes['InstanceType'],
                           EbsInfo(ebs_info['EbsOptimizedSupport'], ebs_info['EncryptionSupport']))


def build_config_aggregator(attributes: dict) -> ConfigAggregator:
    account_aggregation_used = False
    account_aggregation_all_regions_enabled = None
    organization_aggregation_used = False
    organization_aggregation_all_regions_enabled = None
    if attributes.get('AccountAggregationSources'):
        account_aggregation_used = True
        account_aggregation_all_regions_enabled = attributes['AccountAggregationSources'][0]['AllAwsRegions']
    if attributes.get('OrganizationAggregationSource'):
        organization_aggregation_used = True
        organization_aggregation_all_regions_enabled = attributes['OrganizationAggregationSource']['AllAwsRegions']
    return ConfigAggregator(attributes['Account'],
                            attributes['Region'],
                            attributes['ConfigurationAggregatorName'],
                            attributes['ConfigurationAggregatorArn'],
                            account_aggregation_used,
                            organization_aggregation_used,
                            account_aggregation_all_regions_enabled,
                            organization_aggregation_all_regions_enabled)


def build_global_accelerator_attribute(attributes: dict) -> GlobalAcceleratorAttribute:
    return GlobalAcceleratorAttribute(attributes['Account'],
                                      attributes['Value']['FlowLogsEnabled'],
                                      attributes['Value'].get('FlowLogsS3Bucket'),
                                      attributes['Value'].get('FlowLogsS3Prefix'),
                                      urllib.parse.unquote(extract_attribute_from_file_path(attributes['FilePath'], ['AcceleratorArn-'])))


def build_s3_bucket_logging(attributes: dict) -> S3BucketLogging:
    target_bucket = None
    target_prefix = None
    if attributes['Value'].get('LoggingEnabled'):
        target_bucket = attributes['Value']['LoggingEnabled'].get('TargetBucket')
        target_prefix = attributes['Value']['LoggingEnabled'].get('TargetPrefix')
    return S3BucketLogging(extract_attribute_from_file_path(attributes['FilePath'], ['Bucket-']),
                           target_bucket,
                           target_prefix,
                           attributes['Account'],
                           attributes['Region'])


def build_cfn_resources_info(attributes: dict) -> CloudformationResourceInfo:
    return CloudformationResourceInfo(account=attributes['Account'],
                                      region=attributes['Region'],
                                      stack_id=attributes['StackId'],
                                      stack_name=attributes['StackName'],
                                      logical_resource_id=attributes['LogicalResourceId'],
                                      physical_resource_id=attributes.get('PhysicalResourceId', None),  # Deleted resources not have 'PhysicalResourceId'
                                      resource_type=attributes['ResourceType'],
                                      resource_status=CloudformationResourceStatus(attributes['ResourceStatus']))

def build_fsx_windows_file_system(attributes: dict) -> FsxWindowsFileSystem:
    return FsxWindowsFileSystem(account=attributes['Account'],
                                region=attributes['Region'],
                                fsx_windows_file_system_id=attributes['FileSystemId'],
                                kms_key_id=attributes['KmsKeyId'],
                                arn=attributes['ResourceARN'])
