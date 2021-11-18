import logging
import os
from typing import List, Optional
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.efs.efs_mount_target import EfsMountTarget, MountTargetSecurityGroups
from cloudrail.knowledge.context.aws.resources_builders.scanner.network_acl_association_builder import NetworkAclAssociationBuilder
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext

from cloudrail.knowledge.context.aws.resources_builders.scanner.account_builder import AccountBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.api_gateway_v2 import ApiGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.api_gateway_v2_integration import ApiGatewayV2IntegrationBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.api_gateway_v2_vpc_link_builder import ApiGatewayVpcLinkBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.athena_workgroups_builder import AthenaWorkGroupsBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.auto_scaling_group_builder import AutoScalingGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.batch_compute_environment_builder import BatchComputeEnvironmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_directory_builder import CloudDirectoryBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_watch_event_target_builder import CloudWatchEventTargetBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_watch_log_groups_builder import CloudWatchLogGroupsBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloudformation.cloudformation_resource_info_builder import CloudformationResourceInfoBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloudfront_distribution_list_builder import \
    CloudFrontDistributionListBuilder, CloudfrontDistributionLoggingBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloudtrail_builder import CloudTrailBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloudwatch_logs_destination_builder import CloudWatchLogsDestinationBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloudwatch_logs_destination_policy_builder \
    import CloudWatchLogsDestinationPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.codebuild_projects_builder import CodeBuildProjectsBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.codebuild_report_group_builder import CodeBuildReportGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.config_aggregator_builder import ConfigAggregatorBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.dax_cluster_builder import DaxClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.db_subnet_group_builder import DbSubnetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.dms_replication_instance_builder import DmsReplicationInstanceBuilder, \
    DmsReplicationInstanceSubnetGroupsBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.docdb_cluster_builder import DocDbClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.docdb_cluster_parameter_group_builder import DocDbClusterParameterGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.dynamodb_builder import DynamoDbBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.ec2_availability_zones_builder import Ec2AvailabilityZonesBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.ec2_builder import Ec2Builder
