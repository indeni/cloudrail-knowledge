import functools
from dataclasses import dataclass
from typing import List, Dict, Union, TypeVar, Callable, Set
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.account.account import Account
from cloudrail.knowledge.context.aws.apigateway.api_gateway_integration import ApiGatewayIntegration
from cloudrail.knowledge.context.aws.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.apigateway.api_gateway_method_settings import ApiGatewayMethodSettings
from cloudrail.knowledge.context.aws.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.aws.apigateway.rest_api_gw_domain import RestApiGwDomain
from cloudrail.knowledge.context.aws.apigateway.rest_api_gw_mapping import RestApiGwMapping
from cloudrail.knowledge.context.aws.apigateway.rest_api_gw_policy import RestApiGwPolicy
from cloudrail.knowledge.context.aws.athena.athena_workgroup import AthenaWorkgroup
from cloudrail.knowledge.context.aws.autoscaling.launch_configuration import LaunchConfiguration, AutoScalingGroup
from cloudrail.knowledge.context.aws.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.aws_client import AwsClient
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.cloudfront.cloud_front_distribution_list import CloudFrontDistribution
from cloudrail.knowledge.context.aws.cloudfront.origin_access_identity import OriginAccessIdentity
from cloudrail.knowledge.context.aws.cloudtrail.cloudtrail import CloudTrail
from cloudrail.knowledge.context.aws.cloudwatch.cloud_watch_event_target import CloudWatchEventTarget
from cloudrail.knowledge.context.aws.cloudwatch.cloud_watch_log_group import CloudWatchLogGroup
from cloudrail.knowledge.context.aws.cloudwatch.cloudwatch_logs_destination import CloudWatchLogsDestination
from cloudrail.knowledge.context.aws.cloudwatch.cloudwatch_logs_destination_policy import CloudWatchLogsDestinationPolicy
from cloudrail.knowledge.context.aws.codebuild.codebuild_project import CodeBuildProject
from cloudrail.knowledge.context.aws.codebuild.codebuild_report_group import CodeBuildReportGroup
from cloudrail.knowledge.context.aws.dax.dax_cluster import DaxCluster
from cloudrail.knowledge.context.aws.dms.dms_replication_instance import DmsReplicationInstance
from cloudrail.knowledge.context.aws.dms.dms_replication_instance_subnet_group import DmsReplicationInstanceSubnetGroup
from cloudrail.knowledge.context.aws.docdb.docdb_cluster import DocumentDbCluster
from cloudrail.knowledge.context.aws.docdb.docdb_cluster_parameter_group import DocDbClusterParameterGroup
from cloudrail.knowledge.context.aws.ds.directory_service import DirectoryService
from cloudrail.knowledge.context.aws.dynamodb.dynamodb_table import DynamoDbTable
from cloudrail.knowledge.context.aws.ec2.ec2_image import Ec2Image
from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.ec2.elastic_ip import ElasticIp
from cloudrail.knowledge.context.aws.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.aws.ec2.main_route_table_association import MainRouteTableAssociation
from cloudrail.knowledge.context.aws.ec2.nat_gateways import NatGateways
from cloudrail.knowledge.context.aws.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.ec2.network_acl_rule import NetworkAclRule
from cloudrail.knowledge.context.aws.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.ec2.peering_connection import PeeringConnection
from cloudrail.knowledge.context.aws.ec2.route import Route
from cloudrail.knowledge.context.aws.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.ec2.route_table_association import RouteTableAssociation
from cloudrail.knowledge.context.aws.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.ec2.security_group_rule import SecurityGroupRule
from cloudrail.knowledge.context.aws.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.ec2.transit_gateway import TransitGateway
from cloudrail.knowledge.context.aws.ec2.transit_gateway_route import TransitGatewayRoute
from cloudrail.knowledge.context.aws.ec2.transit_gateway_route_table import TransitGatewayRouteTable
from cloudrail.knowledge.context.aws.ec2.transit_gateway_route_table_association import TransitGatewayRouteTableAssociation
from cloudrail.knowledge.context.aws.ec2.transit_gateway_route_table_propagation import TransitGatewayRouteTablePropagation
from cloudrail.knowledge.context.aws.ec2.transit_gateway_vpc_attachment import TransitGatewayVpcAttachment
from cloudrail.knowledge.context.aws.ec2.vpc import Vpc, VpcAttribute
from cloudrail.knowledge.context.aws.ec2.vpc_endpoint import VpcEndpoint
from cloudrail.knowledge.context.aws.ec2.vpc_endpoint_route_table_association import VpcEndpointRouteTableAssociation
from cloudrail.knowledge.context.aws.ecr.ecr_repository import EcrRepository
from cloudrail.knowledge.context.aws.ecr.ecr_repository_policy import EcrRepositoryPolicy
from cloudrail.knowledge.context.aws.ecs.ecs_cluster import EcsCluster
from cloudrail.knowledge.context.aws.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.ecs.ecs_task_definition import EcsTaskDefinition
from cloudrail.knowledge.context.aws.efs.efs_file_system import ElasticFileSystem
from cloudrail.knowledge.context.aws.efs.efs_mount_target import EfsMountTarget
from cloudrail.knowledge.context.aws.efs.efs_policy import EfsPolicy
from cloudrail.knowledge.context.aws.eks.eks_cluster import EksCluster
from cloudrail.knowledge.context.aws.elasticache.elasticache_replication_group import ElastiCacheReplicationGroup
from cloudrail.knowledge.context.aws.elasticache.elasticache_cluster import ElastiCacheCluster
from cloudrail.knowledge.context.aws.elasticache.elasticache_subnet_group import ElastiCacheSubnetGroup
from cloudrail.knowledge.context.aws.elb.load_balancer import LoadBalancer
from cloudrail.knowledge.context.aws.elb.load_balancer_listener import LoadBalancerListener
from cloudrail.knowledge.context.aws.elb.load_balancer_target import LoadBalancerTarget
from cloudrail.knowledge.context.aws.elb.load_balancer_target_group import LoadBalancerTargetGroup
from cloudrail.knowledge.context.aws.elb.load_balancer_target_group_association import LoadBalancerTargetGroupAssociation
from cloudrail.knowledge.context.aws.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.context.aws.es.elastic_search_domain_policy import ElasticSearchDomainPolicy
from cloudrail.knowledge.context.aws.glacier.glacier_vault import GlacierVault
from cloudrail.knowledge.context.aws.glacier.glacier_vault_policy import GlacierVaultPolicy
from cloudrail.knowledge.context.aws.glue.glue_data_catalog_crawler import GlueCrawler
from cloudrail.knowledge.context.aws.glue.glue_data_catalog_policy import GlueDataCatalogPolicy
from cloudrail.knowledge.context.aws.glue.glue_data_catalog_table import GlueDataCatalogTable
from cloudrail.knowledge.context.aws.iam.iam_group import IamGroup
from cloudrail.knowledge.context.aws.iam.iam_group_membership import IamGroupMembership
from cloudrail.knowledge.context.aws.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.iam.iam_instance_profile import IamInstanceProfile
from cloudrail.knowledge.context.aws.iam.iam_password_policy import IamPasswordPolicy
from cloudrail.knowledge.context.aws.iam.iam_policy_attachment import IamPolicyAttachment
from cloudrail.knowledge.context.aws.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.iam.iam_user_group_membership import IamUserGroupMembership
from cloudrail.knowledge.context.aws.iam.iam_users_login_profile import IamUsersLoginProfile
from cloudrail.knowledge.context.aws.iam.policy import AssumeRolePolicy, InlinePolicy, ManagedPolicy, S3Policy, S3AccessPointPolicy, Policy
from cloudrail.knowledge.context.aws.iam.policy_group_attachment import PolicyGroupAttachment
from cloudrail.knowledge.context.aws.iam.policy_role_attachment import PolicyRoleAttachment
from cloudrail.knowledge.context.aws.iam.policy_user_attachment import PolicyUserAttachment
from cloudrail.knowledge.context.aws.iam.role import Role
from cloudrail.knowledge.context.aws.iam.role_last_used import RoleLastUsed
from cloudrail.knowledge.context.aws.kinesis.kinesis_firehose_stream import KinesisFirehoseStream
from cloudrail.knowledge.context.aws.kinesis.kinesis_stream import KinesisStream
from cloudrail.knowledge.context.aws.kms.kms_alias import KmsAlias
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_policy import KmsKeyPolicy
from cloudrail.knowledge.context.aws.lambda_.lambda_alias import LambdaAlias
from cloudrail.knowledge.context.aws.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.lambda_.lambda_policy_statements import LambdaPolicyStatements
from cloudrail.knowledge.context.aws.neptune.neptune_cluster import NeptuneCluster
from cloudrail.knowledge.context.aws.neptune.neptune_instance import NeptuneInstance
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.networking_config.network_resource import NetworkResource
from cloudrail.knowledge.context.aws.prefix_lists import PrefixLists
from cloudrail.knowledge.context.aws.rds.db_subnet_group import DbSubnetGroup
from cloudrail.knowledge.context.aws.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.rds.rds_global_cluster import RdsGlobalCluster
from cloudrail.knowledge.context.aws.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.aws.redshift.redshift_subnet_group import RedshiftSubnetGroup
from cloudrail.knowledge.context.aws.resourcegroupstaggingapi.resource_tag_mapping_list import ResourceTagMappingList
from cloudrail.knowledge.context.aws.s3.public_access_block_settings import PublicAccessBlockSettings
from cloudrail.knowledge.context.aws.s3.s3_acl import S3ACL
from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.s3.s3_bucket_access_point import S3BucketAccessPoint
from cloudrail.knowledge.context.aws.s3.s3_bucket_encryption import S3BucketEncryption
from cloudrail.knowledge.context.aws.s3.s3_bucket_object import S3BucketObject
from cloudrail.knowledge.context.aws.s3.s3_bucket_regions import S3BucketRegions
from cloudrail.knowledge.context.aws.s3.s3_bucket_versioning import S3BucketVersioning
from cloudrail.knowledge.context.aws.sagemaker.sagemaker_endpoint_config import SageMakerEndpointConfig
from cloudrail.knowledge.context.aws.sagemaker.sagemaker_notebook_instance import SageMakerNotebookInstance
from cloudrail.knowledge.context.aws.secretsmanager.secrets_manager_secret import SecretsManagerSecret
from cloudrail.knowledge.context.aws.secretsmanager.secrets_manager_secret_policy import SecretsManagerSecretPolicy
from cloudrail.knowledge.context.aws.sns.sns_topic import SnsTopic
from cloudrail.knowledge.context.aws.sqs.sqs_queue import SqsQueue
from cloudrail.knowledge.context.aws.sqs.sqs_queue_policy import SqsQueuePolicy
from cloudrail.knowledge.context.aws.ssm.ssm_parameter import SsmParameter
from cloudrail.knowledge.context.aws.workspaces.workspace_directory import WorkspaceDirectory
from cloudrail.knowledge.context.aws.workspaces.workspaces import Workspace
from cloudrail.knowledge.context.aws.xray.xray_encryption import XrayEncryption
from cloudrail.knowledge.context.managed_resources_summary import ManagedResourcesSummary
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.unknown_block import UnknownBlock

