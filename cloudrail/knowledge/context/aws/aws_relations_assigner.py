import json
import logging
import os
import re
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple, TypeVar, Union

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.account.account import Account
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import ApiGatewayIntegration
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method_settings import ApiGatewayMethodSettings
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_stage import ApiGatewayStage
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
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_association import NetworkAclAssociation
from cloudrail.knowledge.context.aws.resources.fsx.fsx_windows_file_system import FsxWindowsFileSystem
from cloudrail.knowledge.context.aws.resources.iam.principal import PrincipalType
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_policy import LambdaPolicy
from cloudrail.knowledge.context.connection import PolicyEvaluation
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.batch.batch_compute_environment import BatchComputeEnvironment
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_list import CloudFrontDistribution, OriginConfig
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_logging import CloudfrontDistributionLogging
from cloudrail.knowledge.context.aws.resources.cloudfront.origin_access_identity import OriginAccessIdentity
from cloudrail.knowledge.context.aws.resources.cloudhsmv2.cloudhsm_v2_cluster import CloudHsmV2Cluster
from cloudrail.knowledge.context.aws.resources.cloudhsmv2.cloudhsm_v2_hsm import CloudHsmV2Hsm
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_event_target import CloudWatchEventTarget
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_log_group import CloudWatchLogGroup
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloudwatch_logs_destination import CloudWatchLogsDestination
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloudwatch_logs_destination_policy import CloudWatchLogsDestinationPolicy
from cloudrail.knowledge.context.aws.resources.codebuild.codebuild_project import CodeBuildProject
from cloudrail.knowledge.context.aws.resources.codebuild.codebuild_report_group import CodeBuildReportGroup
from cloudrail.knowledge.context.aws.resources.dms.dms_replication_instance import DmsReplicationInstance
from cloudrail.knowledge.context.aws.resources.dms.dms_replication_instance_subnet_group import DmsReplicationInstanceSubnetGroup
from cloudrail.knowledge.context.aws.resources.docdb.docdb_cluster import DocumentDbCluster
from cloudrail.knowledge.context.aws.resources.docdb.docdb_cluster_parameter_group import DocDbClusterParameterGroup
from cloudrail.knowledge.context.aws.resources.ds.directory_service import DirectoryService
from cloudrail.knowledge.context.aws.resources.dynamodb.dynamodb_table import DynamoDbTable
from cloudrail.knowledge.context.aws.resources.ec2.ec2_image import Ec2Image
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.elastic_ip import ElasticIp
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.aws.resources.ec2.main_route_table_association import MainRouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.nat_gateways import NatGateways
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.resources.ec2.network_acl_rule import NetworkAclRule, RuleAction, RuleType
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.peering_connection import PeeringConnection
from cloudrail.knowledge.context.aws.resources.ec2.route import Route, RouteTargetType
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.route_table_association import RouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import ConnectionType, SecurityGroupRule, SecurityGroupRulePropertyType
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway import TransitGateway
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_resource_type import TransitGatewayResourceType
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route import TransitGatewayRoute, TransitGatewayRouteState, \
    TransitGatewayRouteType
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
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.resources.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import EcsTaskDefinition
from cloudrail.knowledge.context.aws.resources.efs.efs_file_system import ElasticFileSystem
from cloudrail.knowledge.context.aws.resources.efs.efs_mount_target import EfsMountTarget
from cloudrail.knowledge.context.aws.resources.efs.efs_policy import EfsPolicy
from cloudrail.knowledge.context.aws.resources.eks.eks_cluster import EksCluster
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_cluster import ElastiCacheCluster
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_replication_group import ElastiCacheReplicationGroup
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_subnet_group import ElastiCacheSubnetGroup
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer, LoadBalancerType
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_attributes import LoadBalancerAttributes
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_listener import LoadBalancerListener
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target import LoadBalancerTarget
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group import LoadBalancerTargetGroup
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group_association import LoadBalancerTargetGroupAssociation
from cloudrail.knowledge.context.aws.resources.emr.emr_cluster import EmrCluster
from cloudrail.knowledge.context.aws.resources.emr.emr_public_access_config import EmrPublicAccessConfiguration
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain_policy import ElasticSearchDomainPolicy
from cloudrail.knowledge.context.aws.resources.glacier.glacier_vault import GlacierVault
from cloudrail.knowledge.context.aws.resources.glacier.glacier_vault_policy import GlacierVaultPolicy
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator import GlobalAccelerator
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator_attributes import GlobalAcceleratorAttribute
from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator_endpoint_group import GlobalAcceleratorEndpointGroup
from cloudrail.knowledge.context.aws.resources.glue.glue_connection import GlueConnection
from cloudrail.knowledge.context.aws.resources.iam.iam_group import IamGroup
from cloudrail.knowledge.context.aws.resources.iam.iam_group_membership import IamGroupMembership
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.resources.iam.iam_instance_profile import IamInstanceProfile
from cloudrail.knowledge.context.aws.resources.iam.iam_policy_attachment import IamPolicyAttachment
from cloudrail.knowledge.context.aws.resources.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.resources.iam.iam_user_group_membership import IamUserGroupMembership
from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy, InlinePolicy, ManagedPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_group_attachment import PolicyGroupAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_role_attachment import PolicyRoleAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_user_attachment import PolicyUserAttachment
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.iam.role_last_used import RoleLastUsed
from cloudrail.knowledge.context.aws.resources.kinesis.kinesis_firehose_stream import KinesisFirehoseStream
from cloudrail.knowledge.context.aws.resources.kms.kms_alias import KmsAlias
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_policy import KmsKeyPolicy
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import create_lambda_function_arn, LambdaAlias
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.mq.mq_broker import MqBroker
from cloudrail.knowledge.context.aws.resources.neptune.neptune_cluster import NeptuneCluster
from cloudrail.knowledge.context.aws.resources.neptune.neptune_instance import NeptuneInstance
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.prefix_lists import PrefixLists
from cloudrail.knowledge.context.aws.resources.rds.db_subnet_group import DbSubnetGroup
from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_global_cluster import RdsGlobalCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.aws.resources.redshift.redshift_logging import RedshiftLogging
from cloudrail.knowledge.context.aws.resources.redshift.redshift_subnet_group import RedshiftSubnetGroup
from cloudrail.knowledge.context.aws.resources.resourcegroupstaggingapi.resource_tag_mapping_list import ResourceTagMappingList
from cloudrail.knowledge.context.aws.resources.s3.public_access_block_settings import create_pseudo_access_block, PublicAccessBlockLevel, \
    PublicAccessBlockSettings
from cloudrail.knowledge.context.aws.resources.s3.s3_acl import S3ACL
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_access_point import S3BucketAccessPoint
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_encryption import S3BucketEncryption
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_logging import S3BucketLogging
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_object import S3BucketObject
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_versioning import S3BucketVersioning
from cloudrail.knowledge.context.aws.resources.s3.s3_access_point_policy import S3AccessPointPolicy
from cloudrail.knowledge.context.aws.resources.s3.s3_policy import S3Policy
from cloudrail.knowledge.context.aws.resources.s3outposts.s3outpost_endpoint import S3OutpostEndpoint
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
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.context.mergeable import EntityOrigin, Mergeable
from cloudrail.knowledge.utils.arn_utils import build_arn, get_arn_resource, is_valid_arn
from cloudrail.knowledge.utils.utils import flat_list, hash_list

from cloudrail.knowledge.context.aws.parallel.create_iam_entity_to_esc_actions_task import CreateIamEntityToEscActionsMapTask
from cloudrail.knowledge.context.aws.pseudo_builder import PseudoBuilder
from cloudrail.knowledge.context.aws.resources_assigner_util import ResourcesAssignerUtil
from cloudrail.knowledge.context.aws.service_ip_range import ServiceIpRangeBuilder
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, FunctionData, IterFunctionData
from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator
from cloudrail.knowledge.utils.policy_evaluator import is_action_subset_allowed, PolicyEvaluator
from cloudrail.knowledge.utils.policy_utils import is_policy_block_public_access