from cloudrail.knowledge.context.aws.resources_builders.scanner.ec2_image_builder import Ec2ImageBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.ec2_instance_type_builder import Ec2InstanceTypeBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.ecr_repository_builder import EcrRepositoryBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.ecr_repository_policy_builder import EcrRepositoryPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.ecs_builders.ecs_cluster_builder import EcsClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.ecs_builders.ecs_service_builder import EcsServiceBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.ecs_builders.ecs_task_definition_builder import EcsTaskDefinitionBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.efs_builder import EfsBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.efs_mount_target_builder import EfsMountTargetBaseBuilder, EfsMountTargetSecurityGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.efs_policy_builder import EfsPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.egress_only_internet_gateway_builder import EgressOnlyInternetGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.eks_cluster_builder import EksClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.elasti_cache_replication_group_builder import ElastiCacheReplicationGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.elastic_ip_builder import ElasticIpBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.elastic_search_domain_builder import ElasticSearchDomainBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.elastic_search_domain_policy_builder import ElasticSearchDomainPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.elasticache_cluster_builder import ElastiCacheClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.elasticache_subnet_group_builder import ElastiCacheSubnetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.emr_cluster_builder import EmrClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.emr_public_access_config_builder import EmrPublicAccessConfigurationBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.fsx_windows_file_system_builder import FsxWindowsFileSystemBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.glacier_vault_builder import GlacierVaultBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.glacier_vault_policy_builder import GlacierVaultPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.global_accelerator_builder import GlobalAcceleratorAttributeBuilder, GlobalAcceleratorBuilder, \
    GlobalAcceleratorEndpointGroupBuilder, \
    GlobalAcceleratorListenerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.glue_data_catalog_crawler_builder import GlueDataCatalogCrawlerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.glue_data_catalog_policy_builder import GlueDataCatalogPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.glue_data_catalog_table_builder import GlueDataCatalogTableBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.iam_group_builder import IamGroupBuilder, IamGroupInlinePoliciesBuilder, \
    IamPolicyGroupAttachmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.iam_password_policy_builder import IamPasswordPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.iam_policy_builder import IamPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.iam_role_builder import AssumeRolePolicyBuilder, IamRoleBuilder, \
    IamPolicyRoleAttachmentBuilder, IamRoleInlinePoliciesBuilder, IamInstanceProfileBuilder, RoleLastUsedBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.iam_user_builder import IamUserBuilder, IamUserInlinePoliciesBuilder, \
    IamPolicyUserAttachmentBuilder, IamUserGroupMembershipBuilder, IamUsersLoginProfileBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.internet_gateway_builder import InternetGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.kinesis_firehose_stream_builder import KinesisFirehoseStreamBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.kinesis_stream_builder import KinesisStreamBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.kms_alias_builder import KmsAliasBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.kms_key_policy_builder import KmsKeyPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.kms_keys_builder import KmsKeysBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.lambda_builders.lambda_alias_builder import LambdaAliasBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.lambda_builders.lambda_function_builder import LambdaFunctionBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.lambda_builders.lambda_policy_builder \
    import LambdaPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.launch_configuration_builder import \
    LaunchConfigurationBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.launch_templates_builder import LaunchTemplatesBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.load_balancer_attributes_builder import LoadBalancerAttributesBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.load_balancer_builders.load_balancer_builder import \
    LoadBalancerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.load_balancer_builders.load_balancer_target_builder \
    import LoadBalancerTargetBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.load_balancer_builders.load_balancer_target_group_associations_builder \
    import LoadBalancerTargetGroupAssociationBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.load_balancer_builders.load_balancer_target_group_builder \
    import LoadBalancerTargetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.load_balancer_listener_builder import LoadBalancerListenerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.mq_broker_builder import MqBrokerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.nat_gateway_builder import NatGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.neptune_cluster_builder import NeptuneClusterBuilder, NeptuneInstanceBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.network_acl_builder import NetworkAclBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.network_acl_rule_builder import NetworkAclRuleBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.network_interface_builder import NetworkInterfaceBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.origin_access_identity_builder import OriginAccessIdentityBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.peering_connection_builder import PeeringConnectionBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.prefix_lists_builder import PrefixListsBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.rds_cluster_builder import RdsClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.rds_global_cluster_builder import RdsGlobalClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.rds_instance_builder import RdsInstanceBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.redshift_builder import RedshiftBuilder, RedshiftLoggingBuilder, RedshiftSubnetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.resources_tagging_list_builder import ResourceTagMappingListBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.rest_api_gw_builder import \
    ApiGatewayStageBuilder, RestApiGwBuilder, RestApiGwDomainBuilder, RestApiGwMappingBuilder, ApiGatewayMethodSettingsBuilder, \
    RestApiGwPolicyBuilder, \
    ApiGatewayMethodBuilder, ApiGatewayIntegrationBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.route_builder import RouteBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.route_table_association_builder import \
    RouteTableAssociationBuilder, MainRouteTableAssociationBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.route_table_builder import RouteTableBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.s3_bucket_encryption_builder import S3BucketEncryptionBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.s3_bucket_logging_builder import S3BucketLoggingBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.s3_bucket_versioning_builder import S3BucketVersioningBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.s3_builders.public_access_block_settings_builder import \
    PublicAccessBlockSettingsBuilder, AccountPublicAccessBlockSettingsBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.s3_builders.s3_bucket_access_point_builder import \
    S3BucketAccessPointBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.s3_builders.s3_bucket_access_point_policy_builder import \
    S3BucketAccessPointPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.s3_builders.s3_bucket_acl_builder import \
    S3BucketAclBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.s3_builders.s3_bucket_builder import S3BucketBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.s3_builders.s3_bucket_policies_builder import \
    S3BucketPoliciesBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.s3_builders.s3_bucket_region_builder import \
    S3BucketRegionBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.sagemaker_endpoint_config_builder import SageMakerEndpointConfigBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.sagemaker_notebook_instance_builder import SageMakerNotebookInstanceBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.secrets_manager_secret_builder import SecretsManagerSecretBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.secrets_manager_secret_policy_builder import SecretsManagerSecretPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.security_group_builder import SecurityGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.security_group_rule_builder import \
    SecurityGroupRuleBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.sns_topic_builder import SnsTopicBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.sqs_queue_builder import SqsQueueBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.sqs_queue_policy_builder import SqsQueuePolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.ssm_parameter_builder import SsmParameterBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.subnet_builder import SubnetBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.transit_gateway_builders.transit_gateway_builder import \
    TransitGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.transit_gateway_builders.transit_gateway_route_builder import TransitGatewayRouteBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.transit_gateway_builders.transit_gateway_route_table_association_builder import \
    TransitGatewayRouteTableAssociationBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.transit_gateway_builders.transit_gateway_route_table_builder import \
    TransitGatewayRouteTableBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.transit_gateway_builders.transit_gateway_vpc_attachments_builder \
    import TransitGatewayVpcAttachmentsBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.vpc_attributes_builder import VpcAttributeBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.vpc_builder import VpcBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.vpc_endpoint_builder import VpcEndpointBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.vpc_gateway_attachment_builder import VpcGatewayAttachmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.workspaces_builder import WorkspacesBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.workspaces_directory_builder import WorkspacesDirectoryBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.xray_encryption_builder import XrayEncryptionBuilder
