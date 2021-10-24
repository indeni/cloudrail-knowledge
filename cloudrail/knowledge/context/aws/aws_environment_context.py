import functools
from typing import List, Dict, Optional, Union, Callable, Set

from cloudrail.knowledge.context.aws.resources.ec2.network_acl_association import NetworkAclAssociation
from cloudrail.knowledge.context.aws.resources.ec2.vpc_gateway_attachment import VpcGatewayAttachment
from cloudrail.knowledge.context.aws.resources.ec2.availability_zone import AvailabilityZone
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.account.account import Account
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import ApiGatewayIntegration
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import ApiGatewayMethodSettings
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_stage import ApiGatewayStage
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_domain import RestApiGwDomain
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_mapping import RestApiGwMapping
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_policy import RestApiGwPolicy
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2 import ApiGateway
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2_integration import ApiGatewayV2Integration
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2_vpc_link import ApiGatewayVpcLink
from cloudrail.knowledge.context.aws.resources.athena.athena_database import AthenaDatabase
from cloudrail.knowledge.context.aws.resources.athena.athena_workgroup import AthenaWorkgroup
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_configuration import LaunchConfiguration, AutoScalingGroup
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.resources.aws_client import AwsClient
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.batch.batch_compute_environment import BatchComputeEnvironment
from cloudrail.knowledge.context.aws.resources.cloudformation.cloudformation_resource_info import CloudformationResourceInfo
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_list import CloudFrontDistribution
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
from cloudrail.knowledge.context.aws.resources.docdb.docdb_cluster_parameter_group import DocDbClusterParameterGroup
from cloudrail.knowledge.context.aws.resources.ds.directory_service import DirectoryService
from cloudrail.knowledge.context.aws.resources.dynamodb.dynamodb_table import DynamoDbTable
from cloudrail.knowledge.context.aws.resources.ec2.ec2_image import Ec2Image
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance_type import Ec2InstanceType
from cloudrail.knowledge.context.aws.resources.ec2.elastic_ip import ElasticIp
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.aws.resources.ec2.main_route_table_association import MainRouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.nat_gateways import NatGateways
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_rule import NetworkAclRule
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.peering_connection import PeeringConnection
from cloudrail.knowledge.context.aws.resources.ec2.route import Route
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.route_table_association import RouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRule
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway import TransitGateway
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route import TransitGatewayRoute
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table import TransitGatewayRouteTable
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table_association import TransitGatewayRouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table_propagation import TransitGatewayRouteTablePropagation
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_vpc_attachment import TransitGatewayVpcAttachment
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc, VpcAttribute
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpoint
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint_route_table_association import VpcEndpointRouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ecr.ecr_repository import EcrRepository
from cloudrail.knowledge.context.aws.resources.ecr.ecr_repository_policy import EcrRepositoryPolicy
from cloudrail.knowledge.context.aws.resources.ecs.ecs_cluster import EcsCluster
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.resources.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import EcsTaskDefinition
from cloudrail.knowledge.context.aws.resources.efs.efs_file_system import ElasticFileSystem
from cloudrail.knowledge.context.aws.resources.efs.efs_mount_target import EfsMountTarget
from cloudrail.knowledge.context.aws.resources.efs.efs_policy import EfsPolicy
from cloudrail.knowledge.context.aws.resources.eks.eks_cluster import EksCluster
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_replication_group import ElastiCacheReplicationGroup
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_cluster import ElastiCacheCluster
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_subnet_group import ElastiCacheSubnetGroup
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_attributes import LoadBalancerAttributes
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_listener import LoadBalancerListener
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target import LoadBalancerTarget
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group import LoadBalancerTargetGroup
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group_association import LoadBalancerTargetGroupAssociation
from cloudrail.knowledge.context.aws.resources.emr.emr_cluster import EmrCluster
from cloudrail.knowledge.context.aws.resources.emr.emr_public_access_config import EmrPublicAccessConfiguration
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain
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
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.resources.iam.iam_instance_profile import IamInstanceProfile
from cloudrail.knowledge.context.aws.resources.iam.iam_password_policy import IamPasswordPolicy
from cloudrail.knowledge.context.aws.resources.iam.iam_policy_attachment import IamPolicyAttachment
from cloudrail.knowledge.context.aws.resources.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.resources.iam.iam_user_group_membership import IamUserGroupMembership
from cloudrail.knowledge.context.aws.resources.iam.iam_users_login_profile import IamUsersLoginProfile
from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy, InlinePolicy, ManagedPolicy, Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_group_attachment import PolicyGroupAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_role_attachment import PolicyRoleAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_user_attachment import PolicyUserAttachment
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.iam.role_last_used import RoleLastUsed
from cloudrail.knowledge.context.aws.resources.kinesis.kinesis_firehose_stream import KinesisFirehoseStream
from cloudrail.knowledge.context.aws.resources.kinesis.kinesis_stream import KinesisStream
from cloudrail.knowledge.context.aws.resources.kms.kms_alias import KmsAlias
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_policy import KmsKeyPolicy
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import LambdaAlias
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.mq.mq_broker import MqBroker
from cloudrail.knowledge.context.aws.resources.neptune.neptune_cluster import NeptuneCluster
from cloudrail.knowledge.context.aws.resources.neptune.neptune_instance import NeptuneInstance
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.networking_config.network_resource import NetworkResource
from cloudrail.knowledge.context.aws.resources.prefix_lists import PrefixLists
from cloudrail.knowledge.context.aws.resources.rds.db_subnet_group import DbSubnetGroup
from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_global_cluster import RdsGlobalCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.aws.resources.redshift.redshift_logging import RedshiftLogging
from cloudrail.knowledge.context.aws.resources.redshift.redshift_subnet_group import RedshiftSubnetGroup
from cloudrail.knowledge.context.aws.resources.resourcegroupstaggingapi.resource_tag_mapping_list import ResourceTagMappingList
from cloudrail.knowledge.context.aws.resources.s3.public_access_block_settings import PublicAccessBlockSettings
from cloudrail.knowledge.context.aws.resources.s3.s3_acl import S3ACL
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_access_point import S3BucketAccessPoint
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_encryption import S3BucketEncryption
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_logging import S3BucketLogging
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_object import S3BucketObject
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_regions import S3BucketRegions
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_versioning import S3BucketVersioning
from cloudrail.knowledge.context.aws.resources.s3.s3_access_point_policy import S3AccessPointPolicy
from cloudrail.knowledge.context.aws.resources.s3.s3_policy import S3Policy
from cloudrail.knowledge.context.aws.resources.s3outposts.s3outpost_endpoint import S3OutpostEndpoint
from cloudrail.knowledge.context.aws.resources.sagemaker.sagemaker_endpoint_config import SageMakerEndpointConfig
from cloudrail.knowledge.context.aws.resources.sagemaker.sagemaker_notebook_instance import SageMakerNotebookInstance
from cloudrail.knowledge.context.aws.resources.secretsmanager.secrets_manager_secret import SecretsManagerSecret
from cloudrail.knowledge.context.aws.resources.secretsmanager.secrets_manager_secret_policy import SecretsManagerSecretPolicy
from cloudrail.knowledge.context.aws.resources.sns.sns_topic import SnsTopic
from cloudrail.knowledge.context.aws.resources.sqs.sqs_queue import SqsQueue
from cloudrail.knowledge.context.aws.resources.sqs.sqs_queue_policy import SqsQueuePolicy
from cloudrail.knowledge.context.aws.resources.ssm.ssm_parameter import SsmParameter
from cloudrail.knowledge.context.aws.resources.worklink.worklink_fleet import WorkLinkFleet
from cloudrail.knowledge.context.aws.resources.workspaces.workspace_directory import WorkspaceDirectory
from cloudrail.knowledge.context.aws.resources.workspaces.workspace import Workspace
from cloudrail.knowledge.context.aws.resources.xray.xray_encryption import XrayEncryption
from cloudrail.knowledge.context.managed_resources_summary import ManagedResourcesSummary
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext, CheckovResult, _TMergeAble
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.unknown_block import UnknownBlock
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_policy import LambdaPolicy