_TMergeAble = TypeVar('_TMergeAble', bound=Mergeable)


@dataclass
class CheckovResult:
    check_id: str
    file_path: str
    resource: str
    start_line: int
    end_line: int

    @staticmethod
    def from_dict(dic: dict):
        return CheckovResult(dic['check_id'], dic['file_path'], dic['resource'], dic['start_line'], dic['end_line'])


class EnvironmentContext(BaseEnvironmentContext): # todo - need to remove under aws folder
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
                 accounts: List[Account] = None,
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
                 ecs_service_list: List[EcsService] = None,
                 cloud_watch_event_target_list: List[CloudWatchEventTarget] = None,
                 ecs_targets_list: List[EcsTarget] = None,
                 security_group_rules: List[SecurityGroupRule] = None,
                 route_tables: AliasesDict[RouteTable] = None,
                 routes: List[Route] = None,
                 route_table_associations: List[RouteTableAssociation] = None,
                 main_route_table_associations: List[MainRouteTableAssociation] = None,
                 network_acls: List[NetworkAcl] = None,
                 network_acl_rules: List[NetworkAclRule] = None,
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
                 lambda_policy_statements: List[LambdaPolicyStatements] = None,
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
                 roles_last_used: List[RoleLastUsed] = None):
        BaseEnvironmentContext.__init__(self, invalidated_resources=invalidated_resources, unknown_blocks=unknown_blocks,
                                        managed_resources_summary=managed_resources_summary)
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
        self.accounts = accounts or []
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
        self.ecs_service_list = ecs_service_list or []
        self.cloud_watch_event_target_list = cloud_watch_event_target_list or []
        self.ecs_targets_list = ecs_targets_list or []
        self.security_group_rules = security_group_rules or []
        self.route_tables = route_tables or AliasesDict()
        self.routes = routes or []
        self.route_table_associations = route_table_associations or []
        self.main_route_table_associations = main_route_table_associations or []
        self.network_acls = network_acls or []
        self.network_acl_rules = network_acl_rules or []
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
        self.lambda_policy_statements = lambda_policy_statements or []
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

    @functools.lru_cache(maxsize=None)
    def get_used_network_interfaces(self) -> AliasesDict[NetworkInterface]:
        return AliasesDict(*[eni for eni in self.network_interfaces if eni.owner])

    @functools.lru_cache(maxsize=None)
    def get_all_nodes_resources(self) -> List[NetworkResource]:
        return [instance.network_resource for instance in self.get_all_network_entities()]

    @functools.lru_cache(maxsize=None)
    def get_all_network_entities(self) -> List[NetworkEntity]:
        condition: Callable = lambda resource: isinstance(resource, NetworkEntity)
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_all_aws_clients(self) -> List[AwsClient]:
        condition: Callable = lambda resource: isinstance(resource, AwsClient)
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_iac_managed_policies(self) -> List[Policy]:
        condition: Callable = lambda resource: isinstance(resource, Policy) and resource.is_managed_by_iac
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_all_network_entities_aws_clients(self) -> List[Union[NetworkEntity, AwsClient]]:
        condition: Callable = lambda resource: isinstance(resource, AwsClient) and isinstance(resource, NetworkEntity)
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_all_iam_entities(self) -> List[IamIdentity]:
        return self.roles + self.users + self.groups

    @functools.lru_cache(maxsize=None)
    def get_all_non_iac_managed_resources(self) -> List[_TMergeAble]:
        condition: Callable = lambda resource: isinstance(resource, AwsResource) and not resource.is_managed_by_iac
        return self.get_all_mergeable_resources(condition)

    @functools.lru_cache(maxsize=None)
    def get_all_taggable_resources(self) -> List[_TMergeAble]:
        condition: Callable = lambda aws_resource: aws_resource.is_tagable
        return self.get_all_mergeable_resources(condition)

    def get_all_mergeable_resources(self, condition: Callable = lambda resource: True) -> List[_TMergeAble]:
        all_resources: List[Mergeable] = []
        for _, attribute in vars(self).items():
            if attribute is self.invalidated_resources:
                continue
            if isinstance(attribute, list):
                iterable = attribute
            elif isinstance(attribute, (dict, AliasesDict)):
                iterable = attribute.values()
            else:
                continue
            for resource in iterable:
                if isinstance(resource, Mergeable) and condition(resource):
                    all_resources.append(resource)
        return all_resources