class AwsRelationsAssigner(DependencyInvocation):
    _TMergeable = TypeVar('_TMergeable', bound=Mergeable)

    def __init__(self, ctx: AwsEnvironmentContext):
        self.pseudo_builder = PseudoBuilder(ctx)
        self.pseudo_builder.create_missing_policies()
        self.pseudo_builder.create_cloudwatch_log_group_for_lambda(ctx.lambda_function_list)
        bucket_name_to_region_map: Dict[str, str] = {location.bucket_name: location.bucket_region for location in ctx.s3_bucket_regions}
        if not ctx.prefix_lists:
            region_to_prefix_lists_map: Dict[str, PrefixLists] = ServiceIpRangeBuilder.to_prefix_lists()
            ctx.prefix_lists = list(region_to_prefix_lists_map.values())

        role_by_arn_map: Dict[str, Role] = self._create_role_by_arn_map(ctx.roles)

        function_pool = [
            ### All Resources###
            IterFunctionData(self._assign_resources_tags, [resource for resource in ctx.get_all_non_iac_managed_resources()
                                                           if not resource.tags and resource.is_tagable and resource.get_arn()
                                                           and not isinstance(resource, ResourceTagMappingList)],
                             (ctx.resources_tagging_list,)),
            ### VPC ###
            IterFunctionData(self._assign_vpc_endpoints, ctx.vpc_endpoints, (ctx.vpcs,)),
            IterFunctionData(self._assign_vpc_default_and_main_route_tables, ctx.vpcs, (ctx.route_tables, ctx.main_route_table_associations)),
            IterFunctionData(self._assign_vpc_default_security_group, ctx.vpcs, (ctx.security_groups,)),
            IterFunctionData(self._assign_vpc_subnets, ctx.vpcs, (ctx.subnets,), [self._assign_subnet_vpc]),
            IterFunctionData(self._assign_vpc_default_nacl, ctx.vpcs, (ctx.network_acls,)),
            IterFunctionData(self._assign_vpc_attributes, ctx.vpcs_attributes, (ctx.vpcs, )),
            IterFunctionData(self._assign_internet_gateway, ctx.vpcs, (ctx.internet_gateways,),
                             [self._assign_vpc_internet_gateway_attachment]),
            IterFunctionData(self._assign_vpc_internet_gateway_attachment, ctx.vpc_gateway_attachment,
                             (ctx.vpcs, AliasesDict(*ctx.internet_gateways))),
            ### Transit Gateway ###
            IterFunctionData(self._assign_transit_gateway_route_tables, ctx.transit_gateways, (ctx.transit_gateway_route_tables,)),
            IterFunctionData(self._assign_transit_gateway_route_table_associations,
                             ctx.transit_gateway_route_tables, (ctx.transit_gateway_route_table_associations,)),
            IterFunctionData(self._assign_transit_gateway_associations_attachments,
                             ctx.transit_gateway_route_table_associations, (ctx.transit_gateway_attachments,)),
            IterFunctionData(self._assign_transit_gateway_propagation_attachments,
                             ctx.transit_gateway_route_table_propagations, (ctx.transit_gateway_attachments,)),
            IterFunctionData(self._assign_transit_gateway_propagated_routes,
                             ctx.transit_gateway_route_table_propagations, (ctx.transit_gateway_routes, ctx.vpcs)),
            IterFunctionData(self._assign_transit_gateway_route_table_routes, ctx.transit_gateway_route_tables, (ctx.transit_gateway_routes,),
                             [self._assign_transit_gateway_propagated_routes]),
            ### S3 ###
            IterFunctionData(self._assign_s3_bucket_region, ctx.s3_buckets, (bucket_name_to_region_map,)),
            IterFunctionData(self._assign_s3_bucket_acls, ctx.s3_buckets, (ctx.s3_bucket_acls,)),
            IterFunctionData(self._assign_s3_bucket_access_points, ctx.s3_buckets, (ctx.s3_bucket_access_points,)),
            IterFunctionData(self._update_s3_bucket_policies_canonical, [policy for policy in  ctx.s3_bucket_policies if policy.is_managed_by_iac],
                             (ctx.origin_access_identity_list,)),
            IterFunctionData(self._assign_s3_bucket_policy, ctx.s3_buckets, (ctx.s3_bucket_policies,),
                             [self._update_s3_bucket_policies_canonical]),
            IterFunctionData(self._assign_s3_access_point_policy, ctx.s3_bucket_access_points, (ctx.s3_bucket_access_points_policies,)),
            IterFunctionData(self._assign_s3_access_block_settings, ctx.s3_buckets, (ctx.s3_public_access_block_settings_list,)),
            IterFunctionData(self._assign_encryption_data_to_s3_bucket, ctx.s3_buckets, (ctx.s3_bucket_encryption,)),
            IterFunctionData(self._assign_versioning_data_to_s3_bucket, ctx.s3_buckets, (ctx.s3_bucket_versioning,)),
            FunctionData(self._assign_acls_owner_data, (ctx.s3_bucket_acls,)),
            IterFunctionData(self._assign_s3_bucket_objects, ctx.s3_bucket_objects, (ctx.s3_buckets,)),
            IterFunctionData(self._assign_s3_bucket_logs, ctx.s3_buckets, (ctx.s3_bucket_logs,)),
            ### IAM ###
            IterFunctionData(self._assign_iam_assume_role_policies, ctx.roles, (ctx.assume_role_policies,)),
            IterFunctionData(self._assign_iam_roles_policies, ctx.roles, (ctx.policies, ctx.policy_role_attachments)),
            IterFunctionData(self._assign_iam_roles_policies_from_iam_policy_attachment, ctx.roles, (ctx.policies, ctx.iam_policy_attachments)),
            IterFunctionData(self._assign_iam_roles_inline_policies, ctx.roles, (ctx.role_inline_policies,)),
            IterFunctionData(self._assign_iam_users_policies, ctx.users, (ctx.policies, ctx.policy_user_attachments)),
            IterFunctionData(self._assign_iam_users_inline_policies, ctx.users, (ctx.user_inline_policies,)),
            IterFunctionData(self._assign_iam_users_policies_from_iam_policy_attachment, ctx.users, (ctx.policies, ctx.iam_policy_attachments)),
            IterFunctionData(self._assign_iam_groups_policies, ctx.groups, (ctx.policies, ctx.policy_group_attachments)),
            IterFunctionData(self._assign_iam_groups_policies_from_iam_policy_attachment, ctx.groups, (ctx.policies, ctx.iam_policy_attachments)),
            IterFunctionData(self._assign_iam_groups_inline_policies, ctx.groups, (ctx.group_inline_policies,)),
            IterFunctionData(self._assign_iam_group_membership, ctx.iam_group_membership, (ctx.groups, ctx.users)),
            IterFunctionData(self._assign_iam_user_group_membership, ctx.iam_user_group_membership, (ctx.groups, ctx.users)),
            IterFunctionData(self._assign_iam_role_permission_boundary, ctx.roles, (ctx.policies,)),
            IterFunctionData(self._assign_iam_user_permission_boundary, ctx.users, (ctx.policies,)),
            FunctionData(self._assign_esc_actions_map_to_iam_entity,
                         ({iam_entity.qualified_arn: iam_entity for iam_entity in ctx.get_all_iam_entities()},)),
            IterFunctionData(self._assign_ec2_data_to_iam_profile, ctx.iam_instance_profiles, (ctx.ec2s,)),
            IterFunctionData(self._assign_roles_last_used_data, ctx.roles, (ctx.roles_last_used,)),
            ### Security Group ###
            IterFunctionData(self._assign_security_group_vpc, ctx.security_groups, (ctx.vpcs,)),
            IterFunctionData(self._assign_security_group_rules, ctx.security_groups, (ctx.security_group_rules,)),
            ### Route Table ###
            IterFunctionData(self._assign_route_table_routes, ctx.route_tables, (ctx.routes, ctx.vpcs)),
            IterFunctionData(self._assign_route_vpc_peering, ctx.routes, (ctx.peering_connections,)),
            IterFunctionData(self._assign_route_table_vpc_endpoint_routes, ctx.vpc_endpoint_route_table_associations,
                             (ctx.route_tables, ctx.prefix_lists, ctx.vpc_endpoints),
                             [self._assign_route_table_routes]),
            IterFunctionData(self._assign_route_tables_to_vpc_endpoint, [vpce_inet for vpce_inet in ctx.vpc_endpoints
                                                                         if isinstance(vpce_inet, VpcEndpointGateway)],
                             (ctx.route_tables, ctx.vpc_endpoint_route_table_associations)),
            ### Subnet ###
            IterFunctionData(self._assign_subnet_vpc, ctx.subnets, (ctx.vpcs,)),
            IterFunctionData(self._assign_subnet_route_table, ctx.subnets, (ctx.route_tables, ctx.route_table_associations),
                             [self._assign_vpc_default_and_main_route_tables, self._assign_subnet_vpc]),
            IterFunctionData(self._assign_subnet_network_acl, ctx.subnets, (ctx.network_acls,), [self._assign_subnet_vpc,
                                                                                                 self._assign_vpc_default_nacl,
                                                                                                 self._assign_subnet_id_to_nacl]),
            ### NACL ###
            IterFunctionData(self._assign_network_acl_rules, ctx.network_acls, (ctx.network_acl_rules,), [self._assign_subnet_network_acl]),
            IterFunctionData(self._assign_default_network_acl_rules_for_tf, [nacl for nacl in ctx.network_acls if nacl.is_managed_by_iac],
                             (ctx.vpcs,)),
            IterFunctionData(self._assign_subnet_id_to_nacl, ctx.network_acl_associations, (ctx.network_acls,)),
            ### EC2 ###
            IterFunctionData(self._assign_ec2_role_permissions, ctx.ec2s,
                             (AliasesDict(*ctx.roles), AliasesDict(*ctx.iam_instance_profiles)),
                             [self._add_auto_scale_ec2s]),
            IterFunctionData(self._assign_ec2_network_interfaces, ctx.ec2s, (ctx.network_interfaces, ctx.subnets, ctx.vpcs)),
            IterFunctionData(self._assign_ec2_images_data, ctx.ec2s, (ctx.ec2_images,)),
            ### Auto-Scale ###
            FunctionData(self._remove_deleted_auto_scale_ec2s, (ctx.ec2s, ctx.auto_scaling_groups,)),
            IterFunctionData(self._assign_auto_scaling_group_launch_template, ctx.auto_scaling_groups, (ctx.launch_templates,)),
            IterFunctionData(self._assign_auto_scaling_group_launch_configuration, ctx.auto_scaling_groups, (ctx.launch_configurations,)),
            IterFunctionData(self._add_auto_scale_ec2s, ctx.auto_scaling_groups, (ctx.load_balancers, ctx.load_balancer_target_groups,
                                                                                  ctx.ec2s, ctx.subnets, ctx.vpcs),
                             [self._assign_subnet_vpc, self._assign_load_balancer_target_groups, self._assign_auto_scaling_group_launch_template,
                              self._assign_auto_scaling_group_launch_configuration]),
            ### Launch Template ###
            IterFunctionData(self._assign_launch_template_security_groups, ctx.launch_templates, (ctx.security_groups,),
                             [self._assign_vpc_default_security_group]),
            IterFunctionData(self._assign_launch_template_network, ctx.launch_templates, (ctx.security_groups, ctx.subnets),
                             [self._assign_launch_template_security_groups]),
            ### Load-Balancer ###
            IterFunctionData(self._assign_load_balancer_network_interfaces, ctx.load_balancers,
                             (ctx.network_interfaces, ctx.subnets, ctx.elastic_ips)),
            IterFunctionData(self._assign_load_balancer_target_groups,
                             ctx.load_balancers, (ctx.load_balancer_target_groups, ctx.load_balancer_target_group_associations)),
            IterFunctionData(self._assign_load_balancer_listener_ports,
                             ctx.load_balancers, (ctx.load_balancer_listeners,)),
            IterFunctionData(self._assign_load_balancer_target_ec2_instance, ctx.load_balancer_targets, (ctx.ec2s,)),
            IterFunctionData(self._assign_load_balancer_target_group_targets, ctx.load_balancer_target_groups, (ctx.load_balancer_targets,)),
            IterFunctionData(self._assign_load_balancer_attributes, ctx.load_balancers, (ctx.load_balancers_attributes,)),
            ### Network Interface ###
            IterFunctionData(self._assign_network_interface_subnets, ctx.network_interfaces, (ctx.subnets,),
                             [self._assign_ecs_host_eni, self._assign_subnet_vpc]),
            IterFunctionData(self._assign_network_interface_security_groups, ctx.network_interfaces, (ctx.security_groups,),
                             [self._assign_vpc_default_security_group, self._assign_network_interface_subnets]),
            IterFunctionData(self._assign_eni_to_vpc_endpoint, [vpce_inet for vpce_inet in ctx.vpc_endpoints
                                                                if isinstance(vpce_inet, VpcEndpointInterface)],
                             (ctx.network_interfaces,),
                             [self._assign_network_interface_security_groups, self._assign_vpc_default_security_group]),

            ### Vpc-Peering ###
            IterFunctionData(self._assign_peering_connection_vpc_cidrs, ctx.peering_connections, (ctx.vpcs,)),
            ### ECS ###
            IterFunctionData(self._assign_ecs_service_to_cluster, ctx.ecs_cluster_list, (ctx.ecs_service_list,)),
            IterFunctionData(self._assign_cloud_watch_event_target_to_cluster, ctx.ecs_cluster_list, (ctx.cloud_watch_event_target_list,)),
            IterFunctionData(self._assign_task_definition_to_ecs_instance, ctx.ecs_task_definitions, (ctx.ecs_cluster_list,),
                             [self._assign_ecs_service_to_cluster, self._assign_cloud_watch_event_target_to_cluster]),
            IterFunctionData(self._assign_iam_role_to_task_definition, ctx.ecs_cluster_list, (role_by_arn_map,),
                             [self._assign_task_definition_to_ecs_instance]),
            IterFunctionData(self._assign_ecs_host_eni, ctx.ecs_service_list + ctx.ecs_targets_list, (ctx.subnets,),
                             [self._assign_vpc_default_security_group, self._assign_task_definition_to_ecs_instance]),
            IterFunctionData(self._assign_ecs_cluster_name_to_service, ctx.ecs_service_list, (ctx.ecs_cluster_list,)),
            IterFunctionData(self._assign_ecs_cluster_name_to_target, ctx.ecs_targets_list, (ctx.ecs_cluster_list,)),
            ### Redshift ###
            IterFunctionData(self._assign_redshift_subnets,
                             ctx.redshift_clusters, (ctx.redshift_subnet_groups, ctx.subnets, ctx.accounts, ctx.vpcs),
                             [self._assign_vpc_default_security_group]),
            IterFunctionData(self._assign_redshift_logs, ctx.redshift_clusters, (ctx.redshift_logs,)),
            ### RDS ###
            IterFunctionData(self._assign_rds_cluster_default_security_group, ctx.rds_clusters, (),
                             [self._assign_vpc_default_security_group, self._assign_subnet_vpc]),
            IterFunctionData(self._assign_rds_instance_subnets,
                             ctx.rds_instances, (ctx.rds_clusters, ctx.vpcs, ctx.db_subnet_groups, ctx.subnets),
                             [self._assign_vpc_default_security_group]),
            IterFunctionData(self._assign_rds_instances_to_cluster, ctx.rds_clusters, (ctx.rds_instances,)),
            IterFunctionData(self._assign_rds_instance_missing_data_from_cluster, ctx.rds_instances, (ctx.rds_clusters,)),
            IterFunctionData(self._assign_rds_global_cluster_encrypted_at_rest, ctx.rds_global_clusters, (ctx.rds_clusters,)),
            IterFunctionData(self._assign_keys_data_to_rds_cluster_instance, ctx.rds_instances, (ctx.kms_keys,)),
            ### Elastic-Search ###
            IterFunctionData(self._assign_elastic_search_domain_subnets,
                             ctx.elastic_search_domains, (ctx.subnets,),
                             [self._assign_vpc_default_security_group, self._assign_subnet_vpc]),
            IterFunctionData(self._assign_policy_data_to_elastic_search_domain, ctx.elastic_search_domains, (ctx.elastic_search_domains_policies,)),
            ### EKS ###
            IterFunctionData(self._assign_eks_cluster_eni, ctx.eks_clusters, (ctx.subnets, ctx.security_groups),
                             [self._assign_vpc_default_security_group, self._assign_subnet_vpc]),
            ### NatGateways
            IterFunctionData(self._assign_nat_gateways_eni_list,
                             ctx.nat_gateway_list, (ctx.network_interfaces, ctx.subnets),
                             [self._assign_subnet_vpc, self._assign_network_interface_subnets]),
            ### ApiGateway
            IterFunctionData(self._assign_method_settings_to_api_gateway, ctx.rest_api_gw, (ctx.api_gateway_method_settings,)),
            IterFunctionData(self._assign_policy_data_to_rest_api_gw, ctx.rest_api_gw, (ctx.rest_api_gw_policies,)),
            IterFunctionData(self._assign_api_id_to_domain_data, ctx.rest_api_gw_domains, (ctx.rest_api_gw_mappings,)),
            IterFunctionData(self._assign_rest_api_domain, ctx.rest_api_gw, (ctx.rest_api_gw_domains,),
                             [self._assign_api_id_to_domain_data]),
            IterFunctionData(self._assign_integration_to_api_gateway_method, ctx.api_gateway_integrations, (ctx.api_gateway_methods,)),
            IterFunctionData(self._assign_lambda_function_to_api_gateway_integration, ctx.api_gateway_integrations, (ctx.lambda_function_list,),
                             [self._exclude_lambda_functions]),
            IterFunctionData(self._assign_api_gw_methods_to_api_gw, ctx.rest_api_gw, (ctx.api_gateway_methods,),
                             [self._assign_integration_to_api_gateway_method, self._assign_lambda_function_to_api_gateway_integration]),
            IterFunctionData(self._assign_api_gateway_is_public, ctx.rest_api_gw, (),
                             [self._assign_policy_data_to_rest_api_gw]),
            IterFunctionData(self._assign_api_gateway_stage, ctx.rest_api_gw, (ctx.rest_api_stages,),
                             [self._assign_api_gateway_stage_method_settings]),
            IterFunctionData(self._assign_api_gateway_stage_method_settings, ctx.rest_api_stages, (ctx.api_gateway_method_settings,)),
            ### CodeBuild
            IterFunctionData(self._assign_kms_key_from_alias_to_codebuild_project, ctx.codebuild_projects, (ctx.kms_aliases,)),
            IterFunctionData(self._assign_kms_key_from_alias_to_codebuild_report_group, ctx.codebuild_report_groups,
                             (ctx.kms_aliases,)),
            IterFunctionData(self._assign_keys_data_to_code_build_project, ctx.codebuild_projects, (ctx.kms_keys,),
                             [self._assign_policy_data_to_kms_keys, self._assign_kms_key_from_alias_to_codebuild_project]),
            IterFunctionData(self._assign_keys_data_to_codebuild_report_group, ctx.codebuild_report_groups, (ctx.kms_keys,),
                             [self._assign_kms_key_from_alias_to_codebuild_report_group]),
            IterFunctionData(self._assign_eni_to_codebuild_project, ctx.codebuild_projects, (ctx.subnets,)),
            ### AthenaWorkgroups
            IterFunctionData(self._assign_keys_data_to_athena_workgroup, ctx.athena_workgroups, (ctx.kms_keys,),
                             [self._assign_policy_data_to_kms_keys]),
            ### CloudWatch
            IterFunctionData(self._assign_keys_data_to_cloudwatch_log_group, ctx.cloud_watch_log_groups,
                             (ctx.kms_keys,), [self._assign_policy_data_to_kms_keys]),
            ### SqsQueue
            IterFunctionData(self._assign_policy_data_to_sqs_queue, ctx.sqs_queues, (ctx.sqs_queues_policy,)),
            IterFunctionData(self._assign_keys_data_to_sqs_queue, ctx.sqs_queues, (ctx.kms_keys,)),
            ### EcrRepository
            IterFunctionData(self._assign_policy_data_to_ecr_repository, ctx.ecr_repositories, (ctx.ecr_repositories_policy,)),
            IterFunctionData(self._assign_keys_data_to_ecr_repository, ctx.ecr_repositories, (ctx.kms_keys,),
                             [self._assign_alias_data_to_kms_keys]),
            ### CloudWatch Logs Destinations
            IterFunctionData(self._assign_policy_data_to_cloudwatch_logs_destination, ctx.cloudwatch_logs_destinations,
                             (ctx.cloudwatch_logs_destination_policies,)),
            ### KmsKey
            IterFunctionData(self._assign_policy_data_to_kms_keys, ctx.kms_keys, (ctx.kms_keys_policies,)),
            IterFunctionData(self._assign_policy_data_to_ecr_repository, ctx.ecr_repositories, (ctx.ecr_repositories_policy,)),
            IterFunctionData(self._assign_keys_data_to_cloudwatch_log_group, ctx.cloud_watch_log_groups, (ctx.kms_keys,)),
            IterFunctionData(self._assign_keys_data_to_code_build_project, ctx.codebuild_projects, (ctx.kms_keys,)),
            IterFunctionData(self._assign_alias_data_to_kms_keys, ctx.kms_keys, (ctx.kms_aliases,)),
            IterFunctionData(self._assign_key_manager_data_to_keys_alias, ctx.kms_aliases, (ctx.kms_keys,),
                             [self._assign_alias_data_to_kms_keys]),
            IterFunctionData(self._assign_keys_data_to_ssm_parameter, ctx.ssm_parameters, (ctx.kms_keys,)),
            IterFunctionData(self._assign_keys_data_to_sagemaker_notebook_instance, ctx.sagemaker_notebook_instances, (ctx.kms_keys,)),
            ### Lambda Function ###
            IterFunctionData(self._assign_lambda_function_alias, ctx.lambda_function_list, (ctx.lambda_aliases,)),
            FunctionData(self._enrich_lambda_function_arn_with_tf_address, (ctx.lambda_function_list,),
                         [self._assign_lambda_function_alias]),
            FunctionData(self._exclude_lambda_functions, (ctx.lambda_function_list,),
                         [self._assign_lambda_function_alias]),
            IterFunctionData(self._assign_lambda_function_role, ctx.lambda_function_list, (role_by_arn_map,),
                             [self._exclude_lambda_functions]),
            IterFunctionData(self._assign_lambda_function_policy, ctx.lambda_function_list, (ctx.lambda_policies,),
                             [self._assign_lambda_function_alias, self._enrich_lambda_function_arn_with_tf_address]),
            IterFunctionData(self._assign_lambda_vpc_config, ctx.lambda_function_list, (ctx.subnets, ctx.security_groups),
                             [self._exclude_lambda_functions]),
            IterFunctionData(self._assign_lambda_log_group, ctx.lambda_function_list, (ctx.cloud_watch_log_groups,)),
            IterFunctionData(self._assign_eni_to_lambda_function, [function for function in ctx.lambda_function_list if function.vpc_config],
                             (ctx.subnets,), [self._assign_lambda_vpc_config]),
            ### Glacier Vault ###
            IterFunctionData(self._assign_glacier_vault_policies, ctx.glacier_vaults, (ctx.glacier_vaults_policies,)),
            ### Efs ###
            IterFunctionData(self._assign_file_system_policies, ctx.efs_file_systems, (ctx.efs_file_systems_policies,)),
            IterFunctionData(self._assign_eni_to_efs_mount_target, ctx.efs_mount_targets, (ctx.subnets,),
                             [self._assign_vpc_default_security_group]),
            ### Secrets Manager Secret ###
            IterFunctionData(self._assign_secrets_manager_secrets_policies, ctx.secrets_manager_secrets, (ctx.secrets_manager_secrets_policies,)),
            IterFunctionData(self._assign_keys_data_to_secrets_manager, ctx.secrets_manager_secrets, (ctx.kms_keys,)),
            ### DocDB Cluster
            IterFunctionData(self._assign_docdb_parameter_group_name, ctx.docdb_cluster, (ctx.docdb_cluster_parameter_groups,)),
            IterFunctionData(self._assign_kms_key_from_alias_to_docdb_cluster, ctx.docdb_cluster, (ctx.kms_aliases,)),
            IterFunctionData(self._assign_kms_key_manager_to_docdb_cluster, ctx.docdb_cluster, (ctx.kms_keys,),
                             [self._assign_kms_key_from_alias_to_docdb_cluster]),
            ### Neptune Cluster
            IterFunctionData(self._assign_keys_data_to_neptune_cluster, ctx.neptune_clusters, (ctx.kms_keys,)),
            IterFunctionData(self._assign_network_data_from_neptune_cluster, ctx.neptune_cluster_instances, (ctx.neptune_clusters,)),
            IterFunctionData(self._assign_neptune_instance_to_cluster, ctx.neptune_clusters, (ctx.neptune_cluster_instances,),
                             [self._assign_network_data_from_neptune_cluster]),
            IterFunctionData(self._assign_neptune_instance_subnets,
                             ctx.neptune_cluster_instances, (ctx.db_subnet_groups, ctx.subnets),
                             [self._assign_vpc_default_security_group, self._assign_network_data_from_neptune_cluster]),
            ### SNS Topic
            IterFunctionData(self._assign_keys_data_to_sns_topic, ctx.sns_topics, (ctx.kms_keys,)),
            ### Xray Encryption
            IterFunctionData(self._assign_keys_data_to_xray_encryption, ctx.xray_encryption_configurations, (ctx.kms_keys,)),
            ### Workspaces
            IterFunctionData(self._assign_keys_data_to_workspace, ctx.workspaces, (ctx.kms_keys,),
                             [self._assign_alias_data_to_kms_keys]),
            IterFunctionData(self._assign_cloud_directory_to_workspace_directory, ctx.workspaces_directories, (ctx.cloud_directories,),
                             [self._assign_security_group_controller_to_directory]),
            IterFunctionData(self._assign_networking_to_workspace_directory, ctx.workspaces_directories, (ctx.security_groups, ctx.subnets, ctx.vpcs),
                             [self._assign_cloud_directory_to_workspace_directory]),
            ### Dms
            IterFunctionData(self._assign_dms_instance_networking_data, ctx.dms_replication_instances,
                             (ctx.vpcs, ctx.subnets, ctx.dms_replication_instance_subnet_groups),
                             [self._assign_vpc_default_security_group, self._assign_security_group_rules, self._assign_security_group_vpc,
                              self._assign_vpc_endpoints]),
            IterFunctionData(self._assign_eni_to_dms, ctx.dms_replication_instances, (ctx.subnets,),
                             [self._assign_dms_instance_networking_data]),
            ### CloudFront
            IterFunctionData(self._assign_aoi_to_cloudfront_distribution, ctx.origin_access_identity_list, (ctx.cloudfront_distribution_list,)),
            IterFunctionData(self._assign_logging_to_cloudfront_distribution, ctx.cloudfront_distribution_list, (ctx.cloudfront_log_settings,)),
            ### Elasticache
            IterFunctionData(self._assign_replication_group_network_data_for_aws_scanner,
                             [rep_group for rep_group in ctx.elasti_cache_replication_groups if not rep_group.is_managed_by_iac],
                             ([cluster for cluster in ctx.elasticache_clusters if not cluster.is_managed_by_iac],
                              [subnet for subnet in ctx.elasticache_subnet_groups if not subnet.is_managed_by_iac], ctx.vpcs),
                             [self._assign_vpc_default_security_group, self._assign_security_group_rules, self._assign_security_group_vpc]),
            IterFunctionData(self._assign_networking_data_for_elasticache_rep_group_tf,
                             [rep_group for rep_group in ctx.elasti_cache_replication_groups if rep_group.is_managed_by_iac],
                             (ctx.elasticache_subnet_groups, ctx.vpcs)),
            IterFunctionData(self._assign_eni_to_replication_group, ctx.elasti_cache_replication_groups, (ctx.subnets,),
                             [self._assign_replication_group_network_data_for_aws_scanner,
                              self._assign_networking_data_for_elasticache_rep_group_tf]),
            IterFunctionData(self._assign_networking_data_for_elasticache_cluster_aws_scanner,
                             [cluster for cluster in ctx.elasticache_clusters if not cluster.is_managed_by_iac],
                             ([subnet for subnet in ctx.elasticache_subnet_groups if not subnet.is_managed_by_iac], ctx.vpcs),
                             [self._assign_vpc_default_security_group, self._assign_security_group_rules, self._assign_security_group_vpc]),
            IterFunctionData(self._assign_networking_data_for_tf_elasticache_cluster,
                             [cluster for cluster in ctx.elasticache_clusters if cluster.is_managed_by_iac],
                             (ctx.elasticache_subnet_groups, ctx.vpcs, ctx.elasti_cache_replication_groups),
                             [self._assign_eni_to_replication_group]),
            IterFunctionData(self._assign_eni_to_elasticache_cluster, ctx.elasticache_clusters, (ctx.subnets,),
                             [self._assign_networking_data_for_tf_elasticache_cluster,
                              self._assign_networking_data_for_elasticache_cluster_aws_scanner]),
            ### Kinesis Firehose
            IterFunctionData(self._assign_eni_to_kinesis_firehose, ctx.kinesis_firehose_streams, (ctx.subnets,)),
            ### Directory service
            IterFunctionData(self._assign_security_group_controller_to_directory, ctx.cloud_directories, (ctx.security_groups, ctx.vpcs)),
            IterFunctionData(self._assign_eni_to_directory, ctx.cloud_directories, (ctx.subnets,),
                             [self._assign_security_group_controller_to_directory]),
            ### DynamoDB table
            IterFunctionData(self._assign_kms_key_from_alias_to_dynamodb_table, ctx.dynamodb_table_list, (ctx.kms_aliases,)),
            IterFunctionData(self._assign_keys_data_to_dynamodb_table, ctx.dynamodb_table_list, (ctx.kms_keys,),
                             [self._assign_alias_data_to_kms_keys, self._assign_kms_key_from_alias_to_dynamodb_table]),
            ### Batch Compute Environment
            IterFunctionData(self._assign_eni_to_batch_compute, ctx.batch_compute_environments, (ctx.subnets,)),
            ### MQ Broker
            IterFunctionData(self._assign_networking_to_mq_broker, ctx.mq_brokers, (ctx.subnets, ctx.vpcs),
                             [self._assign_vpc_default_security_group]),
            ### Api Gateway V2
            IterFunctionData(self._assign_integration_to_api, ctx.api_gateways_v2, (ctx.api_gateway_v2_integrations,)),
            IterFunctionData(self._assign_vpc_link_to_api_and_eni, ctx.api_gateways_v2, (ctx.api_gateway_v2_vpc_links, ctx.subnets),
                             [self._assign_integration_to_api]),
            ### EMR cluster
            IterFunctionData(self._assign_emr_security_groups_rules_for_tf, [emr for emr in ctx.emr_clusters if emr.is_managed_by_iac],
                             (ctx.security_groups,)),
            IterFunctionData(self._assign_public_access_data_to_emr, ctx.emr_clusters, (ctx.emr_public_access_configurations,)),
            IterFunctionData(self._assign_networking_to_emr, ctx.emr_clusters, (ctx.subnets, ctx.vpcs),
                             [self._assign_public_access_data_to_emr]),
            ### Global Acceleration
            IterFunctionData(self._assign_endpoint_resource_to_endpoint_group, ctx.global_accelerator_endpoint_groups,
                             ([ctx.load_balancers + ctx.elastic_ips + ctx.ec2s][0],)),
            IterFunctionData(self._assign_eni_endpoint_group, ctx.global_accelerator_endpoint_groups, (ctx.vpcs,),
                             [self._assign_endpoint_resource_to_endpoint_group, self._assign_load_balancer_network_interfaces,
                              self._assign_ec2_network_interfaces]),
            IterFunctionData(self._assign_attributes_to_global_ac, ctx.global_accelerators, (ctx.global_accelerator_attributes,)),
            ### CloudHsmV2Cluster
            IterFunctionData(self._assign_hsm_to_cloudhsm_cluster, ctx.cloudhsm_v2_clusters, (ctx.cloudhsm_list,)),
            IterFunctionData(self._assign_eni_to_cloudhsm_cluster, ctx.cloudhsm_v2_clusters, (ctx.subnets, ctx.vpcs),
                             [self._assign_hsm_to_cloudhsm_cluster]),
            ### S3 Outpost Endpoint
            IterFunctionData(self._assign_eni_to_s3outpost_endpoint, ctx.s3outpost_endpoints, (ctx.subnets,)),
            ### WorkLink fleet
            IterFunctionData(self._assign_eni_to_worklink_fleet, ctx.worklink_fleets, (ctx.subnets,)),
            ### Glue connection
            IterFunctionData(self._assign_eni_to_glue_connection, ctx.glue_connections, (ctx.subnets,)),
            ### FSx
            IterFunctionData(self._assign_keys_data_to_fsx_windows_file_system, ctx.fsx_windows_file_systems, (ctx.kms_keys,))

        ]
        super().__init__(function_pool, context=ctx)

    @staticmethod
    def _create_role_by_arn_map(roles: List[Role]) -> Dict[str, Role]:
        role_by_arn_map: Dict[str, Role] = {}
        for role in roles:
            role_by_arn_map[role.qualified_arn] = role
            if role.arn:
                role_by_arn_map[role.arn] = role
        return role_by_arn_map

    @staticmethod
    def _assign_vpc_endpoints(endpoint: VpcEndpoint, vpcs: AliasesDict[Vpc]):
        vpc = ResourceInvalidator.get_by_id(vpcs, endpoint.vpc_id, True, endpoint)
        vpc.endpoints.append(endpoint)

    def _assign_vpc_default_and_main_route_tables(self,
                                                  vpc: Vpc,
                                                  route_tables: AliasesDict[RouteTable],
                                                  main_route_table_association: List[MainRouteTableAssociation]):

        def get_default_rt():
            if main_route_table_id := next((rta.route_table_id for rta in main_route_table_association if rta.vpc_id == vpc.vpc_id), None):
                return ResourceInvalidator.get_by_id(route_tables, main_route_table_id, True, vpc)
            if default_rt := next((rt for rt in route_tables if rt.is_managed_by_iac and rt.is_main_route_table and rt.vpc_id == vpc.vpc_id),
                                  None):
                return default_rt
            if vpc.raw_data.main_route_table_id:
                if default_rt := ResourceInvalidator.get_by_id(route_tables, vpc.raw_data.main_route_table_id, False):
                    return default_rt
            if vpc.raw_data.default_route_table_id:
                if default_rt := ResourceInvalidator.get_by_id(route_tables, vpc.raw_data.default_route_table_id, False):
                    return default_rt
            if vpc.is_managed_by_iac:
                return self.pseudo_builder.create_main_route_table(vpc.vpc_id, vpc.account, vpc.region)
            return None

        vpc.main_route_table = ResourceInvalidator.get_by_logic(get_default_rt, True, vpc, 'Could not associate main route table')
        vpc.main_route_table.with_aliases(vpc.raw_data.main_route_table_id, vpc.raw_data.default_route_table_id)
        vpc.main_route_table.is_main_route_table = True

        route_tables.update(vpc.main_route_table)

    def _assign_vpc_default_security_group(self, vpc: Vpc, security_groups: AliasesDict[SecurityGroup]):
        def get_default_security_group():
            default_sg = self._find_default_vpc_security_group(vpc.aliases, security_groups)
            if not default_sg and vpc.is_managed_by_iac:
                default_sg = self.pseudo_builder.create_security_group(vpc, True, vpc.account, vpc.region)
            return default_sg

        vpc.default_security_group = ResourceInvalidator.get_by_logic(get_default_security_group,
                                                                      True, vpc, 'Could not find default security group')

        if vpc.raw_data.default_security_group_id:
            vpc.default_security_group.with_aliases(vpc.raw_data.default_security_group_id)
            security_groups.update(vpc.default_security_group)

    @staticmethod
    def _assign_vpc_attributes(vpc_attribute: VpcAttribute, vpcs: AliasesDict[Vpc]):
        vpc = ResourceInvalidator.get_by_id(vpcs, vpc_attribute.vpc_id, True, vpc_attribute)
        if vpc_attribute.attribute_name == 'EnableDnsSupport':
            vpc.enable_dns_support = vpc_attribute.enable
        else:
            vpc.enable_dns_hostnames = vpc_attribute.enable

    def _assign_vpc_default_nacl(self, vpc: Vpc, nacls: AliasesDict[NetworkAcl]):
        def get_default_nacl():
            nacl = next((nacl for nacl in nacls if nacl.is_default and nacl.vpc_id in vpc.aliases), None)
            if not nacl and vpc.is_managed_by_iac:
                nacl = self.pseudo_builder.create_default_nacl(vpc.vpc_id, vpc.account, vpc.region)
            return nacl

        vpc.default_nacl = ResourceInvalidator.get_by_logic(get_default_nacl, True, vpc, 'Could not associate default Network ACL')

    @staticmethod
    def _assign_security_group_vpc(security_group: SecurityGroup, vpcs: AliasesDict[Vpc]):
        def get_vpc():
            if security_group.vpc_id is None:
                return next((vpc for vpc in vpcs if vpc.is_default and vpc.region == security_group.region), None)
            else:
                return ResourceInvalidator.get_by_id(vpcs, security_group.vpc_id, True, security_group)

        security_group.vpc = ResourceInvalidator.get_by_logic(get_vpc, True, security_group, 'Could not associate the security group to a VPC')

    @staticmethod
    def _assign_network_acl_rules(nacl: NetworkAcl, network_acl_rules: List[NetworkAclRule]):
        nacl_inbound_rules = ResourceInvalidator.get_by_logic(
            lambda: list({nar for nar in network_acl_rules if nar.network_acl_id in nacl.aliases and nar.rule_type == RuleType.INBOUND}),
            False
        )
        nacl.inbound_rules.extend(nacl_inbound_rules)
        nacl_outbound_rules = ResourceInvalidator.get_by_logic(
            lambda: list({nar for nar in network_acl_rules if nar.network_acl_id in nacl.aliases and nar.rule_type == RuleType.OUTBOUND}),
            False
        )
        nacl.outbound_rules.extend(nacl_outbound_rules)

    @staticmethod
    def _assign_default_network_acl_rules_for_tf(nacl: NetworkAcl, vpcs: AliasesDict[Vpc]):
        nacl_vpc = ResourceInvalidator.get_by_id(vpcs, nacl.vpc_id, True, nacl)
        if nacl_vpc:
            nacl.inbound_rules.append(NetworkAclRule(nacl.region, nacl.account, nacl.network_acl_id, '0.0.0.0/0',
                                                     0, 65535, RuleAction.DENY, 32767, RuleType.INBOUND, IpProtocol('ALL')))
            nacl.outbound_rules.append(NetworkAclRule(nacl.region, nacl.account, nacl.network_acl_id, '0.0.0.0/0',
                                                      0, 65535, RuleAction.DENY, 32767, RuleType.OUTBOUND, IpProtocol('ALL')))
        if nacl_vpc.ipv6_cidr_block and len(nacl_vpc.ipv6_cidr_block) > 0:
            nacl.outbound_rules.append(NetworkAclRule(nacl.region, nacl.account, nacl.network_acl_id, '::/0',
                                                      0, 65535, RuleAction.DENY, 32768, RuleType.OUTBOUND, IpProtocol('ALL')))
            nacl.inbound_rules.append(NetworkAclRule(nacl.region, nacl.account, nacl.network_acl_id, '::/0',
                                                     0, 65535, RuleAction.DENY, 32768, RuleType.INBOUND, IpProtocol('ALL')))

    def _assign_network_interface_subnets(self, network_interface: NetworkInterface, subnets: AliasesDict[Subnet]):
        network_interface.subnet = ResourceInvalidator.get_by_id(subnets, network_interface.subnet_id, True, network_interface)
        if not network_interface.primary_ip_address:
            network_interface.primary_ip_address = network_interface.subnet.cidr_block
        if not network_interface.vpc_id:
            network_interface.vpc_id = network_interface.subnet.vpc_id
            network_interface.vpc = network_interface.subnet.vpc
        if not network_interface.availability_zone:
            network_interface.availability_zone = network_interface.subnet.availability_zone
        if self._should_associate_public_ip(network_interface, network_interface.subnet.map_public_ip_on_launch):
            network_interface.public_ip_address = '0.0.0.0'

    @staticmethod
    def _should_associate_public_ip(network_interface: NetworkInterface, associate_public_ip: bool):
        if isinstance(network_interface.owner, Ec2Instance):
            associate_public_ip = network_interface.owner.raw_data.associate_public_ip_address
        return not network_interface.is_pseudo and associate_public_ip and not network_interface.public_ip_address

    @staticmethod
    def _assign_security_group_rules(security_group: SecurityGroup, security_group_rules: List[SecurityGroupRule]):
        security_group.inbound_permissions.extend(ResourceInvalidator.get_by_logic(
            lambda: [sgr for sgr in security_group_rules
                     if sgr.security_group_id in security_group.aliases
                     and sgr.connection_type == ConnectionType.INBOUND],
            False))
        security_group.outbound_permissions.extend(ResourceInvalidator.get_by_logic(
            lambda: [sgr for sgr in security_group_rules
                     if sgr.security_group_id in security_group.aliases
                     and sgr.connection_type == ConnectionType.OUTBOUND],
            False))

    @staticmethod
    def _assign_network_interface_security_groups(network_interface: NetworkInterface,
                                                  security_groups: AliasesDict[SecurityGroup]):
        if not network_interface.security_groups_ids:
            owner = network_interface.owner
            if not (isinstance(owner, LoadBalancer) and owner.load_balancer_type == LoadBalancerType.NETWORK):
                network_interface.security_groups = [network_interface.vpc.default_security_group]
                network_interface.security_groups_ids = [sg.security_group_id for sg in network_interface.security_groups]
        else:
            for sg_id in network_interface.security_groups_ids:
                network_interface.security_groups.append(ResourceInvalidator.get_by_id(security_groups, sg_id, True, network_interface))

        for security_group in network_interface.security_groups:
            security_group.add_usage(network_interface)

    @staticmethod
    def _assign_transit_gateway_route_tables(transit_gateway: TransitGateway,
                                             route_tables: List[TransitGatewayRouteTable]):
        transit_gateway.route_tables = ResourceInvalidator.get_by_logic(
            lambda: [route_table for route_table in route_tables if route_table.tgw_id == transit_gateway.tgw_id],
            True,
            transit_gateway,
            'Could not associate route tables'
        )

    @staticmethod
    def _assign_transit_gateway_route_table_routes(route_table: TransitGatewayRouteTable,
                                                   routes: List[TransitGatewayRoute]):
        route_table.routes = ResourceInvalidator.get_by_logic(
            lambda: [route for route in routes if route.route_table_id == route_table.route_table_id],
            True,
            route_table,
            'Could not associate routes')

    @staticmethod
    def _assign_transit_gateway_associations_attachments(
            association: TransitGatewayRouteTableAssociation,
            attachments: List[TransitGatewayVpcAttachment]):
        association.attachment = ResourceInvalidator.get_by_id(attachments, association.tgw_attachment_id, True, association)

    @staticmethod
    def _assign_transit_gateway_route_table_associations(route_table: TransitGatewayRouteTable,
                                                         associations: List[TransitGatewayRouteTableAssociation]):
        route_table.associations = ResourceInvalidator.get_by_logic(
            lambda: [x for x in associations if x.tgw_route_table_id == route_table.route_table_id],
            False)

    @staticmethod
    def _assign_transit_gateway_propagation_attachments(propagation: TransitGatewayRouteTablePropagation,
                                                        attachments: List[TransitGatewayVpcAttachment]):
        propagation.attachment = ResourceInvalidator.get_by_id(attachments, propagation.tgw_attachment_id, True, propagation)

    @staticmethod
    def _assign_transit_gateway_propagated_routes(propagation: TransitGatewayRouteTablePropagation,
                                                  routes: List[TransitGatewayRoute], vpcs: AliasesDict[Vpc]):
        if propagation.attachment.resource_type == TransitGatewayResourceType.VPC:
            tgw_vpc = ResourceInvalidator.get_by_id(vpcs, propagation.attachment.resource_id, True, propagation)
            for vpc_cidr in tgw_vpc.cidr_block:
                propagated_route = TransitGatewayRoute(vpc_cidr,
                                                       TransitGatewayRouteState.ACTIVE,
                                                       TransitGatewayRouteType.PROPAGATED,
                                                       propagation.tgw_route_table_id,
                                                       propagation.region,
                                                       propagation.account)
                routes.append(propagated_route)
        else:
            logging.warning(f'The propagation\'s attachment type is {propagation.attachment.resource_type.value} which is not supported.')

    @staticmethod
    def _assign_s3_bucket_region(bucket: S3Bucket, bucket_name_to_region_map: Dict[str, str]):
        if bucket.bucket_name in bucket_name_to_region_map:
            bucket.region = ResourceInvalidator.get_by_logic(
                lambda: bucket_name_to_region_map[bucket.bucket_name],
                True,
                bucket,
                'Could not determine bucket\'s region'
            )

    @staticmethod
    def _assign_s3_bucket_acls(bucket: S3Bucket, acls: List[S3ACL]):
        bucket.acls = ResourceInvalidator.get_by_logic(
            lambda: [acl for acl in acls if acl.bucket_name == bucket.bucket_name],
            False)

    @staticmethod
    def _assign_acls_owner_data(acls: List[S3ACL]):
        for acl in acls:
            if not (acl.owner_id and acl.owner_name):
                owner: Tuple[str, str] = ResourcesAssignerUtil.get_account_owner(acl.account, acls)
                if owner:
                    acl.owner_id = owner[0]
                    acl.owner_name = owner[1]

    @classmethod
    def _assign_s3_access_block_settings(cls, bucket: S3Bucket, access_blocks_list: List[PublicAccessBlockSettings]):
        def get_public_access_block_settings():
            settings = [sett for sett in access_blocks_list if bucket.bucket_name == sett.bucket_name_or_account_id or
                        sett.bucket_name_or_account_id in bucket.aliases]
            if settings:
                public_access_block_settings = settings[0]
            else:
                public_access_block_settings = create_pseudo_access_block(bucket_name_or_account_id=bucket.bucket_name,
                                                                          access_level=PublicAccessBlockLevel.BUCKET,
                                                                          account_id=bucket.account,
                                                                          region=bucket.region)
            public_access_block_settings.account_access_block = ResourcesAssignerUtil.get_account_access_block(bucket.account,
                                                                                                               access_blocks_list,
                                                                                                               bucket.region)
            return public_access_block_settings

        bucket.public_access_block_settings = ResourceInvalidator.get_by_logic(
            get_public_access_block_settings,
            True,
            bucket,
            'Could not associate public access block settings'
        )

    @staticmethod
    def _assign_s3_bucket_access_points(bucket: S3Bucket, access_points: List[S3BucketAccessPoint]):
        bucket.access_points = ResourceInvalidator.get_by_logic(
            lambda: [access_point for access_point in access_points if access_point.bucket_name == bucket.bucket_name],
            False
        )

    @staticmethod
    def _assign_s3_bucket_policy(bucket: S3Bucket, policies: List[S3Policy]):
        bucket.resource_based_policy = ResourceInvalidator.get_by_logic(
            lambda: next((policy for policy in policies
                          if policy.bucket_name in bucket.aliases), bucket.resource_based_policy),
            False
        )

    @staticmethod
    def _update_s3_bucket_policies_canonical(s3_policy: S3Policy, oai_list: List[OriginAccessIdentity]):
        for statement in s3_policy.statements:
            if statement.principal.principal_type == PrincipalType.CANONICAL_USER:
                oai = next((oai for oai in oai_list if oai.s3_canonical_user_id in statement.principal.principal_values), None)
                if oai:
                    statement.principal.principal_type = PrincipalType.AWS
                    for index, value in enumerate(statement.principal.principal_values):
                        if value == oai.s3_canonical_user_id:
                            statement.principal.principal_values[index] = oai.iam_arn

    @staticmethod
    def _assign_s3_access_point_policy(access_point: S3BucketAccessPoint, policies: List[S3AccessPointPolicy]):
        access_point.resource_based_policy = ResourceInvalidator.get_by_logic(
            lambda: next((policy for policy in policies if policy.access_point_name == access_point.name), None),
            False
        )

    @staticmethod
    def _assign_iam_roles_policies_from_iam_policy_attachment(role: Role, policies: List[ManagedPolicy],
                                                              policy_attachments: List[IamPolicyAttachment]):
        def get_role_policies():
            policy_arns = [pra.policy_arn for pra in policy_attachments
                           if pra.roles and role.role_name in pra.roles]
            return [policy for policy in policies if policy.arn in policy_arns]

        role_policies = ResourceInvalidator.get_by_logic(get_role_policies, False)
        if role_policies:
            role.attach_policy_origin_data(role_policies, policy_attachments)

    @staticmethod
    def _assign_iam_assume_role_policies(role: Role, assume_role_policies: List[AssumeRolePolicy]):
        def get_assume_role_policies():
            role_policy = next((policy for policy in assume_role_policies if policy.role_arn in (role.arn, role.qualified_arn)), None)
            return role_policy

        role.assume_role_policy = ResourceInvalidator.get_by_logic(get_assume_role_policies, False)

    @staticmethod
    def _assign_iam_roles_policies(role: Role, policies: List[ManagedPolicy],
                                   policy_role_attachments: List[PolicyRoleAttachment]):
        def get_role_policies():
            policy_arns = [pra.policy_arn for pra in policy_role_attachments if pra.role_name == role.role_name]
            return [policy for policy in policies if policy.arn in policy_arns]

        role_policies = ResourceInvalidator.get_by_logic(get_role_policies, False)
        if role_policies:
            role.attach_policy_origin_data(role_policies, policy_role_attachments)

    @staticmethod
    def _assign_iam_roles_inline_policies(role: Role, role_inline_policies: List[InlinePolicy]):
        role.permissions_policies.extend(ResourceInvalidator.get_by_logic(
            lambda: [policy for policy in role_inline_policies
                     if (policy.owner_name in role.aliases or policy.owner_name == role.role_name) and policy.account == role.account],
            False
        ))

    @staticmethod
    def _assign_iam_users_policies(user: IamUser, policies: List[ManagedPolicy],
                                   policy_user_attachments: List[PolicyUserAttachment]):
        def get_user_policies():
            policy_arns = [pua.policy_arn for pua in policy_user_attachments if pua.user_id == user.name or pua.user_name == user.name]
            return [policy for policy in policies if policy.arn in policy_arns]

        user_policies = ResourceInvalidator.get_by_logic(get_user_policies, False)
        if user_policies:
            user.attach_policy_origin_data(user_policies, policy_user_attachments)

    @staticmethod
    def _assign_iam_users_inline_policies(user: IamUser, user_inline_policy: List[InlinePolicy]):
        user.permissions_policies.extend(ResourceInvalidator.get_by_logic(
            lambda: [policy for policy in user_inline_policy if policy.owner_name == user.name],
            False
        ))

    @staticmethod
    def _assign_iam_users_policies_from_iam_policy_attachment(user: IamUser, policies: List[ManagedPolicy],
                                                              policy_attachments: List[IamPolicyAttachment]):
        def get_user_policies():
            policy_arns = [pra.policy_arn for pra in policy_attachments
                           if any(pra.users for pra in policy_attachments)
                           and any(user.name in pra.users for pra in policy_attachments)]
            return [policy for policy in policies if policy.arn in policy_arns]

        user_policies = ResourceInvalidator.get_by_logic(get_user_policies, False)
        if user_policies:
            user.attach_policy_origin_data(user_policies, policy_attachments)

    @staticmethod
    def _assign_iam_groups_policies(group: IamGroup, policies: List[ManagedPolicy],
                                    policy_group_attachments: List[PolicyGroupAttachment]):
        def get_group_policies():
            policy_arns = [pga.policy_arn for pga in policy_group_attachments if pga.group_id == group.group_id or group.name]
            return [policy for policy in policies if policy.arn in policy_arns]

        group_policies = ResourceInvalidator.get_by_logic(get_group_policies, False)
        if group_policies:
            group.attach_policy_origin_data(group_policies, policy_group_attachments)

    @staticmethod
    def _assign_iam_groups_policies_from_iam_policy_attachment(group: IamGroup, policies: List[ManagedPolicy],
                                                               policy_attachments: List[IamPolicyAttachment]):
        def get_group_policies():
            policy_arns = [pra.policy_arn for pra in policy_attachments
                           if pra.groups and group.name in pra.groups]
            return [policy for policy in policies if policy.arn in policy_arns]

        group_policies = ResourceInvalidator.get_by_logic(get_group_policies, False)
        if group_policies:
            group.attach_policy_origin_data(group_policies, policy_attachments)

    @staticmethod
    def _assign_iam_groups_inline_policies(group: IamGroup, group_inline_policies: List[InlinePolicy]):
        group.permissions_policies.extend(ResourceInvalidator.get_by_logic(
            lambda: [policy for policy in group_inline_policies if policy.owner_name in (group.name, group.group_id)],
            False
        ))

    @staticmethod
    def _assign_iam_group_membership(group_membership: IamGroupMembership, groups: List[IamGroup], users: List[IamUser]):
        group = ResourceInvalidator.get_by_logic(lambda: next(group for group in groups if group_membership.group == group.name
                                                              or group_membership.group == group.group_id),
                                                 True,
                                                 group_membership,
                                                 'Could not find relevant IAM Groups')
        for user in users:
            if user.name in group_membership.users:
                user.groups.append(group)
                user.groups_attach_origin_map.append({group.name: group_membership.origin})

    @staticmethod
    def _assign_iam_user_group_membership(group_membership: IamUserGroupMembership, groups: List[IamGroup],
                                          users: List[IamUser]):
        user = ResourceInvalidator.get_by_logic(
            lambda: next(user for user in users if group_membership.user == user.name),
            True,
            group_membership,
            'Could not find user')
        for group in groups:
            if group.name in group_membership.groups and user.name == group_membership.user:
                user.groups.append(group)
                user.groups_attach_origin_map.append({group.name: group_membership.origin})

    @staticmethod
    def _assign_iam_role_permission_boundary(role: Role, policies: List[ManagedPolicy]):
        if role.permission_boundary_arn:
            role.permission_boundary = ResourceInvalidator.get_by_logic(
                lambda: next(policy for policy in policies if policy.arn == role.permission_boundary_arn),
                True,
                role,
                'Could not find permission boundary policy')

    @staticmethod
    def _assign_iam_user_permission_boundary(user: IamUser, policies: List[ManagedPolicy]):
        if user.permission_boundary_arn:
            user.permission_boundary = ResourceInvalidator.get_by_logic(
                lambda: next(policy for policy in policies if policy.arn == user.permission_boundary_arn),
                True,
                user,
                'Could not find permission boundary policy')

    @staticmethod
    def _assign_route_table_routes(route_table: RouteTable, routes: List[Route], vpcs_map: dict):
        def get_routes():
            rt_routes = []
            for route in routes:
                if route.route_table_id not in route_table.aliases:
                    continue
                route.route_table_id = route_table.route_table_id
                if any(r for r in rt_routes if hash_list(route.get_keys()) == hash_list(r.get_keys())):
                    continue
                rt_routes.append(route)

            return rt_routes

        route_table.routes.extend(ResourceInvalidator.get_by_logic(
            get_routes,
            False
        ))

        if not any(route for route in route_table.routes if route.target == 'local'):
            if vpc := ResourceInvalidator.get_by_id(vpcs_map, route_table.vpc_id, True, route_table):
                for vpc_cidr in vpc.cidr_block:
                    route_table.routes.append(Route(route_table.route_table_id, vpc_cidr, RouteTargetType.GATEWAY_ID, 'local',
                                                    route_table.region, route_table.account))

    @staticmethod
    def _assign_subnet_route_table(subnet: Subnet,
                                   route_tables: AliasesDict[RouteTable],
                                   route_table_association: List[RouteTableAssociation]):
        def get_route_table():
            route_table_id = next((rta.route_table_id for rta in route_table_association if rta.subnet_id == subnet.subnet_id), None)
            if route_table_id:
                return ResourceInvalidator.get_by_id(route_tables, route_table_id, True, subnet)
            else:
                return subnet.vpc.main_route_table

        subnet.route_table = ResourceInvalidator.get_by_logic(get_route_table, True, subnet, 'Could not associate a route table')

    @classmethod
    def _assign_subnet_id_to_nacl(cls, nacl_assoc: NetworkAclAssociation, nacls: AliasesDict[NetworkAcl]):
        nacl = ResourceInvalidator.get_by_id(nacls, nacl_assoc.network_acl_id, False)
        if nacl.subnet_ids is None:
            nacl.subnet_ids = [nacl_assoc.subnet_id]
        elif nacl_assoc.subnet_id not in nacl.subnet_ids:
            nacl.subnet_ids.append(nacl_assoc.subnet_id)

    @classmethod
    def _assign_subnet_network_acl(cls, subnet: Subnet, network_acls: AliasesDict[NetworkAcl]):
        subnet.network_acl = ResourceInvalidator.get_by_logic(
            lambda: next((acl for acl in network_acls if subnet.subnet_id in acl.subnet_ids), None) or subnet.vpc.default_nacl,
            True,
            subnet,
            'Could not associate Network ACL'
        )

    @staticmethod
    def _assign_subnet_vpc(subnet: Subnet, vpcs: AliasesDict[Vpc]):
        subnet.vpc = ResourceInvalidator.get_by_id(vpcs, subnet.vpc_id, True, subnet)

    def _assign_ec2_network_interfaces(self, ec2: Ec2Instance, network_interfaces: AliasesDict[NetworkInterface],
                                       subnets: AliasesDict[Subnet], vpcs: AliasesDict[Vpc]):
        ec2.network_resource.network_interfaces = ResourceInvalidator.get_by_logic(
            lambda: [eni for eni in network_interfaces if eni.eni_id in ec2.network_interfaces_ids],
            False
        )

        if not ec2.network_resource.network_interfaces and ec2.is_managed_by_iac:
            self.pseudo_builder.create_ec2_network_interface(ec2, subnets, vpcs)

        for eni in ec2.network_resource.network_interfaces:
            eni.owner = ec2

    @staticmethod
    def _assign_ec2_role_permissions(ec2: Ec2Instance, roles: AliasesDict[Role], iam_instance_profiles: AliasesDict[IamInstanceProfile]):
        if ec2.iam_profile_name:
            def get_matching_role():
                profile: IamInstanceProfile = iam_instance_profiles.get(ec2.iam_profile_name)
                return profile and roles.get(profile.role_name)
            ec2.iam_role = ResourceInvalidator.get_by_logic(get_matching_role, True, ec2, 'Unable to find matching IAM instance profile')

    @staticmethod
    def _assign_load_balancer_target_ec2_instance(target: LoadBalancerTarget, ec2s: List[Ec2Instance]):
        def get_target_instance():
            ec2_target = next((ec2 for ec2 in ec2s if target.target_id == ec2.instance_id), None)
            if ec2_target:
                return ec2_target
            else:
                return next((ec2 for ec2 in ec2s for eni in ec2.network_resource.network_interfaces if
                             target.target_id in eni.all_ip_addresses), None)

        target.target_instance = ResourceInvalidator.get_by_logic(
            get_target_instance,
            False
        )

    @staticmethod
    def _assign_load_balancer_target_group_targets(target_group: LoadBalancerTargetGroup,
                                                   targets: List[LoadBalancerTarget]):
        target_group.targets = ResourceInvalidator.get_by_logic(
            lambda: [target for target in targets if target.target_group_arn == target_group.target_group_arn],
            False  ### TODO: Should we invalidate the target group???
        )

    @staticmethod
    def _assign_load_balancer_attributes(load_balancer: LoadBalancer, load_balancers_attributes: List[LoadBalancerAttributes]):
        def get_attributes():
            attributes_data = next((attr for attr in load_balancers_attributes if attr.load_balancer_arn == load_balancer.load_balancer_arn), None)
            return attributes_data

        load_balancer.load_balancer_attributes = ResourceInvalidator.get_by_logic(get_attributes, False)

    @staticmethod
    def _assign_load_balancer_target_groups(load_balancer: LoadBalancer,
                                            target_groups: List[LoadBalancerTargetGroup],
                                            load_balancer_target_group_associations: List[LoadBalancerTargetGroupAssociation]):
        def get_target_groups():
            associations = [tga for tga in load_balancer_target_group_associations if tga.load_balancer_arn in load_balancer.aliases]
            target_groups_arns = flat_list([tga.target_group_arns for tga in associations])
            return [tg for tg in target_groups if any(alias in target_groups_arns for alias in tg.aliases)]

        load_balancer.target_groups = ResourceInvalidator.get_by_logic(get_target_groups, False)  ### TODO: Should we invalidate load balancer???

    @staticmethod
    def _assign_load_balancer_listener_ports(load_balancer: LoadBalancer, load_balancer_listeners: List[LoadBalancerListener]):
        def get_listener_ports():
            listeners = [listener for listener in load_balancer_listeners if listener.load_balancer_arn in load_balancer.aliases]
            return [listener.listener_port for listener in listeners]

        ### TODO: Should we invalidate load balancer???
        load_balancer.listener_ports.extend(ResourceInvalidator.get_by_logic(get_listener_ports, False))

    def _assign_load_balancer_network_interfaces(self,
                                                 load_balancer: LoadBalancer,
                                                 network_interfaces: AliasesDict[NetworkInterface],
                                                 subnets: AliasesDict[Subnet],
                                                 elastic_ips: List[ElasticIp]):
        def get_enis():
            elb_resource_name = get_arn_resource(load_balancer.load_balancer_arn)
            # Only way to associate an ELB ENI is by the ENI description
            return [eni for eni in network_interfaces if eni.description == f'ELB {elb_resource_name}']

        load_balancer_network_interfaces = ResourceInvalidator.get_by_logic(get_enis, False)
        for eni in load_balancer_network_interfaces:
            load_balancer.network_resource.add_interface(eni)
            eni.owner = load_balancer

        self.pseudo_builder.create_load_balancer_network_interfaces(load_balancer, subnets, elastic_ips)

    @staticmethod
    def _remove_deleted_auto_scale_ec2s(ec2s: List[Ec2Instance], auto_scaling_groups: List[AutoScalingGroup]):
        auto_scaling_groups_ids = [asg.name for asg in auto_scaling_groups]
        deleted_ec2s = []
        for ec2 in ec2s:
            auto_scale_group_id = ec2.tags.get('aws:autoscaling:groupName')
            if auto_scale_group_id and auto_scale_group_id not in auto_scaling_groups_ids:
                deleted_ec2s.append(ec2)
        for ec2 in deleted_ec2s:
            ec2s.remove(ec2)

    def _add_auto_scale_ec2s(self,
                             auto_scaling_group: AutoScalingGroup,
                             load_balancers: List[LoadBalancer],
                             load_balancer_target_groups: List[LoadBalancerTargetGroup],
                             ec2s: List[Ec2Instance],
                             subnets: AliasesDict[Subnet],
                             vpcs: AliasesDict[Vpc]):

        if auto_scaling_group.launch_configuration:
            self._add_auto_scale_ec2s_by_launch_configuration(auto_scaling_group=auto_scaling_group,
                                                              load_balancers=load_balancers,
                                                              load_balancer_target_groups=load_balancer_target_groups,
                                                              ec2s=ec2s,
                                                              subnets=subnets,
                                                              vpcs=vpcs)
        elif auto_scaling_group.launch_template:
            self._add_auto_scale_ec2s_by_launch_template(auto_scaling_group=auto_scaling_group,
                                                         load_balancers=load_balancers,
                                                         load_balancer_target_groups=load_balancer_target_groups,
                                                         ec2s=ec2s,
                                                         subnets=subnets)

    def _add_auto_scale_ec2s_by_launch_configuration(self,
                                                     auto_scaling_group: AutoScalingGroup,
                                                     load_balancers: List[LoadBalancer],
                                                     load_balancer_target_groups: List[LoadBalancerTargetGroup],
                                                     ec2s: List[Ec2Instance],
                                                     subnets: AliasesDict[Subnet],
                                                     vpcs: AliasesDict[Vpc]):

        if launch_configuration := auto_scaling_group.launch_configuration:
            security_group_ids = launch_configuration.security_group_ids
            image_id = launch_configuration.image_id
            instance_type = launch_configuration.instance_type
            ebs_optimized = launch_configuration.ebs_optimized
            monitoring = launch_configuration.monitoring_enabled
            iam_instance_profile = launch_configuration.iam_instance_profile
            subnet_ids = self._get_autoscaling_group_subnets(auto_scaling_group=auto_scaling_group, subnets=subnets)

            pseudo_ec2s: List[Ec2Instance] = self._create_pseudo_autoscaling_group_ec2_list(auto_scaling_group=auto_scaling_group,
                                                                                            subnet_ids=subnet_ids,
                                                                                            ec2s=ec2s,
                                                                                            subnets=subnets,
                                                                                            image_id=image_id,
                                                                                            security_group_ids=security_group_ids,
                                                                                            iam_instance_profile=iam_instance_profile,
                                                                                            instance_type=instance_type,
                                                                                            ebs_optimized=ebs_optimized,
                                                                                            monitoring=monitoring)

            for pseudo_ec2 in pseudo_ec2s:
                self.pseudo_builder.create_ec2_network_interface(pseudo_ec2, subnets, vpcs, launch_configuration)

            self._attach_load_balancer_to_auto_scaling_group(auto_scaling_group=auto_scaling_group,
                                                             load_balancers=load_balancers,
                                                             load_balancer_target_groups=load_balancer_target_groups,
                                                             ec2s=pseudo_ec2s)

    def _add_auto_scale_ec2s_by_launch_template(self,
                                                auto_scaling_group: AutoScalingGroup,
                                                load_balancers: List[LoadBalancer],
                                                load_balancer_target_groups: List[LoadBalancerTargetGroup],
                                                ec2s: List[Ec2Instance],
                                                subnets: AliasesDict[Subnet]):

        security_group_ids: List[str] = []
        if launch_template := auto_scaling_group.launch_template:
            if launch_template.security_group_ids:
                security_group_ids = launch_template.security_group_ids
            image_id = launch_template.image_id
            instance_type = launch_template.instance_type
            ebs_optimized = launch_template.ebs_optimized
            monitoring = launch_template.monitoring_enabled
            iam_instance_profile = launch_template.iam_instance_profile
            subnet_ids = self._get_autoscaling_group_subnets(auto_scaling_group=auto_scaling_group, subnets=subnets)

            if not subnet_ids and \
                    launch_template.network_configurations:
                subnet_ids = list({subnet_id for net_conf in launch_template.network_configurations
                                   for subnet_id in net_conf.subnet_list_ids})

            pseudo_ec2s: List[Ec2Instance] = []
            for subnet_id in subnet_ids:
                pseudo_ec2: Ec2Instance = self._create_pseudo_autoscaling_group_ec2(auto_scaling_group=auto_scaling_group,
                                                                                    subnet_id=subnet_id,
                                                                                    ec2s=ec2s,
                                                                                    subnets=subnets,
                                                                                    image_id=image_id,
                                                                                    security_group_ids=security_group_ids,
                                                                                    iam_instance_profile=iam_instance_profile,
                                                                                    instance_type=instance_type,
                                                                                    ebs_optimized=ebs_optimized,
                                                                                    monitoring=monitoring)
                if pseudo_ec2:
                    subnet: Subnet = ResourceInvalidator.get_by_id(subnets, pseudo_ec2.raw_data.subnet_id, True, pseudo_ec2)
                    if auto_scaling_group.launch_template.network_configurations:
                        for net_conf in auto_scaling_group.launch_template.network_configurations:
                            assign_public_ip = len(auto_scaling_group.launch_template.network_configurations) == 1 and \
                                               (net_conf.assign_public_ip or (net_conf.assign_public_ip is None and subnet.map_public_ip_on_launch))
                            security_groups = launch_template.security_groups or net_conf.security_groups or\
                                              [self.pseudo_builder.create_security_group(
                                                  subnet.vpc, True, launch_template.account, launch_template.region)]
                            self.pseudo_builder.create_eni(pseudo_ec2, subnet, [x.security_group_id for x in security_groups],
                                                           assign_public_ip, None, None, f'Eni for ASG {auto_scaling_group.name}', False)
                    else:
                        security_groups = (launch_template.security_groups or
                                           [self.pseudo_builder.create_security_group(subnet.vpc,
                                                                                      True,
                                                                                      launch_template.account,
                                                                                      launch_template.region)])
                        self.pseudo_builder.create_eni(pseudo_ec2, subnet, [x.security_group_id for x in security_groups],
                                                       subnet.map_public_ip_on_launch, None, None, f'Eni for ASG {auto_scaling_group.name}', False)
                    pseudo_ec2s.append(pseudo_ec2)

            self._attach_load_balancer_to_auto_scaling_group(auto_scaling_group=auto_scaling_group,
                                                             load_balancers=load_balancers,
                                                             load_balancer_target_groups=load_balancer_target_groups,
                                                             ec2s=pseudo_ec2s)

    def _create_pseudo_autoscaling_group_ec2_list(self,
                                                  auto_scaling_group: AutoScalingGroup,
                                                  subnet_ids: List[str],
                                                  ec2s: List[Ec2Instance],
                                                  subnets: AliasesDict[Subnet],
                                                  image_id: str,
                                                  security_group_ids: List[str],
                                                  iam_instance_profile: str,
                                                  instance_type: str, monitoring: bool, ebs_optimized: bool) -> List[Ec2Instance]:

        pseudo_ec2s: List[Ec2Instance] = []
        for subnet_id in subnet_ids:
            pseudo_ec2: Ec2Instance = self._create_pseudo_autoscaling_group_ec2(auto_scaling_group=auto_scaling_group,
                                                                                subnet_id=subnet_id,
                                                                                ec2s=ec2s,
                                                                                subnets=subnets,
                                                                                image_id=image_id,
                                                                                security_group_ids=security_group_ids,
                                                                                iam_instance_profile=iam_instance_profile,
                                                                                instance_type=instance_type,
                                                                                monitoring=monitoring,
                                                                                ebs_optimized=ebs_optimized)
            if pseudo_ec2:
                pseudo_ec2s.append(pseudo_ec2)
        return pseudo_ec2s

    def _create_pseudo_autoscaling_group_ec2(self,
                                             auto_scaling_group: AutoScalingGroup,
                                             subnet_id: str,
                                             ec2s: List[Ec2Instance],
                                             subnets: AliasesDict[Subnet],
                                             image_id: str,
                                             security_group_ids: List[str],
                                             iam_instance_profile: str,
                                             instance_type: str, monitoring: bool, ebs_optimized: bool) -> Optional[Ec2Instance]:

        ec2_in_group = any(ec2 for ec2 in ec2s
                           if ec2.tags.get('aws:autoscaling:groupName') == auto_scaling_group.name
                           and subnet_id in ec2.network_resource.subnet_ids)

        subnet = ResourceInvalidator.get_by_id(subnets, subnet_id, False)
        assign_public_ip = self._get_assign_public_ip_for_asg_data(subnet, auto_scaling_group)

        if auto_scaling_group.launch_template and auto_scaling_group.launch_template.network_configurations:
            for net_conf in auto_scaling_group.launch_template.network_configurations:
                if subnet.subnet_id in net_conf.subnet_list_ids and net_conf.assign_public_ip is None:
                    net_conf.assign_public_ip = assign_public_ip

        if subnet and not ec2_in_group:
            subnet_identifier = f'subnet-{subnet.name}' if subnet.name else subnet.subnet_id
            name = f'{auto_scaling_group.name}-pseudo-instance-{subnet_identifier}'
            tags = {'aws:autoscaling:groupName': auto_scaling_group.name}
            return self.pseudo_builder.create_ec2(subnet, image_id, security_group_ids, instance_type, monitoring, ebs_optimized,
                                            name, iam_instance_profile, tags, assign_public_ip)
        return None

    @staticmethod
    def _get_assign_public_ip_for_asg_data(subnet: Subnet, auto_scaling_group: AutoScalingGroup) -> Optional[bool]:
        if subnet:
            if auto_scaling_group.is_managed_by_iac and subnet.vpc.is_default:
                return subnet.map_public_ip_on_launch
            elif (auto_scaling_group and auto_scaling_group.launch_template and
                auto_scaling_group.launch_template.network_configurations and
                len(auto_scaling_group.launch_template.network_configurations) == 1 and
                auto_scaling_group.launch_template.network_configurations[0].assign_public_ip is not None):
                # "You cannot auto-assign a public IP address if you specify more than one network interface"
                # source: https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-template.html
                return auto_scaling_group.launch_template.network_configurations[0].assign_public_ip
            elif auto_scaling_group.launch_configuration and auto_scaling_group.launch_configuration.associate_public_ip_address is not None:
                return auto_scaling_group.launch_configuration.associate_public_ip_address
            else:
                return subnet.map_public_ip_on_launch
        return None

    @staticmethod
    def _get_autoscaling_group_subnets(auto_scaling_group: AutoScalingGroup,
                                       subnets: AliasesDict[Subnet]) -> List[str]:
        subnet_ids = auto_scaling_group.subnet_ids
        if not subnet_ids and auto_scaling_group.availability_zones:
            return [subnet.subnet_id for subnet in subnets
                    if subnet.is_default and subnet.availability_zone in auto_scaling_group.availability_zones]
        return subnet_ids

    def _attach_load_balancer_to_auto_scaling_group(self, auto_scaling_group: AutoScalingGroup,
                                                    load_balancers: List[LoadBalancer],
                                                    load_balancer_target_groups: List[LoadBalancerTargetGroup],
                                                    ec2s: List[Ec2Instance]):
        matched_target_groups = [tg for tg in load_balancer_target_groups if tg.target_group_arn in auto_scaling_group.target_group_arns]
        matched_load_balancers = [lb for lb in load_balancers if set(matched_target_groups) & set(lb.target_groups)]

        if matched_load_balancers:
            self.pseudo_builder.create_load_balancer_targets_from_ec2s(matched_target_groups, ec2s)

    @staticmethod
    def _assign_route_vpc_peering(route: Route, peering_connections: List[PeeringConnection]):
        if route.target_type == RouteTargetType.VPC_PEERING_ID:
            route.peering_connection = ResourceInvalidator.get_by_id(peering_connections, route.target, True, route)

    def _assign_ecs_host_eni(self,
                             ecs_instance: Union[EcsTarget, EcsService],
                             subnets: AliasesDict[Subnet]) -> None:
        self._assign_network_configuration_to_eni(ecs_instance, ecs_instance.get_all_network_configurations(), subnets)

    def _assign_redshift_subnets(self,
                                 redshift: RedshiftCluster,
                                 redshift_subnet_groups: List[RedshiftSubnetGroup],
                                 subnets: AliasesDict[Subnet],
                                 accounts: List[Account],
                                 vpcs: AliasesDict[Vpc]):
        if redshift.subnet_group_name is None:
            account = ResourceInvalidator.get_by_id(accounts, redshift.account, False)
            if account and not account.supports_ec2_classic_mode:
                default_subnet_group_name = 'default'
                redshift.subnet_group_name = default_subnet_group_name

                if not any(group.name == default_subnet_group_name and group.region == redshift.region for group in redshift_subnet_groups):
                    default_vpc = ResourceInvalidator.get_by_logic(
                        lambda: ResourcesAssignerUtil.get_default_vpc(vpcs, redshift.account, redshift.region),
                        True,
                        redshift,
                        f'Could not find default vpc in the region {redshift.region} for account {redshift.account}')
                    subnet_list = ResourceInvalidator.get_by_logic(
                        lambda: [subnet.subnet_id for subnet in subnets if subnet.vpc_id == default_vpc.vpc_id],
                        True,
                        redshift,
                        'Could not associate any subnet')
                    subnet_group = RedshiftSubnetGroup(default_subnet_group_name, subnet_list, redshift.region, redshift.account)
                    redshift_subnet_groups.append(subnet_group)

        if redshift.is_ec2_vpc_platform:
            redshift.network_configuration.subnet_list_ids = ResourceInvalidator.get_by_logic(
                lambda: next(x.subnet_ids for x in redshift_subnet_groups if x.name == redshift.subnet_group_name and x.region == redshift.region),
                True,
                redshift,
                'Could not find any subnet group')
            self._assign_network_configuration_to_eni(redshift, redshift.get_all_network_configurations(), subnets)

    @staticmethod
    def _assign_redshift_logs(redshift_cluster: RedshiftCluster, redshift_logs: List[RedshiftLogging]):
        def get_logs():
            logs = next((logs for logs in redshift_logs if logs.cluster_identifier == redshift_cluster.name), None)
            return logs

        redshift_cluster.logs_config = ResourceInvalidator.get_by_logic(get_logs, False)

    @staticmethod
    def _assign_task_definition_to_ecs_instance(ecs_task_definition: EcsTaskDefinition, ecs_cluster_list: List[EcsCluster]) -> None:
        for cluster in ecs_cluster_list:
            for ecs_instance in cluster.get_all_ecs_instances():
                if ecs_instance.get_task_definition_arn() == ecs_task_definition.get_arn():
                    ecs_instance.set_task_definition(ecs_task_definition)
                    break

    @staticmethod
    def _assign_iam_role_to_task_definition(cluster: EcsCluster, role_by_arn_map: Dict[str, Role]) -> None:
        for ecs_instance in cluster.get_all_ecs_instances():
            task_definition = ecs_instance.get_task_definition()
            if task_definition:
                task_role_arn = ecs_instance.get_task_definition().task_role_arn
                if task_role_arn:
                    ecs_instance.iam_role = ResourceInvalidator.get_by_id(role_by_arn_map, task_role_arn, False)

    @staticmethod
    def _assign_ecs_service_to_cluster(cluster: EcsCluster, ecs_service_list: List[EcsService]) -> None:
        cluster.add_services(ResourceInvalidator.get_by_logic(
            lambda: [service for service in ecs_service_list if service.cluster_arn in cluster.aliases],
            False  ### TODO: Should invalidate???
        ))

    @staticmethod
    def _assign_cloud_watch_event_target_to_cluster(cluster: EcsCluster, event_target_list: List[CloudWatchEventTarget]) -> None:
        cluster.add_events_targets(ResourceInvalidator.get_by_logic(
            lambda: [event_target for event_target in event_target_list if event_target.cluster_arn in cluster.aliases],
            False
        ))

    def _assign_rds_instance_subnets(self,
                                     rds_instance: RdsInstance,
                                     rds_clusters: List[RdsCluster],
                                     vpcs: AliasesDict[Vpc],
                                     db_subnet_groups: List[DbSubnetGroup],
                                     subnets: AliasesDict[Subnet]):
        if rds_instance.is_in_default_vpc:
            default_vpc = ResourceInvalidator.get_by_logic(
                lambda: ResourcesAssignerUtil.get_default_vpc(vpcs, rds_instance.account, rds_instance.region),
                True,
                rds_instance,
                f'{rds_instance.get_type()} should be deployed in default VPC, but the default VPC was '
                f'not found for region {rds_instance.region} on account {rds_instance.account}'
            )
            rds_instance.network_configuration.subnet_list_ids = ResourceInvalidator.get_by_logic(
                lambda: [subnet.subnet_id for subnet in subnets if subnet.vpc_id == default_vpc.vpc_id],
                True,
                rds_instance,
                'Could not associate any subnet')
        else:
            rds_instance.network_configuration.subnet_list_ids = ResourceInvalidator.get_by_logic(
                lambda: next(x.subnet_ids for x in db_subnet_groups if x.name == rds_instance.db_subnet_group_name),
                True,
                rds_instance,
                'Could not associate any subnet')

        if rds_instance.db_cluster_id and not rds_instance.network_configuration.security_groups_ids:
            rds_cluster = ResourceInvalidator.get_by_id(rds_clusters, rds_instance.db_cluster_id, True, rds_instance)
            rds_instance.network_configuration.security_groups_ids = rds_cluster.security_group_ids

        self._assign_network_configuration_to_eni(rds_instance, rds_instance.get_all_network_configurations(), subnets)

    def _assign_neptune_instance_subnets(self,
                                         neptune_instance: NeptuneInstance,
                                         db_subnet_groups: List[DbSubnetGroup],
                                         subnets: AliasesDict[Subnet]):

        neptune_instance.network_configuration.subnet_list_ids = ResourceInvalidator.get_by_logic(
            lambda: next((x.subnet_ids for x in db_subnet_groups if x.name == neptune_instance.neptune_subnet_group_name), None),
            True,
            neptune_instance,
            'Could not associate any subnet')

        self._assign_network_configuration_to_eni(neptune_instance, neptune_instance.get_all_network_configurations(), subnets,
                                                  neptune_instance.is_in_default_vpc)

    def _assign_elastic_search_domain_subnets(self,
                                              elastic_search_domain: ElasticSearchDomain,
                                              subnets: AliasesDict[Subnet]):
        if elastic_search_domain.is_in_vpc:
            self._assign_network_configuration_to_eni(elastic_search_domain, elastic_search_domain.get_all_network_configurations(), subnets)

    def _assign_eks_cluster_eni(self,
                                eks_cluster: EksCluster,
                                subnets: AliasesDict[Subnet],
                                security_groups: AliasesDict[SecurityGroup]):
        self._assign_network_configuration_to_eni(eks_cluster, eks_cluster.get_all_network_configurations(), subnets, False)

        if eks_cluster.is_managed_by_iac and eks_cluster.cluster_security_group_id is None:
            security_group = self.pseudo_builder.create_security_group(eks_cluster.network_resource.vpc, False,
                                                                       eks_cluster.account, eks_cluster.region)
            security_groups.update(security_group)
            eks_cluster.cluster_security_group_id = security_group.security_group_id
            for eni in eks_cluster.network_resource.network_interfaces:
                eni.security_groups_ids.append(security_group.security_group_id)

    @staticmethod
    def _assign_rds_instances_to_cluster(rds_cluster: RdsCluster, rds_instances: List[RdsInstance]):
        rds_cluster.cluster_instances = ResourceInvalidator.get_by_logic(
            lambda: [ins for ins in rds_instances if ins.db_cluster_id == rds_cluster.cluster_id],
            False
        )

    @staticmethod
    def _assign_rds_instance_missing_data_from_cluster(rds_instance: RdsInstance, rds_clusters: List[RdsCluster]):
        rds_cluster: RdsCluster = ResourceInvalidator.get_by_logic(
            lambda: next((cluster for cluster in rds_clusters if rds_instance.db_cluster_id == cluster.cluster_id), None),
            False
        )
        if rds_cluster:
            rds_instance.iam_database_authentication_enabled = rds_cluster.iam_database_authentication_enabled
            rds_instance.backup_retention_period = rds_cluster.backup_retention_period

    @staticmethod
    def _assign_rds_cluster_default_security_group(rds_cluster: RdsCluster):
        if rds_cluster.cluster_instances and not rds_cluster.security_group_ids:
            rds_cluster.security_group_ids.append(rds_cluster.cluster_instances[0].network_resource.vpc.default_security_group.security_group_id)

    @staticmethod
    def _assign_rds_global_cluster_encrypted_at_rest(rds_global_cluster: RdsGlobalCluster, rds_clusters: List[RdsCluster]):
        def encrypt_at_rest():
            if rds_global_cluster.encrypted_at_rest is False:
                if rds_global_cluster.raw_data.source_id is not None:
                    if len(rds_clusters) > 0:
                        for rds_cluster in rds_clusters:
                            return rds_cluster.arn == rds_global_cluster.raw_data.source_id and rds_cluster.encrypted_at_rest
            elif rds_global_cluster.encrypted_at_rest is None:
                if rds_global_cluster.raw_data.source_id is None:
                    return False
                else:
                    if len(rds_clusters) > 0:
                        for rds_cluster in rds_clusters:
                            if rds_cluster.arn == rds_global_cluster.raw_data.source_id and rds_cluster.encrypted_at_rest:
                                return True
            elif rds_global_cluster.encrypted_at_rest:
                return True

            return False

        rds_global_cluster.encrypted_at_rest = ResourceInvalidator.get_by_logic(encrypt_at_rest,
                                                                                True,
                                                                                rds_global_cluster,
                                                                                'Unable to assess encrypted_at_rest')

    @staticmethod
    def _assign_peering_connection_vpc_cidrs(peering_connection: PeeringConnection, vpcs: AliasesDict[Vpc]):
        for vpc_info in [peering_connection.accepter_vpc_info, peering_connection.requester_vpc_info]:
            if not vpc_info.cidr_blocks:
                if vpc := ResourceInvalidator.get_by_id(vpcs, vpc_info.vpc_id, False):
                    vpc_info.cidr_blocks = vpc.cidr_block

    def _assign_network_configuration_to_eni(self, entity: NetworkEntity, network_conf_list: List[NetworkConfiguration],
                                             subnets: AliasesDict[Subnet], assign_default_security_group: bool = True) -> None:
        net_conf_to_subnet = ResourceInvalidator.get_by_logic(
            lambda: [(net_conf, subnet)
                     for net_conf in network_conf_list
                     for subnet_id in net_conf.subnet_list_ids
                     if (subnet := ResourceInvalidator.get_by_id(subnets, subnet_id, False))],
            True,
            entity,
            'Could not associate subnets'
        )

        for net_conf, subnet in net_conf_to_subnet:
            self.pseudo_builder.create_eni(entity, subnet, net_conf.security_groups_ids,
                                           net_conf.assign_public_ip or subnet.map_public_ip_on_launch, None, None, '',
                                           assign_default_security_group)

    @staticmethod
    def _find_default_vpc_security_group(vpc_aliases: Set[str], security_groups: AliasesDict[SecurityGroup]) -> Optional[SecurityGroup]:
        for security_group in security_groups:
            if security_group.vpc_id in vpc_aliases and security_group.is_default:
                return security_group
        return None

    def _assign_nat_gateways_eni_list(self, nat_gw: NatGateways, network_interfaces: AliasesDict[NetworkInterface],
                                      subnets: Dict[str, Subnet]):
        if eni := ResourceInvalidator.get_by_id(network_interfaces, nat_gw.eni_id, False):
            nat_gw.network_resource.network_interfaces.append(eni)
            eni.owner = nat_gw
        else:
            subnet = ResourceInvalidator.get_by_id(subnets, nat_gw.subnet_id, False)
            if subnet and nat_gw.is_managed_by_iac:
                private_ip_address = nat_gw.private_ip or ResourcesAssignerUtil.get_random_ip_in_subnet(subnet.cidr_block)
                self.pseudo_builder.create_eni(nat_gw, subnet, [], True, private_ip_address, nat_gw.public_ip, 'pseudo NAT Gateways eni')
                if not nat_gw.private_ip:
                    nat_gw.private_ip = private_ip_address
            else:
                nat_gw.add_invalidation('Could not associate a network interface')

    @staticmethod
    def _assign_vpc_subnets(vpc: Vpc, subnet_list: List[Subnet]) -> None:
        vpc_subnets = ResourceInvalidator.get_by_logic(
            lambda: [subnet for subnet in subnet_list if subnet.vpc_id in vpc.aliases],
            False
        )

        for subnet in vpc_subnets:
            if subnet.availability_zone not in vpc.subnets_by_az_map:
                vpc.subnets_by_az_map[subnet.availability_zone] = []
            vpc.subnets_by_az_map[subnet.availability_zone].append(subnet)

    @staticmethod
    def _assign_method_settings_to_api_gateway(rest_api_gw: RestApiGw, rest_api_methods: List[ApiGatewayMethodSettings]):
        rest_api_gw.method_settings = ResourceInvalidator.get_by_logic(
            lambda: next((method for method in rest_api_methods if rest_api_gw.rest_api_gw_id in method.api_gw_id), None),
            False)

    @staticmethod
    def _assign_auto_scaling_group_launch_template(auto_scaling_group: AutoScalingGroup, launch_templates: List[LaunchTemplate]):
        def get_launch_template():
            launch_template_data = auto_scaling_group.raw_data.launch_template_data
            if launch_template_data:
                templates = [lt for lt in launch_templates
                             if launch_template_data.template_id == lt.template_id
                             or launch_template_data.template_name == lt.name]
                if launch_template_data.version == '$Latest':
                    return max(templates, key=lambda x: x.version_number)
                else:
                    # If we dont have cloudmapper data and the auto_scaling_group is using an older version and not the latest,
                    # then we wont actually know what is the launch_template is should use, so we do not assign any launch_template to it.
                    return next((t for t in templates if str(t.version_number) == str(launch_template_data.version)), None)
            return None

        auto_scaling_group.launch_template = ResourceInvalidator.get_by_logic(get_launch_template, False)

    @staticmethod
    def _assign_launch_template_network(launch_template: LaunchTemplate, security_groups: AliasesDict[SecurityGroup],
                                        subnets: AliasesDict[Subnet]):
        for net_conf in launch_template.network_configurations:
            for sg_id in net_conf.security_groups_ids:
                net_conf.security_groups.append(ResourceInvalidator.get_by_id(security_groups, sg_id, True, launch_template))
            for subnet_id in net_conf.subnet_list_ids:
                net_conf.subnets.append(ResourceInvalidator.get_by_id(subnets, subnet_id, True, launch_template))

    @staticmethod
    def _assign_auto_scaling_group_launch_configuration(auto_scaling_group: AutoScalingGroup, launch_configurations: List[LaunchConfiguration]):
        def get_launch_configuration():
            if auto_scaling_group.raw_data.launch_configuration_name:
                return next((lc for lc in launch_configurations if lc.name == auto_scaling_group.raw_data.launch_configuration_name
                             and lc.account == auto_scaling_group.account and lc.region == auto_scaling_group.region), None)
            return None

        auto_scaling_group.launch_configuration = ResourceInvalidator.get_by_logic(get_launch_configuration, False)

    @staticmethod
    def _assign_launch_template_security_groups(launch_template: LaunchTemplate,
                                                security_groups: AliasesDict[SecurityGroup]):
        if launch_template.security_group_ids:
            security_groups = [ResourceInvalidator.get_by_id(security_groups, sg_id, True, launch_template)
                               for sg_id in launch_template.security_group_ids]
            launch_template.security_groups.extend(security_groups)

    @staticmethod
    def _assign_ec2_images_data(ec2: Ec2Instance, images: List[Ec2Image]):
        image = ResourceInvalidator.get_by_id(images, ec2.image_id, False)
        if image is None:
            # We generate images on the fly, and assume they are public images.
            # We do this because today we don't load the public images at all, so if we didn't find an image,
            # we assume it's a public one
            if ec2.image_id.startswith('ami-'):
                image = Ec2Image(image_id=ec2.image_id, is_public=True, region=ec2.region, account=ec2.account)
                images.append(image)
            else:
                logging.error(f'The image {ec2.image_id}, was not parsed correctly before, and should have been included already')
        ec2.image_data = image

    @staticmethod
    def _assign_encryption_data_to_s3_bucket(s3_bucket: S3Bucket, encryption_data: List[S3BucketEncryption]):
        def get_encryption_data():
            encryption_data_to_add = next((data for data in encryption_data if s3_bucket.bucket_name == data.bucket_name), None)
            if encryption_data_to_add is None:
                encryption_data_to_add = S3BucketEncryption(bucket_name=s3_bucket.bucket_name, encrypted=False,
                                                            region=s3_bucket.region, account=s3_bucket.account)
                encryption_data.append(encryption_data_to_add)
            return encryption_data_to_add

        s3_bucket.encryption_data = ResourceInvalidator.get_by_logic(get_encryption_data, False)

    @staticmethod
    def _assign_versioning_data_to_s3_bucket(s3_bucket: S3Bucket, versioning_data: List[S3BucketVersioning]):
        def get_versioning_data():
            versioning_data_to_add = next((data for data in versioning_data if s3_bucket.bucket_name == data.bucket_name), None)
            if versioning_data_to_add is None:
                versioning_data_to_add = S3BucketVersioning(bucket_name=s3_bucket.bucket_name, versioning=False,
                                                            region=s3_bucket.region, account=s3_bucket.account)
                versioning_data.append(versioning_data_to_add)
            return versioning_data_to_add

        s3_bucket.versioning_data = ResourceInvalidator.get_by_logic(get_versioning_data, False)

    @staticmethod
    def _get_encryption_key_from_alias(encryption_key: str, region: str, account: str, kms_aliases: List[KmsAlias]):
        kms_alias = next((alias for alias in kms_aliases if alias.alias_name == encryption_key), None)
        if kms_alias:
            return build_arn('kms', region, account,'key', None, kms_alias.target_key_id)
        return None

    @staticmethod
    def _is_kms_alias(kms_key: str) -> bool:
        return 'alias' in kms_key and not is_valid_arn(kms_key)

    def _assign_kms_key_from_alias_to_codebuild_project(self, codebuild: CodeBuildProject, kms_aliases: List[KmsAlias]):
        if codebuild.origin == EntityOrigin.CLOUDFORMATION and self._is_kms_alias(codebuild.encryption_key):
            codebuild.encryption_key = self._get_encryption_key_from_alias(codebuild.encryption_key,
                                                                           codebuild.region,
                                                                           codebuild.account,
                                                                           kms_aliases)

    def _assign_kms_key_from_alias_to_codebuild_report_group(self, codebuild: CodeBuildReportGroup, kms_aliases: List[KmsAlias]):
        if codebuild.origin == EntityOrigin.CLOUDFORMATION and self._is_kms_alias(codebuild.export_config_s3_destination_encryption_key):
            codebuild.export_config_s3_destination_encryption_key \
                = self._get_encryption_key_from_alias(codebuild.export_config_s3_destination_encryption_key,
                                                      codebuild.region,
                                                      codebuild.account,
                                                      kms_aliases)

    @staticmethod
    def _assign_keys_data_to_code_build_project(code_build: CodeBuildProject, keys_data: List[KmsKey]):
        def get_kms_data():
            kms_data = next((kms_keys_data for kms_keys_data in keys_data if code_build.encryption_key in kms_keys_data.arn), None)
            return kms_data

        code_build.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_keys_data_to_fsx_windows_file_system(fsx_windows_file_system: FsxWindowsFileSystem, keys_data: List[KmsKey]):
        def get_kms_data():
            kms_data = next((kms_keys_data for kms_keys_data in keys_data if fsx_windows_file_system.kms_key_id in kms_keys_data.arn), None)
            return kms_data

        fsx_windows_file_system.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_route_table_vpc_endpoint_routes(vpc_endpoint_route_table_association: VpcEndpointRouteTableAssociation,
                                                route_tables: AliasesDict[RouteTable],
                                                prefix_lists: List[PrefixLists],
                                                vpc_endpoints: List[VpcEndpoint]):
        if not (route_table := ResourceInvalidator.get_by_id(route_tables, vpc_endpoint_route_table_association.route_table_id, False)):
            return
        for route in route_table.routes:
            if route.target_type == RouteTargetType.GATEWAY_ID and route.target == vpc_endpoint_route_table_association.vpc_endpoint_id:
                return

        prefix_list = next(prefix_list for prefix_list in prefix_lists if prefix_list.region == vpc_endpoint_route_table_association.region)
        if not (vpc_endpoint := ResourceInvalidator.get_by_id(vpc_endpoints, vpc_endpoint_route_table_association.vpc_endpoint_id, False)):
            return
        # If `get_prefix_lists_by_service` returns None this means that the service_name is unresolveable
        # because its taken from a data source of a new entity, which is currently not supported.
        if p_l := prefix_list.get_prefix_lists_by_service(vpc_endpoint.get_aws_service_type()):
            route = Route(vpc_endpoint_route_table_association.route_table_id,
                          p_l.pl_id,
                          RouteTargetType.GATEWAY_ID,
                          vpc_endpoint_route_table_association.vpc_endpoint_id,
                          vpc_endpoint_route_table_association.region,
                          vpc_endpoint_route_table_association.account)
            route_table.routes.append(route)

    @staticmethod
    def _assign_route_tables_to_vpc_endpoint(vpc_endpoint: VpcEndpointGateway, route_tables: AliasesDict[RouteTable],
                                             vpc_endpoint_route_table_associations: List[VpcEndpointRouteTableAssociation]):
        def get_route_tables():
            rts = []

            for rtb_id in vpc_endpoint.route_table_ids:
                if route_table := ResourceInvalidator.get_by_id(route_tables, rtb_id, False):  ### TODO: Should invalidate VPCE???
                    rts.append(route_table)

            for assoc in vpc_endpoint_route_table_associations:
                if assoc.vpc_endpoint_id == vpc_endpoint.vpce_id:
                    if route_table := ResourceInvalidator.get_by_id(route_tables, assoc.route_table_id, False):  ### TODO: Should invalidate VPCE???
                        rts.append(route_table)

            return rts

        vpc_endpoint.route_tables.extend(ResourceInvalidator.get_by_logic(get_route_tables, False))  ### TODO: Should invalidate VPCE???

    def _assign_eni_to_vpc_endpoint(self, vpc_endpoint: VpcEndpointInterface, id_to_eni_map: AliasesDict[NetworkInterface]):
        def get_enis():
            enis = []
            for eni_id in vpc_endpoint.network_interface_ids:
                if eni := ResourceInvalidator.get_by_id(id_to_eni_map, eni_id, False):  ### TODO: Should invalidate VPCE?
                    enis.append(eni)
            return enis

        if vpc_endpoint.network_interface_ids and vpc_endpoint.network_interface_ids != ['cfn-pseudo']:
            enis = ResourceInvalidator.get_by_logic(get_enis, False)  ### TODO: Should invalidate VPCE?
            for eni in enis:
                eni.owner = vpc_endpoint
                vpc_endpoint.network_resource.add_interface(eni)
        elif vpc_endpoint.is_managed_by_iac:
            self.pseudo_builder.create_vpc_endpoint_network_interface(vpc_endpoint)
        else:
            vpc_endpoint.add_invalidation('Could not associate network interfaces')

    @staticmethod
    def _assign_keys_data_to_athena_workgroup(athena_workgroup: AthenaWorkgroup, keys_data: List[KmsKey]):
        def get_kms_data():
            if athena_workgroup.encryption_config and (athena_workgroup.kms_key_arn or athena_workgroup.kms_key_id):
                kms_data = next((kms_keys_data for kms_keys_data in keys_data if (athena_workgroup.kms_key_id == kms_keys_data.key_id or
                                                                                  athena_workgroup.kms_key_arn == kms_keys_data.arn)), None)
                return kms_data
            return None

        athena_workgroup.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_keys_data_to_cloudwatch_log_group(cloudwatch_log_group: CloudWatchLogGroup, keys_data: List[KmsKey]):
        if cloudwatch_log_group.kms_encryption:
            cloudwatch_log_group.kms_data = ResourceInvalidator.get_by_logic(
                lambda: next((kms_keys_data for kms_keys_data in keys_data if cloudwatch_log_group.kms_encryption in kms_keys_data.arn), None),
                False
            )

    @staticmethod
    def _assign_policy_data_to_sqs_queue(queue: SqsQueue, sqs_queues_policies: List[SqsQueuePolicy]):
        def get_policy():
            if queue.resource_based_policy:
                return queue.resource_based_policy

            for policy in sqs_queues_policies:
                if not policy.statements:
                    continue
                if policy.queue_name in (queue.queue_name, queue.queue_url):
                    return policy
            return None

        queue.resource_based_policy = ResourceInvalidator.get_by_logic(get_policy, False)  ### TODO: Should invalidate queue?

    @staticmethod
    def _assign_policy_data_to_ecr_repository(repo: EcrRepository, repo_policies: List[EcrRepositoryPolicy]):
        repo.resource_based_policy = ResourceInvalidator.get_by_logic(
            lambda: next((repo_policy for repo_policy in repo_policies if repo_policy.statements
                          and repo.repo_name == repo_policy.repo_name), None),
            False
        )

    def _assign_keys_data_to_ecr_repository(self, repo: EcrRepository, kms_keys: List[KmsKey]):
        if repo.encryption_type == 'KMS':
            def get_kms_data():
                if repo.kms_key_id is not None:
                    kms_data = next((kms_keys_data for kms_keys_data in kms_keys if repo.kms_key_id in kms_keys_data.arn), None)
                else:
                    kms_data = self.pseudo_builder.create_kms_key(repo.get_keys()[0], repo.arn, repo.region, repo.account)
                return kms_data

            repo.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_policy_data_to_cloudwatch_logs_destination(cloudwatch_dest: CloudWatchLogsDestination,
                                                           cloudwatch_dest_policies: List[CloudWatchLogsDestinationPolicy]):
        cloudwatch_dest.resource_based_policy = ResourceInvalidator.get_by_logic(
            lambda: next((cloudwatch_dest_policy for cloudwatch_dest_policy in cloudwatch_dest_policies
                          if cloudwatch_dest_policy.statements and
                          cloudwatch_dest.name == cloudwatch_dest_policy.destination_name), None),
            False
        )

    @staticmethod
    def _assign_policy_data_to_rest_api_gw(rest_api: RestApiGw, rest_api_policies: List[RestApiGwPolicy]):
        rest_api.resource_based_policy = ResourceInvalidator.get_by_logic(
            lambda: next((rest_api_policy for rest_api_policy in rest_api_policies
                          if rest_api_policy.statements and rest_api_policy.rest_api_gw_id == rest_api.rest_api_gw_id), None),
            False
        )

    @staticmethod
    def _assign_policy_data_to_kms_keys(kms_key: KmsKey, kms_policies: List[KmsKeyPolicy]):
        kms_key.resource_based_policy = ResourceInvalidator.get_by_logic(
            lambda: next((kms_policy for kms_policy in kms_policies
                          if kms_policy.statements and kms_policy.key_id == kms_key.key_id), None),
            False
        )

    @staticmethod
    def _assign_policy_data_to_elastic_search_domain(es_domain: ElasticSearchDomain, es_policies: List[ElasticSearchDomainPolicy]):
        if not es_domain.resource_based_policy:
            es_domain.resource_based_policy = ResourceInvalidator.get_by_logic(
                lambda: next((es_policy for es_policy in es_policies
                              if es_policy.statements and es_policy.domain_name == es_domain.name), None),
                False
            )

    @staticmethod
    def _assign_lambda_function_role(lambda_func: LambdaFunction, role_by_arn_map: Dict[str, Role]):
        lambda_func.iam_role = ResourceInvalidator.get_by_id(role_by_arn_map, lambda_func.execution_role_arn, True, lambda_func)

    @staticmethod
    def _assign_lambda_function_policy(lambda_func: LambdaFunction, lambda_policies: List[LambdaPolicy]):
        lambda_func.resource_based_policy = ResourceInvalidator.get_by_logic(
            lambda: next((lambda_policy for lambda_policy in lambda_policies
                          if lambda_func.is_arn_match(lambda_policy.lambda_func_arn)), None),
            False
        )

    @staticmethod
    def _assign_lambda_function_alias(lambda_func: LambdaFunction, lambda_aliases: AliasesDict[LambdaAlias]):
        for lambda_alias in lambda_func.lambda_func_arn_set:
            alias = lambda_aliases.get(lambda_alias)
            if alias:
                lambda_func.lambda_func_alias = alias
                lambda_func.lambda_func_arn_set.add(
                    create_lambda_function_arn(lambda_func.account, lambda_func.region, lambda_func.function_name, alias.name))
                if alias.function_name_or_arn.endswith('.arn'):
                    alias.function_name_or_arn = lambda_func.function_name  # for the 'get_cloud_resource_url' use
                if alias.iac_state and not lambda_func.iac_state:
                    lambda_func.iac_state = alias.iac_state
                break

    @staticmethod
    def _assign_lambda_vpc_config(lambda_func: LambdaFunction, subnets: AliasesDict[Subnet], security_groups: AliasesDict[SecurityGroup]):
        def get_subnets():
            return [subnet for subnet_id in lambda_func.vpc_config.subnet_list_ids
                    if (subnet := ResourceInvalidator.get_by_id(subnets, subnet_id, False))]

        def get_security_groups():
            return [security_group for sg_id in lambda_func.vpc_config.security_groups_ids
                    if (security_group := ResourceInvalidator.get_by_id(security_groups, sg_id, False))]

        ### TODO: Should invalidate lambda?
        if lambda_func.vpc_config:
            lambda_func.vpc_config.subnets.extend(ResourceInvalidator.get_by_logic(get_subnets, False))
            security_groups = ResourceInvalidator.get_by_logic(get_security_groups, False)
            lambda_func.vpc_config.security_groups.extend(security_groups)

    @staticmethod
    def _enrich_lambda_function_arn_with_tf_address(lambda_functions: List[LambdaFunction]):
        for lambda_func in lambda_functions:
            if lambda_func.origin == EntityOrigin.TERRAFORM:
                tf_lambda_func_arn_set = {create_lambda_function_arn(lambda_func.account, lambda_func.region,
                                                                    lambda_func.iac_state.address + '.arn', lambda_func.get_qualifier())}
                lambda_func.lambda_func_arn_set.update(tf_lambda_func_arn_set)

    @staticmethod
    def _exclude_lambda_functions(lambda_functions: List[LambdaFunction]):
        include_lambda_func_list: List[LambdaFunction] = []
        for lambda_func in lambda_functions:
            if lambda_func.is_managed_by_iac or lambda_func.lambda_func_alias or lambda_func.lambda_func_version == '$LATEST':
                include_lambda_func_list.append(lambda_func)
        lambda_functions.clear()
        lambda_functions.extend(include_lambda_func_list)

    @staticmethod
    def _assign_lambda_log_group(lambda_function: LambdaFunction, cloudwatch_log_groups: List[CloudWatchLogGroup]):
        lambda_function.log_group = ResourceInvalidator.get_by_logic(
            lambda: next((log_group for log_group in cloudwatch_log_groups
                          if log_group.name.replace('/aws/lambda/', '') == lambda_function.function_name), None),
            False
        )

    def _assign_eni_to_lambda_function(self, lambda_function: LambdaFunction, subnets: AliasesDict[Subnet]):
        self._assign_network_configuration_to_eni(lambda_function, lambda_function.get_all_network_configurations(), subnets, False)

    @staticmethod
    def _assign_glacier_vault_policies(glacier_vault: GlacierVault, gv_policies: List[GlacierVaultPolicy]):
        glacier_vault.resource_based_policy = ResourceInvalidator.get_by_logic(
            lambda: next((gv_policy for gv_policy in gv_policies if gv_policy.statements
                          and gv_policy.vault_arn == glacier_vault.arn), None),
            False
        )

    @staticmethod
    def _assign_file_system_policies(efs_fs: ElasticFileSystem, efs_policies: List[EfsPolicy]):
        efs_fs.resource_based_policy = ResourceInvalidator.get_by_logic(
            lambda: next((efs_policy for efs_policy in efs_policies
                          if efs_policy.statements and efs_policy.efs_id == efs_fs.efs_id), None),
            False
        )

    @staticmethod
    def _assign_secrets_manager_secrets_policies(sm_secret: SecretsManagerSecret, sm_secret_policies: List[SecretsManagerSecretPolicy]):
        if not sm_secret.resource_based_policy:
            sm_secret.resource_based_policy = ResourceInvalidator.get_by_logic(
                lambda: next((sm_secret_policy for sm_secret_policy in sm_secret_policies if sm_secret_policy.secret_arn == sm_secret.arn), None),
                False
            )

    @staticmethod
    def _assign_docdb_parameter_group_name(docdb_cluster: DocumentDbCluster, docdb_cluster_parameter_groups: List[DocDbClusterParameterGroup]):
        if docdb_cluster.is_new_resource():
            if docdb_cluster.parameter_group_name is not None:
                for parameter_group in docdb_cluster_parameter_groups:
                    ### TODO: Why is there an assignment to docdb_cluster.parameter_group_name, if theres already data there ?
                    if docdb_cluster.parameter_group_name == parameter_group.raw_data.source_id:
                        docdb_cluster.parameter_group_name = parameter_group.group_name

    @staticmethod
    def _assign_keys_data_to_sqs_queue(sqs_queue: SqsQueue, keys_data: List[KmsKey]):
        def get_kms_data():
            if sqs_queue.kms_key:
                kms_data = next((kms_keys_data for kms_keys_data in keys_data if sqs_queue.kms_key in kms_keys_data.arn), None)
                return kms_data
            return None

        sqs_queue.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    def _assign_kms_key_from_alias_to_docdb_cluster(self, docdb_cluster: DocumentDbCluster, kms_aliases: List[KmsAlias]):
        if docdb_cluster.origin == EntityOrigin.CLOUDFORMATION and docdb_cluster.kms_key_id \
            and self._is_kms_alias(docdb_cluster.kms_key_id):
            docdb_cluster.kms_key_id = self._get_encryption_key_from_alias(docdb_cluster.kms_key_id,
                                                                           docdb_cluster.region,
                                                                           docdb_cluster.account,
                                                                           kms_aliases)

    @staticmethod
    def _assign_kms_key_manager_to_docdb_cluster(docdb_cluster: DocumentDbCluster, keys_data: List[KmsKey]):
        def get_kms_data():
            if docdb_cluster.storage_encrypted and docdb_cluster.kms_key_id is not None:
                kms_data = next((kms_keys_data for kms_keys_data in keys_data if docdb_cluster.kms_key_id in kms_keys_data.arn), None)
                return kms_data
            return None

        docdb_cluster.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_api_id_to_domain_data(rest_api_domain: RestApiGwDomain, rest_api_mappings: List[RestApiGwMapping]):
        rest_api_domain.map_data = ResourceInvalidator.get_by_logic(
            lambda: next((map_data for map_data in rest_api_mappings if map_data.domain_name == rest_api_domain.domain_name), None),
            False
        )

    @staticmethod
    def _assign_rest_api_domain(rest_api_gw: RestApiGw, rest_api_domains: List[RestApiGwDomain]):
        rest_api_gw.domain = ResourceInvalidator.get_by_logic(
            lambda: next((domain_data for domain_data in rest_api_domains
                          if domain_data.map_data and domain_data.map_data.api_id == rest_api_gw.rest_api_gw_id), None),
            False
        )

    @staticmethod
    def _assign_integration_to_api_gateway_method(integration: ApiGatewayIntegration, methods: List[ApiGatewayMethod]):
        def _get_method():
            for method in methods:
                if integration.rest_api_id == method.rest_api_id and \
                        integration.resource_id == method.resource_id and \
                        (integration.request_http_method == method.http_method):
                    return method
            return None

        api_gateway_method: ApiGatewayMethod = ResourceInvalidator.get_by_logic(_get_method, True, integration,
                                                                                'could not find api gateway method to assign')
        api_gateway_method.integration = integration

    @classmethod
    def _assign_lambda_function_to_api_gateway_integration(cls, integration: ApiGatewayIntegration, lambda_functions: List[LambdaFunction]):
        def _get_lambda_function():
            for lambda_func in lambda_functions:
                lambda_func_arn: str = cls._uri_to_lambda_function_arn(integration.uri)
                if lambda_func.is_arn_match(lambda_func_arn):
                    return lambda_func
            return None

        if integration.uri:
            integration.lambda_func_integration = ResourceInvalidator.get_by_logic(_get_lambda_function, False)

    @staticmethod
    @lru_cache(maxsize=None)
    def _uri_to_lambda_function_arn(uri: str) -> Optional[str]:
        result = re.search('functions/.*/invocations', uri)
        if result:
            return result.group(0).replace('functions/', '', 1).replace('/invocations', '', 1)
        return None

    @staticmethod
    def _assign_keys_data_to_secrets_manager(secrets_manager: SecretsManagerSecret, keys_data: List[KmsKey]):
        def get_kms_data():
            if secrets_manager.kms_key:
                kms_data = next((kms_keys_data for kms_keys_data in keys_data if secrets_manager.kms_key in kms_keys_data.arn), None)
                return kms_data
            return None

        secrets_manager.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_keys_data_to_neptune_cluster(neptune_cluster: NeptuneCluster, keys_data: List[KmsKey]):
        def get_kms_data():
            if neptune_cluster.kms_key:
                kms_data = next((kms_keys_data for kms_keys_data in keys_data if neptune_cluster.kms_key in kms_keys_data.arn), None)
                return kms_data
            return None

        neptune_cluster.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_keys_data_to_codebuild_report_group(codebuild_report_group: CodeBuildReportGroup, keys_data: List[KmsKey]):
        def get_kms_data():
            if codebuild_report_group.export_config_s3_destination_encryption_key:
                kms_data = next((kms_keys_data for kms_keys_data in keys_data
                                 if codebuild_report_group.export_config_s3_destination_encryption_key in kms_keys_data.arn), None)
                return kms_data
            return None

        codebuild_report_group.export_config_s3_destination_kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    def _assign_eni_to_codebuild_project(self, codebuild_project: CodeBuildProject, subnets: AliasesDict[Subnet]):
        if codebuild_project.get_all_network_configurations():
            self._assign_network_configuration_to_eni(codebuild_project, codebuild_project.get_all_network_configurations(), subnets, False)

    @staticmethod
    def _assign_keys_data_to_sns_topic(sns_topic: SnsTopic, keys_data: List[KmsKey]):
        def get_kms_data():
            if sns_topic.kms_key:
                kms_data = next((kms_keys_data for kms_keys_data in keys_data if sns_topic.kms_key in kms_keys_data.arn), None)
                return kms_data
            return None

        sns_topic.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_alias_data_to_kms_keys(kms_key: KmsKey, keys_aliases: List[KmsAlias]):
        def get_alias_data():
            alias_data = next((alias_data for alias_data in keys_aliases \
                               if alias_data.target_key_id == kms_key.key_id), None)
            return alias_data

        kms_key.alias_data = ResourceInvalidator.get_by_logic(get_alias_data, False)

    @staticmethod
    def _assign_key_manager_data_to_keys_alias(kms_key_alias: KmsAlias, kms_keys: List[KmsKey]):
        def get_key_manager_data():
            key_manager_data = next((key.key_manager for key in kms_keys
                                    if kms_key_alias.target_key_id == key.key_id), None)
            return key_manager_data

        kms_key_alias.key_manager = ResourceInvalidator.get_by_logic(get_key_manager_data, True,
                                                                    kms_key_alias,
                                                                    'Unable to find KMS key associated with the Alias')

    @staticmethod
    def _assign_keys_data_to_xray_encryption(xray: XrayEncryption, keys_data: List[KmsKey]):
        def get_kms_data():
            kms_data = next((kms_keys_data for kms_keys_data in keys_data if xray.key_id is not None
                             and xray.key_id in kms_keys_data.arn), None)
            return kms_data

        xray.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_keys_data_to_workspace(workspace: Workspace, kms_keys: List[KmsKey]):
        def get_keys_data():
            if workspace.volume_encryption_key:
                return next((kms_key for kms_key in kms_keys
                             if (kms_key.key_id and kms_key.key_id in workspace.volume_encryption_key)
                             or (kms_key.alias_data and workspace.volume_encryption_key == kms_key.alias_data.alias_name)), None)
            return None

        workspace.keys_data = ResourceInvalidator.get_by_logic(get_keys_data, False)

    def _assign_eni_to_workspace_directory(self, directory: WorkspaceDirectory, subnets: AliasesDict[Subnet]):
        self._assign_network_configuration_to_eni(directory, directory.get_all_network_configurations(), subnets, False)

    @staticmethod
    def _assign_keys_data_to_rds_cluster_instance(rds_cluster_instance: RdsInstance, keys_data: List[KmsKey]):
        def get_kms_data():
            kms_data = None
            if rds_cluster_instance.performance_insights_kms_key is not None:
                kms_data = next((kms_keys_data for kms_keys_data in keys_data
                                 if rds_cluster_instance.performance_insights_kms_key in kms_keys_data.arn), None)
            return kms_data

        rds_cluster_instance.performance_insights_kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_esc_actions_map_to_iam_entity(iam_entities_map: Dict[str, IamIdentity]):
        executor: CreateIamEntityToEscActionsMapTask = CreateIamEntityToEscActionsMapTask(list(iam_entities_map.values()))
        executor.execute()

        for iam_entity_qualified_arn, actions_map in executor.iam_entity_to_actions_map.items():
            iam_entities_map[iam_entity_qualified_arn].policy_to_escalation_actions_map = actions_map

    @staticmethod
    def _create_id_to_resource_map(resources_list: List[_TMergeable]) -> Dict[str, _TMergeable]:
        return {resource.get_id(): resource for resource in resources_list}

    @staticmethod
    def _assign_ec2_data_to_iam_profile(iam_profile: IamInstanceProfile, ec2s: List[Ec2Instance]):
        iam_profile.ec2_instance_data = ResourceInvalidator.get_by_logic(
            lambda: next((ec2 for ec2 in ec2s if ec2.iam_profile_name == iam_profile.iam_instance_profile_name), None),
            False
        )

    @staticmethod
    def _assign_roles_last_used_data(role: Role, last_used_roles_list: List[RoleLastUsed]):
        role.last_used_date = next((last_used_date for last_used_date in last_used_roles_list
                                    if last_used_date.arn == role.arn), None)

    def _assign_keys_data_to_ssm_parameter(self, ssm_param: SsmParameter, keys_data: List[KmsKey]):
        def get_kms_data():
            kms_data = next((kms_keys_data for kms_keys_data in keys_data if ssm_param.kms_key_id in kms_keys_data.arn
                             or ssm_param.kms_key_id == kms_keys_data.arn), None)
            if kms_data is None:
                kms_data: KmsKey = self.pseudo_builder.create_kms_key(ssm_param.get_keys()[0], None,
                                                                      ssm_param.region, ssm_param.account)
            return kms_data

        ssm_param.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    def _assign_keys_data_to_sagemaker_notebook_instance(self, instance: SageMakerNotebookInstance, keys_data: List[KmsKey]):
        def get_kms_data():
            kms_data = None
            if instance.kms_key_id is None:
                kms_data: KmsKey = self.pseudo_builder.create_kms_key(instance.arn, None, instance.region, instance.account)
            else:
                kms_data = next((kms_keys_data for kms_keys_data in keys_data if instance.kms_key_id in kms_keys_data.arn), None)
            return kms_data

        instance.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    @staticmethod
    def _assign_network_data_from_neptune_cluster(neptune_instance: NeptuneInstance, neptune_clusters: List[NeptuneCluster]):
        def get_npc():
            return next((npc for npc in neptune_clusters
                         if npc.cluster_identifier == neptune_instance.cluster_identifier
                         or npc.cluster_id == neptune_instance.cluster_identifier), None)

        neptune_cluster = ResourceInvalidator.get_by_logic(get_npc, False)
        if neptune_cluster:
            neptune_instance.neptune_subnet_group_name = neptune_cluster.db_subnet_group_name
            neptune_instance.is_in_default_vpc = neptune_instance.neptune_subnet_group_name is None
            neptune_instance.network_configuration.security_groups_ids = neptune_cluster.security_group_ids

    @staticmethod
    def _assign_internet_gateway(vpc: Vpc, igw_list: List[InternetGateway]):
        def get_igw():
            return next((igw for igw in igw_list if igw.vpc_id == vpc.vpc_id), None)

        vpc.internet_gateway = ResourceInvalidator.get_by_logic(get_igw, False)

    @staticmethod
    def _assign_vpc_internet_gateway_attachment(vpc_gateway_attachment: VpcGatewayAttachment, vpcs: AliasesDict[Vpc],
                                                igw_dict: AliasesDict[InternetGateway]):
        vpc: Vpc = ResourceInvalidator.get_by_id(vpcs, vpc_gateway_attachment.vpc_id, True, vpc_gateway_attachment)
        if vpc:
            def find_igw():
                igw: InternetGateway = igw_dict.get(vpc_gateway_attachment.gateway_id)
                if igw:
                    igw.vpc_id = vpc.vpc_id
                    return igw
                else:
                    return None

            vpc.internet_gateway = ResourceInvalidator.get_by_logic(find_igw, True, vpc, 'failed to attach internet gateway to vpc')

    @staticmethod
    def _assign_neptune_instance_to_cluster(neptune_cluster: NeptuneCluster, neptune_instances: List[NeptuneInstance]):
        neptune_cluster.cluster_instances = ResourceInvalidator.get_by_logic(
            lambda: [instance for instance in neptune_instances
                     if instance.cluster_identifier == neptune_cluster.cluster_identifier
                     or instance.cluster_identifier == neptune_cluster.cluster_id],
            False
        )

    def _assign_resources_tags(self, resource: AwsResource, tags_list: List[ResourceTagMappingList]):
        def get_tags_data():
            tags_data = next((tags.tags for tags in tags_list if self._are_arns_equal(tags.resource_arn, resource)), None)
            if tags_data:
                return tags_data
            else:
                return {}

        resource.tags = ResourceInvalidator.get_by_logic(get_tags_data, False)

    @staticmethod
    def _are_arns_equal(tags_arn: str, resource: AwsResource) -> bool:
        if isinstance(resource, LambdaFunction):
            lambda_arn = re.sub(r":[^:]+$", "", resource.arn)
            return tags_arn == lambda_arn
        else:
            return tags_arn == resource.get_arn()

    @staticmethod
    def _assign_s3_bucket_objects(bucket_object: S3BucketObject, buckets: AliasesDict[S3Bucket]):
        owning_bucket = ResourceInvalidator.get_by_id(buckets, bucket_object.bucket_name, True, bucket_object)
        owning_bucket.bucket_objects.append(bucket_object)
        bucket_object.owning_bucket = owning_bucket

    @staticmethod
    def _assign_s3_bucket_logs(s3_bucket: S3Bucket, s3_bucket_logs: List[S3BucketLogging]):
        def get_logs():
            logs = next((logs for logs in s3_bucket_logs if logs.bucket_name == s3_bucket.bucket_name), None)
            return logs

        list_target_buckets = [logs.target_bucket for logs in s3_bucket_logs]
        if any(item in list_target_buckets for item in s3_bucket.aliases):
            s3_bucket.is_logger = True
        s3_bucket.bucket_logging = ResourceInvalidator.get_by_logic(get_logs, False)

    @staticmethod
    def _assign_dms_instance_networking_data(dms_replication_instance: DmsReplicationInstance, vpcs: AliasesDict[Vpc],
                                             subnets: List[Subnet], dms_subnet_group_data: List[DmsReplicationInstanceSubnetGroup]):
        if dms_replication_instance.is_in_default_vpc:
            default_vpc = ResourceInvalidator.get_by_logic(
                lambda: ResourcesAssignerUtil.get_default_vpc(vpcs, dms_replication_instance.account, dms_replication_instance.region),
                True,
                dms_replication_instance,
                f'{dms_replication_instance.get_type()} should be deployed in default VPC, but the default VPC was '
                f'not found for region {dms_replication_instance.region} on account {dms_replication_instance.account}'
            )
            dms_replication_instance.subnet_ids = ResourceInvalidator.get_by_logic(
                lambda: [subnet.subnet_id for subnet in subnets if subnet.vpc_id == default_vpc.vpc_id],
                True,
                dms_replication_instance,
                'Could not associate any subnet')
        else:
            def get_subnet_ids():
                subnet_ids = next((subnet_data.subnet_ids for subnet_data in dms_subnet_group_data
                                   if dms_replication_instance.rep_instance_subnet_group_id in subnet_data.aliases
                                   or (dms_replication_instance.rep_instance_subnet_group_id + dms_replication_instance.account
                                       + dms_replication_instance.region) in subnet_data.aliases), [])
                return subnet_ids

            dms_replication_instance.subnet_ids = ResourceInvalidator.get_by_logic(get_subnet_ids, True, dms_replication_instance,
                                                                                   "Could not find DMS replication subnet ID's")
        if not dms_replication_instance.security_group_ids:
            def get_subnet_group_vpc():
                vpc = ResourceInvalidator.get_by_id(subnets, dms_replication_instance.subnet_ids[0], True, dms_replication_instance).vpc
                return [vpc.default_security_group.get_id()] if vpc else []

            dms_replication_instance.security_group_ids = ResourceInvalidator.get_by_logic(get_subnet_group_vpc, True, dms_replication_instance,
                                                                                           "Could not find DMS security group ID's")

    def _assign_eni_to_dms(self, dms_rep: DmsReplicationInstance, subnets: AliasesDict[Subnet]):
        self._assign_network_configuration_to_eni(dms_rep, dms_rep.get_all_network_configurations(), subnets, dms_rep.is_in_default_vpc)

    @staticmethod
    def _assign_aoi_to_cloudfront_distribution(oai: OriginAccessIdentity, cloudfront_distributions: List[CloudFrontDistribution]):
        def _get_oai_to_origin() -> List[OriginConfig]:
            origin_configs: List[OriginConfig] = []
            for cf_dist in cloudfront_distributions:
                for origin_conf in cf_dist.origin_config_list:
                    if oai.cloudfront_access_identity_path == origin_conf.oai_path:
                        origin_configs.append(origin_conf)
                        break
            return origin_configs

        origin_config_list: List[OriginConfig] = ResourceInvalidator.get_by_logic(_get_oai_to_origin, False)
        for origin_conf in origin_config_list:
            origin_conf.origin_access_identity_list.append(oai)

    @staticmethod
    def _assign_logging_to_cloudfront_distribution(cloudfront: CloudFrontDistribution, cloudfront_log_settings: List[CloudfrontDistributionLogging]):
        cloudfront.logs_settings = ResourceInvalidator.get_by_id(cloudfront_log_settings, cloudfront.distribution_id, False)

    @staticmethod
    def _assign_ecs_cluster_name_to_service(ecs_service: EcsService, ecs_clusters: List[EcsCluster]):
        ecs_service.cluster_name = next((cluster.cluster_name for cluster in ecs_clusters
                                         if cluster.cluster_arn == ecs_service.cluster_arn), None)

    @staticmethod
    def _assign_ecs_cluster_name_to_target(ecs_target: EcsTarget, ecs_clusters: List[EcsCluster]):
        ecs_target.cluster_name = next((cluster.cluster_name for cluster in ecs_clusters
                                        if cluster.cluster_arn == ecs_target.cluster_arn), None)

    def _assign_replication_group_network_data_for_aws_scanner(self, elasticache_rep_group: ElastiCacheReplicationGroup,
                                                               elasticache_clusters: List[ElastiCacheCluster],
                                                               elastic_cache_subnet_groups: List[ElastiCacheSubnetGroup], vpcs: List[Vpc]):
        def get_rep_group_cluster():
            rep_group_cluster = [cluster for cluster in elasticache_clusters
                                 if cluster.replication_group_id == elasticache_rep_group.replication_group_id]
            return rep_group_cluster

        rep_group_clusters = ResourceInvalidator.get_by_logic(get_rep_group_cluster, True, elasticache_rep_group,
                                                              'Could not find cluster nodes for replication group')
        elasticache_rep_group.subnet_group_name = rep_group_clusters[0].subnet_group_name
        elasticache_rep_group.is_in_default_vpc = elasticache_rep_group.subnet_group_name == 'default'
        if elasticache_rep_group.is_in_default_vpc:
            default_vpc = ResourceInvalidator.get_by_logic(
                lambda: ResourcesAssignerUtil.get_default_vpc(vpcs, elasticache_rep_group.account, elasticache_rep_group.region),
                True,
                elasticache_rep_group,
                f'{elasticache_rep_group.get_type()} should be deployed in default VPC, but the default VPC was '
                f'not found for region {elasticache_rep_group.region} on account {elasticache_rep_group.account}'
            )
            elasticache_rep_group.elasticache_security_group_ids = [default_vpc.default_security_group.get_id()]
        else:
            elasticache_rep_group.elasticache_security_group_ids = list(set(flat_list([cluster.elasticache_security_group_ids
                                                                                       for cluster in rep_group_clusters])))

        self._assign_subnet_ids_from_elasticache_subnet_group(elasticache_rep_group, elastic_cache_subnet_groups)

    def _assign_networking_data_for_elasticache_rep_group_tf(self, elasticache_rep_group: ElastiCacheReplicationGroup,
                                                             elastic_cache_subnet_groups: List[ElastiCacheSubnetGroup], vpcs: List[Vpc]):
        self._assign_networking_data_for_elasticache_resource(elasticache_rep_group, elastic_cache_subnet_groups, vpcs)

    def _assign_networking_data_for_elasticache_cluster_aws_scanner(self, elasticache_cluster: ElastiCacheCluster,
                                                                    elastic_cache_subnet_groups: List[ElastiCacheSubnetGroup],
                                                                    vpcs: List[Vpc]):
        self._assign_networking_data_for_elasticache_resource(elasticache_cluster, elastic_cache_subnet_groups, vpcs)

    def _assign_networking_data_for_elasticache_resource(self, elasticache_resource: Union[ElastiCacheReplicationGroup, ElastiCacheCluster],
                                                         elastic_cache_subnet_groups: List[ElastiCacheSubnetGroup],
                                                         vpcs: List[Vpc]):
        if elasticache_resource.is_in_default_vpc:
            self._assign_default_networking_for_elasticache_resource(elasticache_resource, elastic_cache_subnet_groups, vpcs)
        else:
            self._assign_subnet_ids_from_elasticache_subnet_group(elasticache_resource, elastic_cache_subnet_groups)

    def _assign_eni_to_replication_group(self, elasticache_rep_group: ElastiCacheReplicationGroup, subnets: AliasesDict[Subnet]):
        self._assign_network_configuration_to_eni(elasticache_rep_group, elasticache_rep_group.get_all_network_configurations(), subnets, False)

    @staticmethod
    def _assign_default_networking_for_elasticache_resource(elasticache_resource: Union[ElastiCacheReplicationGroup, ElastiCacheCluster],
                                                            elastic_cache_subnet_groups: List[ElastiCacheSubnetGroup],
                                                            vpcs: List[Vpc]):
        def get_default_subnet_group():
            default_subnet_group = next((subnet_group for subnet_group in elastic_cache_subnet_groups
                                         if subnet_group.subnet_group_name == 'default'
                                         and subnet_group.account == elasticache_resource.account
                                         and subnet_group.region == elasticache_resource.region), None)
            return default_subnet_group

        default_subnet_group = ResourceInvalidator.get_by_logic(get_default_subnet_group, True, elasticache_resource,
                                                                'Could not find associated default subnet group')
        elasticache_resource.elasticache_subnet_ids = default_subnet_group.subnet_ids

        default_vpc = ResourceInvalidator.get_by_logic(
            lambda: ResourcesAssignerUtil.get_default_vpc(vpcs, elasticache_resource.account, elasticache_resource.region),
            True,
            elasticache_resource,
            f'{elasticache_resource.get_type()} should be deployed in default VPC, but the default VPC was '
            f'not found for region {elasticache_resource.region} on account {elasticache_resource.account}'
        )
        elasticache_resource.elasticache_security_group_ids = [default_vpc.default_security_group.get_id()]

    @staticmethod
    def _assign_subnet_ids_from_elasticache_subnet_group(elasticache_resource: Union[ElastiCacheReplicationGroup, ElastiCacheCluster],
                                                         elastic_cache_subnet_groups: List[ElastiCacheSubnetGroup]):
        def get_subnet_group():
            subnet_group = next((subnet_group for subnet_group in elastic_cache_subnet_groups
                                 if subnet_group.subnet_group_name == elasticache_resource.subnet_group_name
                                 and subnet_group.account == elasticache_resource.account
                                 and subnet_group.region == elasticache_resource.region), None)
            return subnet_group

        subnet_group = ResourceInvalidator.get_by_logic(get_subnet_group, True, elasticache_resource,
                                                        'Could not find associated subnet group')
        elasticache_resource.elasticache_subnet_ids = subnet_group.subnet_ids

    def _assign_networking_data_for_tf_elasticache_cluster(self, elasticache_cluster: ElastiCacheCluster,
                                                           elastic_cache_subnet_groups: List[ElastiCacheSubnetGroup],
                                                           vpcs: List[Vpc],
                                                           elasticache_rep_groups: List[ElastiCacheReplicationGroup]):
        if elasticache_cluster.is_in_default_vpc and not elasticache_cluster.replication_group_id:
            self._assign_default_networking_for_elasticache_resource(elasticache_cluster, elastic_cache_subnet_groups, vpcs)
        elif not elasticache_cluster.replication_group_id and elasticache_cluster.subnet_group_name != 'default':
            self._assign_subnet_ids_from_elasticache_subnet_group(elasticache_cluster, elastic_cache_subnet_groups)
        else:
            def get_replication_group():
                rep_group = next((group for group in elasticache_rep_groups
                                  if elasticache_cluster.replication_group_id in group.aliases
                                  or (elasticache_cluster.replication_group_id + elasticache_cluster.account + elasticache_cluster.region)
                                  in group.aliases), None)
                return rep_group

            replication_group = ResourceInvalidator.get_by_logic(get_replication_group, True, elasticache_cluster,
                                                                 'Unable to find replication group of Elasticache cluster')
            elasticache_cluster.elasticache_security_group_ids = replication_group.elasticache_security_group_ids
            elasticache_cluster.elasticache_subnet_ids = replication_group.elasticache_subnet_ids

    def _assign_eni_to_elasticache_cluster(self, elasticache_cluster: ElastiCacheCluster, subnets: AliasesDict[Subnet]):
        self._assign_network_configuration_to_eni(elasticache_cluster, elasticache_cluster.get_all_network_configurations(), subnets, False)

    def _assign_eni_to_kinesis_firehose(self, kinesis_firehose: KinesisFirehoseStream, subnets: AliasesDict[Subnet]):
        if kinesis_firehose.get_all_network_configurations():
            self._assign_network_configuration_to_eni(kinesis_firehose, kinesis_firehose.get_all_network_configurations(), subnets, False)

    def _assign_eni_to_efs_mount_target(self, efs_mount_target: EfsMountTarget, subnets: AliasesDict[Subnet]):
        if not efs_mount_target.security_groups_ids:
            mount_target_subnet = ResourceInvalidator.get_by_id(subnets, efs_mount_target.subnet_id, True, efs_mount_target)
            efs_mount_target.security_groups_ids = [mount_target_subnet.vpc.default_security_group.get_id()]
        self._assign_network_configuration_to_eni(efs_mount_target, efs_mount_target.get_all_network_configurations(), subnets, False)

    def _assign_security_group_controller_to_directory(self, directory: DirectoryService, security_groups: AliasesDict[SecurityGroup],
                                                       vpcs: AliasesDict[Vpc]):
        if len(directory.vpc_config.security_groups_ids) > 0:
            directory.security_group_controller = ResourceInvalidator.get_by_id(security_groups, directory.vpc_config.security_groups_ids[0],
                                                                                True, directory)
        elif directory.is_managed_by_iac:
            directory_vpc = ResourceInvalidator.get_by_id(vpcs, directory.vpc_id, True, directory)
            rule_list = self._get_pseudo_dict_data('security_group_cloud_directrory_controller_rules.json')
            directory.security_group_controller = self.pseudo_builder.create_security_group_from_rules_list(directory_vpc, False,
                                                                                                            directory.account,
                                                                                                            directory.region,
                                                                                                            rule_list['Inbound_rules'],
                                                                                                            rule_list['Outbound_rules'],
                                                                                                            None, False)
            directory.vpc_config.security_groups_ids = [directory.security_group_controller.security_group_id]
        else:
            directory.add_invalidation('No security group data available')

    def _assign_eni_to_directory(self, directory: DirectoryService, subnets: AliasesDict[Subnet]):
        self._assign_network_configuration_to_eni(directory, directory.get_all_network_configurations(), subnets, False)

    @staticmethod
    def _assign_cloud_directory_to_workspace_directory(directory: WorkspaceDirectory, cloud_directories: List[DirectoryService]):
        directory.cloud_directory = ResourceInvalidator.get_by_id(cloud_directories, directory.directory_id, True, directory)

    def _assign_networking_to_workspace_directory(self, directory: WorkspaceDirectory, security_groups: AliasesDict[SecurityGroup],
                                                  subnets: AliasesDict[Subnet], vpcs: AliasesDict[Vpc]):
        if not directory.subnet_ids:
            directory.subnet_ids = directory.cloud_directory.vpc_config.subnet_list_ids
        if len(directory.security_group_ids) > 0:
            directory.workspace_security_groups.append(ResourceInvalidator.get_by_id(security_groups,
                                                                                     directory.security_group_ids[0],
                                                                                     True, directory))
            if directory.cloud_directory.security_group_controller.security_group_id not in [sg.security_group_id
                                                                                             for sg in directory.workspace_security_groups]:
                directory.workspace_security_groups.append(directory.cloud_directory.security_group_controller)
        elif directory.is_managed_by_iac:
            directory_vpc = ResourceInvalidator.get_by_id(vpcs, directory.cloud_directory.security_group_controller.vpc_id, True, directory)
            rule_list = self._get_pseudo_dict_data('security_group_workspace_member_rules.json')
            directory.workspace_security_groups.append(self.pseudo_builder.create_security_group_from_rules_list(directory_vpc, False,
                                                                                                                 directory.account,
                                                                                                                 directory.region, None,
                                                                                                                 rule_list['Outbound_rules'],
                                                                                                                 None, False))
            directory.workspace_security_groups.append(directory.cloud_directory.security_group_controller)
            directory.security_group_ids = [sg.security_group_id for sg in directory.workspace_security_groups]

        self._assign_network_configuration_to_eni(directory, directory.get_all_network_configurations(), subnets, False)

    @classmethod
    def _assign_api_gw_methods_to_api_gw(cls, api_gateway: RestApiGw, api_gateway_methods: List[ApiGatewayMethod]):
        for agw_method in api_gateway_methods:
            if agw_method.rest_api_id == api_gateway.rest_api_gw_id:
                api_gateway.api_gateway_methods.append(agw_method)
                if agw_method.integration and \
                        agw_method.integration.lambda_func_integration and \
                        cls._is_lambda_policy_allow_access_to_api_gateway(api_gateway, agw_method.integration.lambda_func_integration):
                    api_gateway.agw_methods_with_valid_integrations_and_allowed_lambda_access.append(agw_method)

    @staticmethod
    def _is_lambda_policy_allow_access_to_api_gateway(api_gateway: RestApiGw, lambda_func: LambdaFunction) -> bool:
        evaluation_results: PolicyEvaluation = PolicyEvaluator.evaluate_actions(source=api_gateway, destination=lambda_func,
                                                                                resource_based_policies=[lambda_func.resource_based_policy],
                                                                                identity_based_policies=[],
                                                                                permission_boundary=None)
        return is_action_subset_allowed(evaluation_results, 'lambda:InvokeFunction')

    @staticmethod
    def _assign_api_gateway_is_public(api_gateway: RestApiGw):
        api_gateway.is_public = \
            api_gateway.api_gateway_type != ApiGatewayType.PRIVATE and \
            (api_gateway.resource_based_policy is None or not is_policy_block_public_access(api_gateway.resource_based_policy))

    @staticmethod
    def _assign_api_gateway_stage(api_gateway: RestApiGw, rest_api_stages: List[ApiGatewayStage]):
        def get_stage():
            stages = [stage for stage in rest_api_stages if stage.api_gw_id == api_gateway.rest_api_gw_id]
            return stages

        api_gateway.api_gw_stages.extend(ResourceInvalidator.get_by_logic(get_stage, False))

    @staticmethod
    def _assign_api_gateway_stage_method_settings(rest_api_stage: ApiGatewayStage, api_gateway_method_settings: List[ApiGatewayMethodSettings]):
        def get_method_settings():
            matching_method_settings = next((settings for settings in api_gateway_method_settings
                                             if settings.api_gw_id == rest_api_stage.api_gw_id
                                             and settings.stage_name == rest_api_stage.stage_name), None)
            return matching_method_settings

        rest_api_stage.method_settings = ResourceInvalidator.get_by_logic(get_method_settings, False)

    @staticmethod
    def _get_pseudo_dict_data(data_path: str) -> dict:
        current_path = os.path.dirname(os.path.abspath(__file__))
        rules_list = os.path.join(current_path + '/pseudo_docs/', data_path)
        with open(rules_list, 'r') as data:
            return json.load(data)

    def _assign_kms_key_from_alias_to_dynamodb_table(self, db_table: DynamoDbTable, kms_aliases: List[KmsAlias]):
        if db_table.origin == EntityOrigin.CLOUDFORMATION and db_table.server_side_encryption \
            and self._is_kms_alias(db_table.kms_key_id):
            db_table.kms_key_id = self._get_encryption_key_from_alias(db_table.kms_key_id,
                                                                      db_table.region,
                                                                      db_table.account,
                                                                      kms_aliases)

    def _assign_keys_data_to_dynamodb_table(self, db_table: DynamoDbTable, keys_data: List[KmsKey]):
        def get_kms_data():
            if db_table.server_side_encryption:
                if db_table.kms_key_id:
                    kms_data = next((kms_keys_data for kms_keys_data in keys_data if db_table.kms_key_id in kms_keys_data.arn), None)
                else:
                    kms_data: KmsKey = self.pseudo_builder.create_kms_key(db_table.get_keys()[0], db_table.table_arn,
                                                                          db_table.region, db_table.account)
                return kms_data
            return None

        db_table.kms_data = ResourceInvalidator.get_by_logic(get_kms_data, False)

    def _assign_eni_to_batch_compute(self, batch: BatchComputeEnvironment, subnets: AliasesDict[Subnet]):
        if batch.get_all_network_configurations():
            self._assign_network_configuration_to_eni(batch, batch.get_all_network_configurations(), subnets, False)

    def _assign_networking_to_mq_broker(self, broker: MqBroker, subnets: AliasesDict[Subnet], vpcs: AliasesDict[Vpc]):
        if not broker.vpc_config.subnet_list_ids or not broker.vpc_config.security_groups_ids:
            default_vpc = ResourceInvalidator.get_by_logic(
                lambda: ResourcesAssignerUtil.get_default_vpc(vpcs, broker.account, broker.region),
                True,
                broker,
                f'{broker.get_type()} should be deployed in default VPC, but the default VPC was '
                f'not found for region {broker.region} on account {broker.account}')
            # AWS choose specific subnets if not defined, based on internal calculation.
            # We choose randomly, as could not find the logic AWS choose it with.
            if not broker.vpc_config.subnet_list_ids:
                if broker.deployment_mode == 'SINGLE_INSTANCE':
                    broker.vpc_config.subnet_list_ids = [next((subnet.subnet_id for subnet in default_vpc.subnets if subnet.is_default), None)]
                else:
                    broker.vpc_config.subnet_list_ids = [subnet.subnet_id for subnet in default_vpc.subnets if subnet.is_default]
            broker.vpc_id = default_vpc.vpc_id
            if not broker.vpc_config.security_groups_ids:
                broker.vpc_config.security_groups_ids = [default_vpc.default_security_group.security_group_id]
        self._assign_network_configuration_to_eni(broker, broker.get_all_network_configurations(), subnets, False)

    @staticmethod
    def _assign_integration_to_api(api_gw: ApiGateway, api_gw_v2_integrations: List[ApiGatewayV2Integration]):
        def get_integration():
            integration = next((integration for integration in api_gw_v2_integrations if integration.rest_api_id == api_gw.api_gw_id), None)
            return integration

        api_gw.api_gw_integration = ResourceInvalidator.get_by_logic(get_integration, False)

    def _assign_vpc_link_to_api_and_eni(self, api_gw: ApiGateway, vpc_links: List[ApiGatewayVpcLink], subnets: AliasesDict[Subnet]):
        if api_gw.api_gw_integration and api_gw.api_gw_integration.connection_id:
            api_gw.vpc_link = ResourceInvalidator.get_by_id(vpc_links, api_gw.api_gw_integration.connection_id, True, api_gw)
        if api_gw.vpc_link:
            self._assign_network_configuration_to_eni(api_gw, api_gw.get_all_network_configurations(), subnets, False)

    def _assign_emr_security_groups_rules_for_tf(self, emr_cluster: EmrCluster, security_groups: AliasesDict[SecurityGroup]):
        if emr_cluster.master_sg_id:
            self._append_security_group_rules_for_emr_cluster_sg(emr_cluster.master_sg_id, security_groups)
        if emr_cluster.slave_sg_id:
            self._append_security_group_rules_for_emr_cluster_sg(emr_cluster.slave_sg_id, security_groups)

    @staticmethod
    def _append_security_group_rules_for_emr_cluster_sg(sg_id: str, security_groups: AliasesDict[SecurityGroup]):
        def get_security_group():
            emr_security_group = next((sg for sg in security_groups if sg.security_group_id == sg_id), None)
            return emr_security_group

        security_group = ResourceInvalidator.get_by_logic(get_security_group, False)
        sg_rules = [SecurityGroupRule(0, 65535, IpProtocol('TCP'), SecurityGroupRulePropertyType.SECURITY_GROUP_ID, sg_id, False,
                                      ConnectionType.INBOUND, sg_id, security_group.region, security_group.account),
                    SecurityGroupRule(0, 65535, IpProtocol('UDP'), SecurityGroupRulePropertyType.SECURITY_GROUP_ID, sg_id, False,
                                      ConnectionType.INBOUND, sg_id, security_group.region, security_group.account),
                    SecurityGroupRule(-1, -1, IpProtocol('ICMP'), SecurityGroupRulePropertyType.SECURITY_GROUP_ID, sg_id, False,
                                      ConnectionType.INBOUND, sg_id, security_group.region, security_group.account)]
        for rule in sg_rules:
            if rule not in security_group.inbound_permissions:
                security_group.inbound_permissions.append(rule)

    @staticmethod
    def _assign_public_access_data_to_emr(emr_cluster: EmrCluster, public_access_data_list: List[EmrPublicAccessConfiguration]):
        emr_cluster.vpc_config.assign_public_ip = not next((public.block_public_access for public in public_access_data_list
                                                            if public.account == emr_cluster.account
                                                            and public.region == emr_cluster.region), True)

    def _assign_networking_to_emr(self, emr_cluster: EmrCluster, subnets: AliasesDict[Subnet], vpcs: AliasesDict[Vpc]):
        if not emr_cluster.vpc_config.subnet_list_ids:
            default_vpc = ResourceInvalidator.get_by_logic(
                lambda: ResourcesAssignerUtil.get_default_vpc(vpcs, emr_cluster.account, emr_cluster.region),
                True,
                emr_cluster,
                f'{emr_cluster.get_type()} should be deployed in default VPC, but the default VPC was '
                f'not found for region {emr_cluster.region} on account {emr_cluster.account}')
            # AWS choose specific subnets if not defined, based on internal calculation.
            # We choose randomly, as could not find the logic AWS choose it with.
            emr_cluster.vpc_config.subnet_list_ids = [default_vpc.subnets[0].subnet_id]

        if not emr_cluster.vpc_config.security_groups_ids:
            subnet = ResourceInvalidator.get_by_id(subnets, emr_cluster.vpc_config.subnet_list_ids[0], True, emr_cluster)
            subnet_vpc = ResourceInvalidator.get_by_id(vpcs, subnet.vpc_id, False)
            security_groups = self._create_default_sg_for_emr(emr_cluster, subnet_vpc)
            emr_cluster.vpc_config.security_groups_ids = [sg.security_group_id for sg in security_groups]

        self._assign_network_configuration_to_eni(emr_cluster, emr_cluster.get_all_network_configurations(), subnets, False)

    def _create_default_sg_for_emr(self, emr_cluster: EmrCluster, sg_vpc: Vpc):
        master_sg_rule_list = self._get_pseudo_dict_data('security_group_emr_master.json')
        slave_sg_rule_list = self._get_pseudo_dict_data('security_group_emr_slave.json')
        master_sg = self.pseudo_builder.create_security_group_from_rules_list(sg_vpc, False, emr_cluster.account, emr_cluster.region,
                                                                              master_sg_rule_list['Inbound_rules'],
                                                                              master_sg_rule_list['Outbound_rules'], None, False)
        slave_sg = self.pseudo_builder.create_security_group_from_rules_list(sg_vpc, False, emr_cluster.account, emr_cluster.region,
                                                                             slave_sg_rule_list['Inbound_rules'],
                                                                             slave_sg_rule_list['Outbound_rules'], None, False)
        return [master_sg, slave_sg]

    @staticmethod
    def _assign_endpoint_resource_to_endpoint_group(gc_endpoint_group: GlobalAcceleratorEndpointGroup,
                                                    endpoints: List[Union[LoadBalancer, ElasticIp, Ec2Instance]]):
        if gc_endpoint_group.endpoint_config_id:
            def get_endpoint():
                endpoint = next((resource for resource in endpoints
                                 if resource.get_id() == gc_endpoint_group.endpoint_config_id
                                 or resource.get_arn() == gc_endpoint_group.endpoint_config_id), None)
                return endpoint

            gc_endpoint_group.endpoint_resource = ResourceInvalidator.get_by_logic(get_endpoint, True, gc_endpoint_group,
                                                                                   f'Unable to find endpoint for resource'
                                                                                   f' {gc_endpoint_group.get_friendly_name()}')

        if gc_endpoint_group.endpoint_resource and not gc_endpoint_group.region:
            gc_endpoint_group.region = gc_endpoint_group.endpoint_resource.region

    def _assign_eni_endpoint_group(self, gc_endpoint_group: GlobalAcceleratorEndpointGroup, vpcs: AliasesDict[Vpc]):
        if gc_endpoint_group.endpoint_resource and isinstance(gc_endpoint_group.endpoint_resource, (LoadBalancer, Ec2Instance)):
            endpoint_resource = gc_endpoint_group.endpoint_resource
            endpoint_vpc = ResourcesAssignerUtil.get_default_vpc(vpcs, gc_endpoint_group.account, gc_endpoint_group.region)
            rules_list = self._get_pseudo_dict_data('default_security_group.json')
            gc_security_group = self.pseudo_builder.create_security_group_from_rules_list(endpoint_vpc, False, gc_endpoint_group.account,
                                                                                          gc_endpoint_group.region, None,
                                                                                          rules_list['Outbound_rules'], None, True)
            self.pseudo_builder.create_eni(endpoint_resource, endpoint_vpc.subnets[0], [gc_security_group.security_group_id],
                                           endpoint_vpc.subnets[0].map_public_ip_on_launch, None, None,
                                           'ENI for Global Accelerator Security group', False)

    @staticmethod
    def _assign_hsm_to_cloudhsm_cluster(cloud_hsm_cluster: CloudHsmV2Cluster, hsm_list: List[CloudHsmV2Hsm]):
        def get_hsm():
            hsm = next((hsm for hsm in hsm_list if hsm.cluster_id == cloud_hsm_cluster.cluster_id), None)
            return hsm

        cloud_hsm_cluster.cluster_hsm = ResourceInvalidator.get_by_logic(get_hsm, False)

    def _assign_eni_to_cloudhsm_cluster(self, cloud_hsm_cluster: CloudHsmV2Cluster, subnets: AliasesDict[Subnet], vpcs: AliasesDict[Vpc]):
        if not cloud_hsm_cluster.vpc_id:
            subnet = ResourceInvalidator.get_by_id(subnets, cloud_hsm_cluster.subnet_ids[0], True, cloud_hsm_cluster)
            cloud_hsm_cluster.vpc_id = subnet.vpc_id
        if not cloud_hsm_cluster.security_group_id:
            rules_list = self._get_pseudo_dict_data('security_group_workspace_member_rules.json')
            cluster_hsm_vpc = ResourceInvalidator.get_by_id(vpcs, cloud_hsm_cluster.vpc_id, True, cloud_hsm_cluster)
            cloud_hsm_security_group = self.pseudo_builder.create_security_group_from_rules_list(cluster_hsm_vpc, False, cloud_hsm_cluster.account,
                                                                                                 cloud_hsm_cluster.region,
                                                                                                 rules_list['Inbound_rules'],
                                                                                                 rules_list['Outbound_rules'], None, False)
            cloud_hsm_cluster.security_group_id = cloud_hsm_security_group.security_group_id
        cloud_hsm_cluster.vpc_config = NetworkConfiguration(False, [cloud_hsm_cluster.security_group_id], cloud_hsm_cluster.subnet_ids)
        if cloud_hsm_cluster.cluster_hsm and cloud_hsm_cluster.cluster_hsm.hsm_state == 'ACTIVE':
            self._assign_network_configuration_to_eni(cloud_hsm_cluster, cloud_hsm_cluster.get_all_network_configurations(), subnets, False)

    def _assign_eni_to_s3outpost_endpoint(self, s3outpost_endpoint: S3OutpostEndpoint, subnets: AliasesDict[Subnet]):
        self._assign_network_configuration_to_eni(s3outpost_endpoint, s3outpost_endpoint.get_all_network_configurations(), subnets, False)

    def _assign_eni_to_worklink_fleet(self, worklink_fleet: WorkLinkFleet, subnets: AliasesDict[Subnet]):
        if worklink_fleet.get_all_network_configurations():
            self._assign_network_configuration_to_eni(worklink_fleet, worklink_fleet.get_all_network_configurations(), subnets, False)

    def _assign_eni_to_glue_connection(self, glue_connection: GlueConnection, subnets: AliasesDict[Subnet]):
        if glue_connection.get_all_network_configurations():
            self._assign_network_configuration_to_eni(glue_connection, glue_connection.get_all_network_configurations(), subnets, False)

    @staticmethod
    def _assign_attributes_to_global_ac(global_accelerator: GlobalAccelerator, gac_attributes: List[GlobalAcceleratorAttribute]):
        def get_attribute():
            attribute = next((attribute for attribute in gac_attributes if attribute.accelerator_arn == global_accelerator.arn), None)
            return attribute

        global_accelerator.attributes = ResourceInvalidator.get_by_logic(get_attribute, False)

    @classmethod
    def clear_cache(cls):
        cls._uri_to_lambda_function_arn.cache_clear()