class AwsEnvironmentContext(BaseEnvironmentContext):
    def __init__(self,
                 vpcs: AliasesDict[Vpc] = None,
                 subnets: AliasesDict[Subnet] = None,
                 transit_gateways: List[TransitGateway] = None,
                 network_interfaces: AliasesDict[NetworkInterface] = None,
                 ec2s: List[Ec2Instance] = None,
                 ecs_cluster_list: List[EcsCluster] = None,
                 load_balancers: List[LoadBalancer] = None,
                 load_balancer_listeners: List[LoadBalancerListener] = None,
                 s3_buckets: AliasesDict[S3Bucket] = None,
                 s3_bucket_objects: List[S3BucketObject] = None,
                 roles: List[Role] = None,
                 users: List[IamUser] = None,
                 groups: List[IamGroup] = None,
                 users_login_profile: List[IamUsersLoginProfile] = None,
                 redshift_clusters: List[RedshiftCluster] = None,
                 rds_instances: List[RdsInstance] = None,
                 rds_clusters: List[RdsCluster] = None,
                 rds_global_clusters: List[RdsGlobalCluster] = None,
                 elastic_search_domains: List[ElasticSearchDomain] = None,
                 eks_clusters: List[EksCluster] = None,
                 cloudfront_distribution_list: List[CloudFrontDistribution] = None,
                 elastic_ips: List[ElasticIp] = None,
                 launch_configurations: List[LaunchConfiguration] = None,
                 launch_templates: List[LaunchTemplate] = None,
                 prefix_lists: List[PrefixLists] = None,
                 rest_api_gw: List[RestApiGw] = None,
                 api_gateway_methods: List[ApiGatewayMethod] = None,
                 athena_workgroups: List[AthenaWorkgroup] = None,
                 dynamodb_table_list: List[DynamoDbTable] = None,
                 dax_cluster: List[DaxCluster] = None,
                 docdb_cluster: List[DocumentDbCluster] = None,
                 docdb_cluster_parameter_groups: List[DocDbClusterParameterGroup] = None,
                 cloud_watch_log_groups: List[CloudWatchLogGroup] = None,
                 cloudtrail: List[CloudTrail] = None,
                 codebuild_projects: List[CodeBuildProject] = None,
                 codebuild_report_groups: List[CodeBuildReportGroup] = None,
                 sqs_queues: List[SqsQueue] = None,
                 accounts: AliasesDict[Account] = None,
                 elasti_cache_replication_groups: List[ElastiCacheReplicationGroup] = None,
                 neptune_clusters: List[NeptuneCluster] = None,
                 sns_topics: List[SnsTopic] = None,
                 ecr_repositories: List[EcrRepository] = None,
                 kms_keys: List[KmsKey] = None,
                 cloudwatch_logs_destinations: List[CloudWatchLogsDestination] = None,
                 efs_file_systems: List[ElasticFileSystem] = None,
                 glacier_vaults: List[GlacierVault] = None,
                 secrets_manager_secrets: List[SecretsManagerSecret] = None,
                 glue_data_catalog_policy: List[GlueDataCatalogPolicy] = None,
                 kinesis_streams: List[KinesisStream] = None,
                 kinesis_firehose_streams: List[KinesisFirehoseStream] = None,
                 xray_encryption_configurations: List[XrayEncryption] = None,
                 workspaces: List[Workspace] = None,
                 kms_aliases: List[KmsAlias] = None,
                 glue_data_catalog_crawlers: List[GlueCrawler] = None,
                 glue_data_catalog_tables: List[GlueDataCatalogTable] = None,
                 iam_account_pass_policies: List[IamPasswordPolicy] = None,
                 checkov_results: Dict[str, List[CheckovResult]] = None,
                 vpc_endpoints: List[VpcEndpoint] = None,
                 lambda_function_list: List[LambdaFunction] = None,
                 neptune_cluster_instances: List[NeptuneInstance] = None,
                 ecs_task_definitions: List[EcsTaskDefinition] = None,
                 ssm_parameters: List[SsmParameter] = None,
                 sagemaker_endpoint_config_list: List[SageMakerEndpointConfig] = None,
                 sagemaker_notebook_instances: List[SageMakerNotebookInstance] = None,
                 security_groups: AliasesDict[SecurityGroup] = None,
                 peering_connections: List[PeeringConnection] = None,
                 dms_replication_instances: List[DmsReplicationInstance] = None,
                 vpcs_attributes: List[VpcAttribute] = None,
                 internet_gateways: List[InternetGateway] = None,
                 vpc_gateway_attachment: AliasesDict[VpcGatewayAttachment] = None,
                 ecs_service_list: List[EcsService] = None,
                 cloud_watch_event_target_list: List[CloudWatchEventTarget] = None,
                 ecs_targets_list: List[EcsTarget] = None,
                 security_group_rules: List[SecurityGroupRule] = None,
                 route_tables: AliasesDict[RouteTable] = None,
                 routes: List[Route] = None,
                 route_table_associations: List[RouteTableAssociation] = None,
                 main_route_table_associations: List[MainRouteTableAssociation] = None,
                 network_acls: AliasesDict[NetworkAcl] = None,
                 network_acl_rules: List[NetworkAclRule] = None,
                 network_acl_associations: AliasesDict[NetworkAclAssociation] = None,
                 load_balancer_target_groups: List[LoadBalancerTargetGroup] = None,
                 load_balancer_target_group_associations: List[LoadBalancerTargetGroupAssociation] = None,
                 load_balancer_targets: List[LoadBalancerTarget] = None,
                 auto_scaling_groups: List[AutoScalingGroup] = None,
                 role_inline_policies: List[InlinePolicy] = None,
                 user_inline_policies: List[InlinePolicy] = None,
                 policy_user_attachments: List[PolicyUserAttachment] = None,
                 iam_user_group_membership: List[IamUserGroupMembership] = None,
                 group_inline_policies: List[InlinePolicy] = None,
                 policy_group_attachments: List[PolicyGroupAttachment] = None,
                 iam_group_membership: List[IamGroupMembership] = None,
                 policies: List[ManagedPolicy] = None,
                 policy_role_attachments: List[PolicyRoleAttachment] = None,
                 s3_bucket_regions: List[S3BucketRegions] = None,
                 s3_bucket_acls: List[S3ACL] = None,
                 s3_bucket_policies: List[S3Policy] = None,
                 lambda_policies: List[LambdaPolicy] = None,
                 s3_bucket_access_points: List[S3BucketAccessPoint] = None,
                 s3_bucket_access_points_policies: List[S3AccessPointPolicy] = None,
                 s3_public_access_block_settings_list: List[PublicAccessBlockSettings] = None,
                 transit_gateway_routes: List[TransitGatewayRoute] = None,
                 transit_gateway_attachments: List[TransitGatewayVpcAttachment] = None,
                 transit_gateway_route_tables: List[TransitGatewayRouteTable] = None,
                 transit_gateway_route_table_associations: List[TransitGatewayRouteTableAssociation] = None,
                 transit_gateway_route_table_propagations: List[TransitGatewayRouteTablePropagation] = None,
                 redshift_subnet_groups: List[RedshiftSubnetGroup] = None,
                 db_subnet_groups: List[DbSubnetGroup] = None,
                 iam_instance_profiles: List[IamInstanceProfile] = None,
                 origin_access_identity_list: List[OriginAccessIdentity] = None,
                 unknown_blocks: List[UnknownBlock] = None,
                 api_gateway_method_settings: List[ApiGatewayMethodSettings] = None,
                 nat_gateway_list: List[NatGateways] = None,
                 s3_bucket_encryption: List[S3BucketEncryption] = None,
                 s3_bucket_versioning: List[S3BucketVersioning] = None,
                 ec2_images: List[Ec2Image] = None,
                 vpc_endpoint_route_table_associations: List[VpcEndpointRouteTableAssociation] = None,
                 sqs_queues_policy: List[SqsQueuePolicy] = None,
                 ecr_repositories_policy: List[EcrRepositoryPolicy] = None,
                 kms_keys_policies: List[KmsKeyPolicy] = None,
                 rest_api_gw_policies: List[RestApiGwPolicy] = None,
                 cloudwatch_logs_destination_policies: List[CloudWatchLogsDestinationPolicy] = None,
                 elastic_search_domains_policies: List[ElasticSearchDomainPolicy] = None,
                 lambda_aliases: AliasesDict[LambdaAlias] = None,
                 efs_file_systems_policies: List[EfsPolicy] = None,
                 glacier_vaults_policies: List[GlacierVaultPolicy] = None,
                 secrets_manager_secrets_policies: List[SecretsManagerSecretPolicy] = None,
                 rest_api_gw_mappings: List[RestApiGwMapping] = None,
                 rest_api_gw_domains: List[RestApiGwDomain] = None,
                 api_gateway_integrations: List[ApiGatewayIntegration] = None,
                 iam_policy_attachments: List[IamPolicyAttachment] = None,
                 resources_tagging_list: List[ResourceTagMappingList] = None,
                 assume_role_policies: List[AssumeRolePolicy] = None,
                 dms_replication_instance_subnet_groups: List[DmsReplicationInstanceSubnetGroup] = None,
                 invalidated_resources: Set[Mergeable] = None,
                 managed_resources_summary: ManagedResourcesSummary = None,
                 elasticache_clusters: List[ElastiCacheCluster] = None,
                 elasticache_subnet_groups: List[ElastiCacheSubnetGroup] = None,
                 efs_mount_targets: List[EfsMountTarget] = None,
                 workspaces_directories: List[WorkspaceDirectory] = None,
                 cloud_directories: List[DirectoryService] = None,
                 roles_last_used: List[RoleLastUsed] = None,
                 batch_compute_environments: List[BatchComputeEnvironment] = None,
                 mq_brokers: List[MqBroker] = None,
                 api_gateways_v2: List[ApiGateway] = None,
                 api_gateway_v2_integrations: List[ApiGatewayV2Integration] = None,
                 api_gateway_v2_vpc_links: List[ApiGatewayVpcLink] = None,
                 emr_clusters: List[EmrCluster] = None,
                 emr_public_access_configurations: List[EmrPublicAccessConfiguration] = None,
                 global_accelerators: List[GlobalAccelerator] = None,
                 global_accelerator_listeners: List[GlobalAcceleratorListener] = None,
                 global_accelerator_endpoint_groups: List[GlobalAcceleratorEndpointGroup] = None,
                 cloudhsm_v2_clusters: List[CloudHsmV2Cluster] = None,
                 cloudhsm_list: List[CloudHsmV2Hsm] = None,
                 s3outpost_endpoints: List[S3OutpostEndpoint] = None,
                 worklink_fleets: List[WorkLinkFleet] = None,
                 glue_connections: List[GlueConnection] = None,
                 load_balancers_attributes: List[LoadBalancerAttributes] = None,
                 ec2_instance_types: List[Ec2InstanceType] = None,
                 aws_config_aggregators: List[ConfigAggregator] = None,
                 rest_api_stages: List[ApiGatewayStage] = None,
                 cloudfront_log_settings: List[CloudfrontDistributionLogging] = None,
                 global_accelerator_attributes: List[GlobalAcceleratorAttribute] = None,
                 redshift_logs: List[RedshiftLogging] = None,
                 s3_bucket_logs: List[S3BucketLogging] = None,
                 athena_databases: List[AthenaDatabase] = None,
                 cfn_resources_info: List[CloudformationResourceInfo] = None,
                 availability_zones: AliasesDict[AvailabilityZone] = None,
                 fsx_windows_file_systems: AliasesDict[FsxWindowsFileSystem] = None):
        BaseEnvironmentContext.__init__(self, invalidated_resources=invalidated_resources, unknown_blocks=unknown_blocks,
                                        managed_resources_summary=managed_resources_summary)
        self.athena_databases = athena_databases or []
        self.s3_bucket_logs = s3_bucket_logs or []
        self.redshift_logs = redshift_logs or []
        self.global_accelerator_attributes = global_accelerator_attributes or []
        self.cloudfront_log_settings = cloudfront_log_settings or []
        self.rest_api_stages = rest_api_stages or []
        self.aws_config_aggregators = aws_config_aggregators or []
        self.ec2_instance_types = ec2_instance_types or []
        self.load_balancers_attributes = load_balancers_attributes or []
        self.glue_connections = glue_connections or []
        self.worklink_fleets = worklink_fleets or []
        self.s3outpost_endpoints = s3outpost_endpoints or []
        self.cloudhsm_list = cloudhsm_list or []
        self.cloudhsm_v2_clusters = cloudhsm_v2_clusters or []
        self.global_accelerator_endpoint_groups = global_accelerator_endpoint_groups or []
        self.global_accelerator_listeners = global_accelerator_listeners or []
        self.global_accelerators = global_accelerators or []
        self.emr_public_access_configurations = emr_public_access_configurations or []
        self.emr_clusters = emr_clusters or []
        self.api_gateway_v2_vpc_links = api_gateway_v2_vpc_links or []
        self.api_gateway_v2_integrations = api_gateway_v2_integrations or []
        self.api_gateways_v2 = api_gateways_v2 or []
        self.mq_brokers = mq_brokers or []
        self.batch_compute_environments = batch_compute_environments or []
        self.roles_last_used = roles_last_used or []
        self.cloud_directories = cloud_directories or []
        self.workspaces_directories = workspaces_directories or []
        self.efs_mount_targets = efs_mount_targets or []
        self.elasticache_subnet_groups = elasticache_subnet_groups or []
        self.elasticache_clusters = elasticache_clusters or []
        self.vpcs = vpcs or AliasesDict()
        self.subnets = subnets or AliasesDict()
        self.transit_gateways = transit_gateways or []
        self.network_interfaces = network_interfaces or AliasesDict()
        self.ec2s = ec2s or []
        self.ecs_cluster_list = ecs_cluster_list or []
        self.load_balancers = load_balancers or []
        self.load_balancer_listeners = load_balancer_listeners or []
        self.s3_buckets = s3_buckets or AliasesDict()
        self.s3_bucket_objects = s3_bucket_objects or []
        self.lambda_policies = lambda_policies or []
        self.roles = roles or []
        self.users = users or []
        self.groups = groups or []
        self.users_login_profile = users_login_profile or []
        self.redshift_clusters = redshift_clusters or []
        self.rds_instances = rds_instances or []
        self.rds_clusters = rds_clusters or []
        self.rds_global_clusters = rds_global_clusters or []
        self.elastic_search_domains = elastic_search_domains or []
        self.eks_clusters = eks_clusters or []
        self.cloudfront_distribution_list = cloudfront_distribution_list or []
        self.elastic_ips = elastic_ips or []
        self.launch_configurations = launch_configurations or []
        self.launch_templates = launch_templates or []
        self.prefix_lists = prefix_lists or []
        self.rest_api_gw = rest_api_gw or []
        self.api_gateway_methods = api_gateway_methods or []
        self.athena_workgroups = athena_workgroups or []
        self.dynamodb_table_list = dynamodb_table_list or []
        self.dax_cluster = dax_cluster or []
        self.docdb_cluster = docdb_cluster or []
        self.docdb_cluster_parameter_groups = docdb_cluster_parameter_groups or []
        self.cloud_watch_log_groups = cloud_watch_log_groups or []
        self.cloudtrail = cloudtrail or []
        self.codebuild_projects = codebuild_projects or []
        self.codebuild_report_groups = codebuild_report_groups or []
        self.sqs_queues = sqs_queues or []
        self.accounts = accounts or AliasesDict()
        self.elasti_cache_replication_groups = elasti_cache_replication_groups or []
        self.neptune_clusters = neptune_clusters or []
        self.sns_topics = sns_topics or []
        self.ecr_repositories = ecr_repositories or []
        self.kms_keys = kms_keys or []
        self.cloudwatch_logs_destinations = cloudwatch_logs_destinations or []
        self.efs_file_systems = efs_file_systems or []
        self.glacier_vaults = glacier_vaults or []
        self.secrets_manager_secrets = secrets_manager_secrets or []
        self.glue_data_catalog_policy = glue_data_catalog_policy or []
        self.kinesis_streams = kinesis_streams or []
        self.kinesis_firehose_streams = kinesis_firehose_streams or []
        self.xray_encryption_configurations = xray_encryption_configurations or []
        self.workspaces = workspaces or []
        self.kms_aliases = kms_aliases or []
        self.glue_data_catalog_crawlers = glue_data_catalog_crawlers or []
        self.glue_data_catalog_tables = glue_data_catalog_tables or []
        self.iam_account_pass_policies = iam_account_pass_policies or []
        self.checkov_results = checkov_results or {}
        self.vpc_endpoints = vpc_endpoints or []
        self.lambda_function_list = lambda_function_list or []
        self.neptune_cluster_instances = neptune_cluster_instances or []
        self.ecs_task_definitions = ecs_task_definitions or []
        self.ssm_parameters = ssm_parameters or []
        self.sagemaker_endpoint_config_list = sagemaker_endpoint_config_list or []
        self.sagemaker_notebook_instances = sagemaker_notebook_instances or []
        self.security_groups = security_groups or AliasesDict()
        self.peering_connections = peering_connections or []
        self.dms_replication_instances = dms_replication_instances or []
        self.vpcs_attributes = vpcs_attributes or []
        self.internet_gateways = internet_gateways or []
        self.vpc_gateway_attachment: AliasesDict[VpcGatewayAttachment] = vpc_gateway_attachment or AliasesDict()
        self.ecs_service_list = ecs_service_list or []
        self.cloud_watch_event_target_list = cloud_watch_event_target_list or []
        self.ecs_targets_list = ecs_targets_list or []
        self.security_group_rules = security_group_rules or []
        self.route_tables = route_tables or AliasesDict()
        self.routes = routes or []
        self.route_table_associations = route_table_associations or []
        self.main_route_table_associations = main_route_table_associations or []
        self.network_acls = network_acls or AliasesDict()
        self.network_acl_rules = network_acl_rules or []
        self.network_acl_associations: AliasesDict[NetworkAclAssociation] = network_acl_associations or AliasesDict()
        self.load_balancer_target_groups = load_balancer_target_groups or []
        self.load_balancer_target_group_associations = load_balancer_target_group_associations or []
        self.load_balancer_targets = load_balancer_targets or []
        self.auto_scaling_groups = auto_scaling_groups or []
        self.role_inline_policies = role_inline_policies or []
        self.user_inline_policies = user_inline_policies or []
        self.policy_user_attachments = policy_user_attachments or []
        self.iam_user_group_membership = iam_user_group_membership or []
        self.group_inline_policies = group_inline_policies or []
        self.policy_group_attachments = policy_group_attachments or []
        self.iam_group_membership = iam_group_membership or []
        self.policies = policies or []
        self.policy_role_attachments = policy_role_attachments or []
        self.s3_bucket_regions = s3_bucket_regions or []
        self.s3_bucket_acls = s3_bucket_acls or []
        self.s3_bucket_policies = s3_bucket_policies or []
        self.s3_bucket_access_points = s3_bucket_access_points or []
        self.s3_bucket_access_points_policies = s3_bucket_access_points_policies or []
        self.s3_public_access_block_settings_list = s3_public_access_block_settings_list or []
        self.transit_gateway_routes = transit_gateway_routes or []
        self.transit_gateway_attachments = transit_gateway_attachments or []
        self.transit_gateway_route_tables = transit_gateway_route_tables or []
        self.transit_gateway_route_table_associations = transit_gateway_route_table_associations or []
        self.transit_gateway_route_table_propagations = transit_gateway_route_table_propagations or []
        self.redshift_subnet_groups = redshift_subnet_groups or []
        self.db_subnet_groups = db_subnet_groups or []
        self.iam_instance_profiles = iam_instance_profiles or []
        self.origin_access_identity_list = origin_access_identity_list or []
        self.unknown_blocks = unknown_blocks or []
        self.api_gateway_method_settings = api_gateway_method_settings or []
        self.nat_gateway_list = nat_gateway_list or []
        self.s3_bucket_encryption = s3_bucket_encryption or []
        self.s3_bucket_versioning = s3_bucket_versioning or []
        self.ec2_images = ec2_images or []
        self.vpc_endpoint_route_table_associations = vpc_endpoint_route_table_associations or []
        self.sqs_queues_policy = sqs_queues_policy or []
        self.ecr_repositories_policy = ecr_repositories_policy or []
        self.kms_keys_policies = kms_keys_policies or []
        self.rest_api_gw_policies = rest_api_gw_policies or []
        self.cloudwatch_logs_destination_policies = cloudwatch_logs_destination_policies or []
        self.elastic_search_domains_policies = elastic_search_domains_policies or []
        self.lambda_aliases = lambda_aliases or AliasesDict()
        self.efs_file_systems_policies = efs_file_systems_policies or []
        self.glacier_vaults_policies = glacier_vaults_policies or []
        self.secrets_manager_secrets_policies = secrets_manager_secrets_policies or []
        self.rest_api_gw_mappings = rest_api_gw_mappings or []
        self.rest_api_gw_domains = rest_api_gw_domains or []
        self.api_gateway_integrations = api_gateway_integrations or []
        self.iam_policy_attachments = iam_policy_attachments or []
        self.resources_tagging_list = resources_tagging_list or []
        self.assume_role_policies = assume_role_policies or []
        self.dms_replication_instance_subnet_groups = dms_replication_instance_subnet_groups or []
        self.invalidated_resources = invalidated_resources or set()
        self.cfn_resources_info: List[CloudformationResourceInfo] = cfn_resources_info or []
        self.availability_zones: AliasesDict[AvailabilityZone] = availability_zones or AliasesDict()
        self.fsx_windows_file_systems: AliasesDict[FsxWindowsFileSystem] = fsx_windows_file_systems or AliasesDict()

    @functools.lru_cache(maxsize=None)
    def get_used_network_interfaces(self) -> AliasesDict[NetworkInterface]:
        return AliasesDict(*[eni for eni in self.network_interfaces if eni.owner])

    @functools.lru_cache(maxsize=None)
    def get_all_nodes_resources(self) -> Set[NetworkResource]:
        return {instance.network_resource for instance in self.get_all_network_entities()}

    @functools.lru_cache(maxsize=None)
    def get_all_network_entities(self) -> Set[NetworkEntity]:
        condition: Callable = lambda resource: isinstance(resource, NetworkEntity)
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_all_aws_clients(self) -> Set[AwsClient]:
        condition: Callable = lambda resource: isinstance(resource, AwsClient)
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_iac_managed_policies(self) -> Set[Policy]:
        condition: Callable = lambda resource: isinstance(resource, Policy) and resource.is_managed_by_iac
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_all_network_entities_aws_clients(self) -> Set[Union[NetworkEntity, AwsClient]]:
        condition: Callable = lambda resource: isinstance(resource, AwsClient) and isinstance(resource, NetworkEntity)
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_all_iam_entities(self) -> List[IamIdentity]:
        return self.roles + self.users + self.groups

    @functools.lru_cache(maxsize=None)
    def get_all_non_iac_managed_resources(self) -> Set[_TMergeAble]:
        condition: Callable = lambda resource: isinstance(resource, AwsResource) and not resource.is_managed_by_iac
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_all_taggable_resources(self) -> Set[_TMergeAble]:
        condition: Callable = lambda aws_resource: aws_resource.is_tagable
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_all_ec2_instance_types_with_default_ebs_optimization(self) -> Optional[Set[Ec2InstanceType]]:
        if self.accounts:
            condition: Callable = lambda resource: isinstance(resource, Ec2InstanceType) and resource.ebs_info.ebs_optimized_support == 'default'
            return self.get_all_mergeable_resources(condition)
        else:
            return []