from cloudrail.knowledge.context.environment_context.scanner_context_builder import ScannerContextBuilder


def _merge_efs_mount_data(efs_mount_base: List[EfsMountTarget], efs_security_groups: List[MountTargetSecurityGroups]):
    for efs_mount in efs_mount_base:
        mount_security_groups = next((sg.security_groups_ids for sg in efs_security_groups
                                      if sg.mount_target_id == efs_mount.mount_target_id), None)
        if mount_security_groups:
            efs_mount.security_groups_ids = mount_security_groups


class AwsScannerContextBuilder(ScannerContextBuilder):

    @staticmethod
    def build(account_data_dir: Optional[str], account_id: Optional[str] = None, salt: Optional[str] = None, **extra_args) -> BaseEnvironmentContext:
        if not account_data_dir:
            return AwsEnvironmentContext()
        if not os.path.exists(account_data_dir):
            logging.warning('cloud mapper working dir does not exists: {}'.format(account_data_dir))
            return AwsEnvironmentContext()

        if extra_args.get('default_resources_only'):
            vpcs = AliasesDict(*[vpc for vpc in VpcBuilder(account_data_dir, salt).build() if vpc.is_default])
            default_vpcs_ids = [vpc.vpc_id for vpc in vpcs]
            return AwsEnvironmentContext(
                vpcs=vpcs,
                vpcs_attributes=[vpc_attribute for vpc_attribute in VpcAttributeBuilder(account_data_dir, salt).build()
                                 if vpc_attribute.vpc_id in default_vpcs_ids],
                subnets=AliasesDict(*[subnet for subnet in SubnetBuilder(account_data_dir, salt).build() if subnet.is_default]),
                security_groups=AliasesDict(*[sg for sg in SecurityGroupBuilder(account_data_dir, salt).build() if sg.is_default]),
                route_tables=AliasesDict(*[rt for rt in RouteTableBuilder(account_data_dir, salt).build() if rt.is_main_route_table]),
                network_acls=AliasesDict(*[nacl for nacl in NetworkAclBuilder(account_data_dir, salt).build() if nacl.is_default]),
                main_route_table_associations=MainRouteTableAssociationBuilder(account_data_dir, salt).build(),
                kms_aliases=KmsAliasBuilder(account_data_dir, salt).build(),
                resources_tagging_list=ResourceTagMappingListBuilder(account_data_dir, salt).build(),
                origin_access_identity_list=OriginAccessIdentityBuilder(account_data_dir, salt).build())

        accounts = AccountBuilder(account_data_dir, salt).build()
        s3_buckets = S3BucketBuilder(account_data_dir, salt).build()
        s3_bucket_access_points = S3BucketAccessPointBuilder(account_data_dir, salt).build()
        cloud_watch_event_target_list = CloudWatchEventTargetBuilder(account_data_dir, salt).build()
        efs_mount_targets = EfsMountTargetBaseBuilder(account_data_dir, salt).build()
        efs_mount_target_security_groups = EfsMountTargetSecurityGroupBuilder(account_data_dir, salt).build()
        _merge_efs_mount_data(efs_mount_targets, efs_mount_target_security_groups)
        return AwsEnvironmentContext(
            accounts=accounts,
            vpcs=AliasesDict(*VpcBuilder(account_data_dir, salt).build()),
            vpcs_attributes=VpcAttributeBuilder(account_data_dir, salt).build(),
            peering_connections=PeeringConnectionBuilder(account_data_dir, salt).build(),
            subnets=AliasesDict(*SubnetBuilder(account_data_dir, salt).build()),
            security_groups=AliasesDict(*SecurityGroupBuilder(account_data_dir, salt).build()),
            security_group_rules=SecurityGroupRuleBuilder(account_data_dir, salt).build(),
            route_tables=AliasesDict(*RouteTableBuilder(account_data_dir, salt).build()),
            routes=RouteBuilder(account_data_dir, salt).build(),
            route_table_associations=RouteTableAssociationBuilder(account_data_dir, salt).build(),
            main_route_table_associations=MainRouteTableAssociationBuilder(account_data_dir, salt).build(),
            network_acls=AliasesDict(*NetworkAclBuilder(account_data_dir, salt).build()),
            network_acl_rules=NetworkAclRuleBuilder(account_data_dir, salt).build(),
            network_acl_associations=AliasesDict(*NetworkAclAssociationBuilder(account_data_dir, salt).build()),
            ec2s=Ec2Builder(account_data_dir, salt).build(),
            load_balancers=LoadBalancerBuilder(account_data_dir, salt).build(),
            load_balancer_target_groups=LoadBalancerTargetGroupBuilder(account_data_dir, salt).build(),
            load_balancer_target_group_associations=LoadBalancerTargetGroupAssociationBuilder(account_data_dir, salt).build(),
            load_balancer_targets=LoadBalancerTargetBuilder(account_data_dir, salt).build(),
            load_balancer_listeners=LoadBalancerListenerBuilder(account_data_dir, salt).build(),
            roles=IamRoleBuilder(account_data_dir, salt).build(),
            role_inline_policies=IamRoleInlinePoliciesBuilder(account_data_dir, salt).build(),
            policies=IamPolicyBuilder(account_data_dir, salt).build(),
            policy_role_attachments=IamPolicyRoleAttachmentBuilder(account_data_dir, salt).build(),
            users_login_profile=IamUsersLoginProfileBuilder(account_data_dir, salt).build(),
            vpc_endpoints=VpcEndpointBuilder(account_data_dir, salt).build(),
            s3_buckets=AliasesDict(*s3_buckets),
            s3_bucket_objects=[],
            s3_bucket_regions=S3BucketRegionBuilder(account_data_dir, salt).build(),
            s3_bucket_acls=S3BucketAclBuilder(account_data_dir, salt).build(),
            s3_bucket_policies=S3BucketPoliciesBuilder(account_data_dir, salt).build(),
            s3_bucket_access_points=s3_bucket_access_points,
            s3_bucket_access_points_policies=S3BucketAccessPointPolicyBuilder(account_data_dir, salt).build(),
            s3_public_access_block_settings_list=PublicAccessBlockSettingsBuilder(account_data_dir, salt).build() + AccountPublicAccessBlockSettingsBuilder
            (account_data_dir, salt).build(),
            transit_gateways=TransitGatewayBuilder(account_data_dir, salt).build(),
            transit_gateway_routes=TransitGatewayRouteBuilder(account_data_dir, salt).build(),
            transit_gateway_attachments=TransitGatewayVpcAttachmentsBuilder(account_data_dir, salt).build(),
            transit_gateway_route_tables=TransitGatewayRouteTableBuilder(account_data_dir, salt).build(),
            transit_gateway_route_table_associations=TransitGatewayRouteTableAssociationBuilder(account_data_dir, salt).build(),
            transit_gateway_route_table_propagations=[],
            network_interfaces=AliasesDict(*NetworkInterfaceBuilder(account_data_dir, salt).build()),
            launch_configurations=LaunchConfigurationBuilder(account_data_dir, salt).build(),
            auto_scaling_groups=AutoScalingGroupBuilder(account_data_dir, salt).build(),
            internet_gateways=InternetGatewayBuilder(account_data_dir, salt).build() + EgressOnlyInternetGatewayBuilder(account_data_dir, salt).build(),
            users=IamUserBuilder(account_data_dir, salt).build(),
            user_inline_policies=IamUserInlinePoliciesBuilder(account_data_dir, salt).build(),
            policy_user_attachments=IamPolicyUserAttachmentBuilder(account_data_dir, salt).build(),
            groups=IamGroupBuilder(account_data_dir, salt).build(),
            group_inline_policies=IamGroupInlinePoliciesBuilder(account_data_dir, salt).build(),
            policy_group_attachments=IamPolicyGroupAttachmentBuilder(account_data_dir, salt).build(),
            iam_group_membership=[],
            iam_user_group_membership=IamUserGroupMembershipBuilder(account_data_dir, salt).build(),
            redshift_clusters=RedshiftBuilder(account_data_dir, salt).build(),
            redshift_subnet_groups=RedshiftSubnetGroupBuilder(account_data_dir, salt).build(),
            ecs_cluster_list=EcsClusterBuilder(account_data_dir, salt).build(),
            ecs_service_list=EcsServiceBuilder(account_data_dir, salt).build(),
            cloud_watch_event_target_list=cloud_watch_event_target_list,
            ecs_targets_list=[target for event_target in cloud_watch_event_target_list for target in event_target.ecs_target_list],
            ecs_task_definitions=EcsTaskDefinitionBuilder(account_data_dir, salt).build(),
            rds_instances=RdsInstanceBuilder(account_data_dir, salt).build(),
            db_subnet_groups=DbSubnetGroupBuilder(account_data_dir, salt).build(),
            rds_clusters=RdsClusterBuilder(account_data_dir, salt).build(),
            rds_global_clusters=RdsGlobalClusterBuilder(account_data_dir, salt).build(),
            elastic_search_domains=ElasticSearchDomainBuilder(account_data_dir, salt).build(),
            iam_instance_profiles=IamInstanceProfileBuilder(account_data_dir, salt).build(),
            eks_clusters=EksClusterBuilder(account_data_dir, salt).build(),
            cloudfront_distribution_list=CloudFrontDistributionListBuilder(account_data_dir, salt).build(),
            origin_access_identity_list=OriginAccessIdentityBuilder(account_data_dir, salt).build(),
            launch_templates=LaunchTemplatesBuilder(account_data_dir, salt).build(),
            elastic_ips=ElasticIpBuilder(account_data_dir, salt).build(),
            unknown_blocks=[],
            rest_api_gw=RestApiGwBuilder(account_data_dir, salt).build(),
            api_gateway_method_settings=ApiGatewayMethodSettingsBuilder(account_data_dir, salt).build(),
            athena_workgroups=AthenaWorkGroupsBuilder(account_data_dir, salt).build(),
            prefix_lists=PrefixListsBuilder(account_data_dir, salt).build(),
            dynamodb_table_list=DynamoDbBuilder(account_data_dir, salt).build(),
            nat_gateway_list=NatGatewayBuilder(account_data_dir, salt).build(),
            dax_cluster=DaxClusterBuilder(account_data_dir, salt).build(),
            docdb_cluster=DocDbClusterBuilder(account_data_dir, salt).build(),
            docdb_cluster_parameter_groups=DocDbClusterParameterGroupBuilder(account_data_dir, salt).build(),
            s3_bucket_encryption=S3BucketEncryptionBuilder(account_data_dir, salt).build(),
            s3_bucket_versioning=S3BucketVersioningBuilder(account_data_dir, salt).build(),
            cloud_watch_log_groups=CloudWatchLogGroupsBuilder(account_data_dir, salt).build(),
            ec2_images=Ec2ImageBuilder(account_data_dir, salt).build(),
            cloudtrail=CloudTrailBuilder(account_data_dir, salt).build(),
            vpc_endpoint_route_table_associations=[],
            codebuild_projects=CodeBuildProjectsBuilder(account_data_dir, salt).build(),
            codebuild_report_groups=CodeBuildReportGroupBuilder(account_data_dir, salt).build(),
            kms_keys=KmsKeysBuilder(account_data_dir, salt).build(),
            sqs_queues=SqsQueueBuilder(account_data_dir, salt).build(),
            elasti_cache_replication_groups=ElastiCacheReplicationGroupBuilder(account_data_dir, salt).build(),
            neptune_clusters=NeptuneClusterBuilder(account_data_dir, salt).build(),
            sqs_queues_policy=SqsQueuePolicyBuilder(account_data_dir, salt).build(),
            sns_topics=SnsTopicBuilder(account_data_dir, salt).build(),
            ecr_repositories=EcrRepositoryBuilder(account_data_dir, salt).build(),
            ecr_repositories_policy=EcrRepositoryPolicyBuilder(account_data_dir, salt).build(),
            kms_keys_policies=KmsKeyPolicyBuilder(account_data_dir, salt).build(),
            rest_api_gw_policies=RestApiGwPolicyBuilder(account_data_dir, salt).build(),
            cloudwatch_logs_destinations=CloudWatchLogsDestinationBuilder(account_data_dir, salt).build(),
            cloudwatch_logs_destination_policies=CloudWatchLogsDestinationPolicyBuilder(account_data_dir, salt).build(),
            elastic_search_domains_policies=ElasticSearchDomainPolicyBuilder(account_data_dir, salt).build(),
            lambda_function_list=LambdaFunctionBuilder(account_data_dir, salt).build(),
            lambda_policies=LambdaPolicyBuilder(account_data_dir, salt).build(),
            lambda_aliases=AliasesDict(*LambdaAliasBuilder(account_data_dir, salt).build()),
            efs_file_systems=EfsBuilder(account_data_dir, salt).build(),
            efs_file_systems_policies=EfsPolicyBuilder(account_data_dir, salt).build(),
            glacier_vaults=GlacierVaultBuilder(account_data_dir, salt).build(),
            glacier_vaults_policies=GlacierVaultPolicyBuilder(account_data_dir, salt).build(),
            secrets_manager_secrets=SecretsManagerSecretBuilder(account_data_dir, salt).build(),
            secrets_manager_secrets_policies=SecretsManagerSecretPolicyBuilder(account_data_dir, salt).build(),
            glue_data_catalog_policy=GlueDataCatalogPolicyBuilder(account_data_dir, salt).build(),
            rest_api_gw_mappings=RestApiGwMappingBuilder(account_data_dir, salt).build(),
            rest_api_gw_domains=RestApiGwDomainBuilder(account_data_dir, salt).build(),
            api_gateway_integrations=ApiGatewayIntegrationBuilder(account_data_dir, salt).build(),
            api_gateway_methods=ApiGatewayMethodBuilder(account_data_dir, salt).build(),
            kinesis_streams=KinesisStreamBuilder(account_data_dir, salt).build(),
            kinesis_firehose_streams=KinesisFirehoseStreamBuilder(account_data_dir, salt).build(),
            xray_encryption_configurations=XrayEncryptionBuilder(account_data_dir, salt).build(),
            checkov_results={},
            workspaces=WorkspacesBuilder(account_data_dir, salt).build(),
            kms_aliases=KmsAliasBuilder(account_data_dir, salt).build(),
            glue_data_catalog_crawlers=GlueDataCatalogCrawlerBuilder(account_data_dir, salt).build(),
            glue_data_catalog_tables=GlueDataCatalogTableBuilder(account_data_dir, salt).build(),
            iam_account_pass_policies=IamPasswordPolicyBuilder(account_data_dir, salt).build(),
            iam_policy_attachments=[],
            neptune_cluster_instances=NeptuneInstanceBuilder(account_data_dir, salt).build(),
            ssm_parameters=SsmParameterBuilder(account_data_dir, salt).build(),
            resources_tagging_list=ResourceTagMappingListBuilder(account_data_dir, salt).build(),
            sagemaker_endpoint_config_list=SageMakerEndpointConfigBuilder(account_data_dir, salt).build(),
            sagemaker_notebook_instances=SageMakerNotebookInstanceBuilder(account_data_dir, salt).build(),
            assume_role_policies=AssumeRolePolicyBuilder(account_data_dir, salt).build(),
            dms_replication_instances=DmsReplicationInstanceBuilder(account_data_dir, salt).build(),
            dms_replication_instance_subnet_groups=DmsReplicationInstanceSubnetGroupsBuilder(account_data_dir, salt).build(),
            elasticache_clusters=ElastiCacheClusterBuilder(account_data_dir, salt).build(),
            elasticache_subnet_groups=ElastiCacheSubnetGroupBuilder(account_data_dir, salt).build(),
            efs_mount_targets=efs_mount_targets,
            workspaces_directories=WorkspacesDirectoryBuilder(account_data_dir, salt).build(),
            cloud_directories=CloudDirectoryBuilder(account_data_dir, salt).build(),
            roles_last_used=RoleLastUsedBuilder(account_data_dir, salt).build(),
            batch_compute_environments=BatchComputeEnvironmentBuilder(account_data_dir, salt).build(),
            mq_brokers=MqBrokerBuilder(account_data_dir, salt).build(),
            api_gateways_v2=ApiGatewayBuilder(account_data_dir, salt).build(),
            api_gateway_v2_integrations=ApiGatewayV2IntegrationBuilder(account_data_dir, salt).build(),
            api_gateway_v2_vpc_links=ApiGatewayVpcLinkBuilder(account_data_dir, salt).build(),
            emr_clusters=EmrClusterBuilder(account_data_dir, salt).build(),
            emr_public_access_configurations=EmrPublicAccessConfigurationBuilder(account_data_dir, salt).build(),
            global_accelerators=GlobalAcceleratorBuilder(account_data_dir, salt).build(),
            global_accelerator_listeners=GlobalAcceleratorListenerBuilder(account_data_dir, salt).build(),
            global_accelerator_endpoint_groups=GlobalAcceleratorEndpointGroupBuilder(account_data_dir, salt).build(),
            cloudhsm_v2_clusters=[],  # Needed API call is not supported currently
            cloudhsm_list=[],  # Needed API call is not supported currently
            s3outpost_endpoints=[],  # Needed API call is not supported currently
            worklink_fleets=[],  # Needed API call is not supported currently
            glue_connections=[],  # Needed API call is not supported currently
            load_balancers_attributes=LoadBalancerAttributesBuilder(account_data_dir, salt).build(),
            ec2_instance_types=Ec2InstanceTypeBuilder(account_data_dir, salt).build(),
            aws_config_aggregators=ConfigAggregatorBuilder(account_data_dir, salt).build(),
            rest_api_stages=ApiGatewayStageBuilder(account_data_dir, salt).build(),
            cloudfront_log_settings=CloudfrontDistributionLoggingBuilder(account_data_dir, salt).build(),
            global_accelerator_attributes=GlobalAcceleratorAttributeBuilder(account_data_dir, salt).build(),
            redshift_logs=RedshiftLoggingBuilder(account_data_dir, salt).build(),
            s3_bucket_logs=S3BucketLoggingBuilder(account_data_dir, salt).build(),
            athena_databases=[],  # Needed API call is not supported currently
            cfn_resources_info=CloudformationResourceInfoBuilder(account_data_dir, salt).build(),
            availability_zones=AliasesDict(*Ec2AvailabilityZonesBuilder(account_data_dir, salt).build()),
            vpc_gateway_attachment=AliasesDict(*VpcGatewayAttachmentBuilder(account_data_dir, salt).build()),
            fsx_windows_file_systems=AliasesDict(*FsxWindowsFileSystemBuilder(account_data_dir, salt).build())
        )
