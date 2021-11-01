import json
from typing import List, Dict, Optional

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_integration import ApiGatewayIntegration
from cloudrail.knowledge.context.aws.resources.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_event_target import CloudWatchEventTarget
from cloudrail.knowledge.context.aws.resources.ecs.ecs_cluster import EcsCluster
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.resources.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import EcsTaskDefinition
from cloudrail.knowledge.context.aws.resources.iam.iam_policy_attachment import IamPolicyAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_group_attachment import PolicyGroupAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_role_attachment import PolicyRoleAttachment
from cloudrail.knowledge.context.aws.resources.iam.policy_user_attachment import PolicyUserAttachment
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_regions import S3BucketRegions
from cloudrail.knowledge.context.aws.resources_builders.terraform.network_acl_association_builder import NetworkAclAssociationBuilder
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.context.managed_resources_summary import ManagedResourcesSummary
from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.utils.terraform_output_validator import TerraformOutputValidator
from cloudrail.knowledge.utils import file_utils
from cloudrail.knowledge.context.aws.resources_builders.terraform.access_origin_identity_builder import OriginAccessIdentityBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.api_gateway_v2 import ApiGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.api_gateway_v2_integration import ApiGatewayV2IntegrationBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.api_gateway_v2_vpc_link_builder import ApiGatewayVpcLinkBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.athena_database_builder import AthenaDatabaseBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.athena_workgroups_builder import AthenaWorkGroupsBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.batch_compute_environment_builder import BatchComputeEnvironmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.cloud_directory_builder import CloudDirectoryBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.cloud_watch.cloud_watch_event_target_builder import CloudWatchEventTargetBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.cloud_watch.cloud_watch_log_groups_builder import CloudWatchLogGroupsBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.cloudfront_distribution_list_builder import CloudFrontDistributionListBuilder, \
    CloudfrontDistributionLoggingBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.cloudhsm_v2_cluster_builder import CloudHsmV2ClusterBuilder, CloudHsmV2HsmBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.cloudtrail_builder import CloudTrailBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.cloudwatch_logs_destination_builder import CloudWatchLogsDestinationBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.cloudwatch_logs_destination_policy_builder \
    import CloudWatchLogsDestinationPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.codebuild_projects_builder import CodeBuildProjectsBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.codebuild_report_group_builder import CodeBuildReportGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.config_aggregator_builder import ConfigAggregatorBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.dax_cluster_builder import DaxClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.db_subnet_group_builder import DbSubnetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.default_network_acl_builder import DefaultNetworkAclBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.default_route_table_builder import DefaultRouteTableBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.default_route_table_inline_routes_builder import \
    DefaultRouteTableInlineRoutesBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.default_security_group_builder import \
    DefaultSecurityGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.default_subnet_builder import DefaultSubnetBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.default_vpc_builder import DefaultVpcBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.dms_replication_instance_builder import DmsReplicationInstanceBuilder, \
    DmsReplicationInstanceSubnetGroupsBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.docdb_cluster_builder import DocDbClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.docdb_cluster_parameter_group_builder import DocDbClusterParameterGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.dynamodb_builder import DynamoDbTableBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.ec2_builder import Ec2Builder
from cloudrail.knowledge.context.aws.resources_builders.terraform.ec2_image_builder import AwsAmiBuilder, AwsAmiCopyBuilder, AwsAmiFromInstanceBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.ecr_repository_builder import EcrRepositoryBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.ecr_repository_policy_builder import EcrRepositoryPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.ecs.ecs_cluster_builder import EcsClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.ecs.ecs_service_builder import EcsServiceBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.ecs.ecs_task_definition_builder import EcsTaskDefinitionBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.efs_builder import EfsBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.efs_mount_target_builder import EfsMountTargetBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.efs_policy_builder import EfsPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.egress_only_internet_gateway_builder import EgressOnlyInternetGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.eks_cluster_builder import EksClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.elasti_cache_replication_group_builder import ElastiCacheReplicationGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.elastic_ip_builder import ElasticIpBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.elastic_search_domain_builder import ElasticSearchDomainBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.elastic_search_domain_policy_builder import ElasticSearchDomainPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.elasticache_cluster_builder import ElastiCacheClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.elasticache_subnet_group_builder import ElastiCacheSubnetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.emr_cluster_builder import EmrClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.fsx_windows_file_system_builder import FsxWindowsFileSystemBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.glacier_vault_builder import GlacierVaultBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.glacier_vault_policy_builder import GlacierVaultPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.global_accelerator_builder import GlobalAcceleratorAttributeBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.global_accelerator_builder import GlobalAcceleratorBuilder, \
    GlobalAcceleratorEndpointGroupBuilder, \
    GlobalAcceleratorListenerBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.glue_connection_builder import GlueConnectionBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.glue_data_catalog_crawler_builder import GlueDataCatalogCrawlerBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.glue_data_catalog_policy_builder import GlueDataCatalogPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.glue_data_catalog_table_builder import GlueDataCatalogTableBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.iam_group_builder import IamGroupBuilder, PolicyGroupAttachmentBuilder, \
    GroupInlinePolicieBuilder, IamGroupMembershipBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.iam_password_policy_builder import IamPasswordPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.iam_policy_attachment_builder import IamPolicyAttachmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.iam_role_builder import AssumeRolePolicyBuilder, IamRoleBuilder, \
    PolicyRoleAttachmentBuilder, RoleInlineNestedPolicyBuilder, RoleInlinePolicieBuilder, IamInstanceProfileBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.iam_user_builder import IamUserBuilder, UserInlinePolicieBuilder, \
    PolicyUserAttachmentBuilder, IamUserGroupMembershipBuilder, IamUsersLoginProfileBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.internet_gateway_builder import InternetGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.kinesis_firehose_stream_builder import KinesisFirehoseStreamBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.kinesis_stream_builder import KinesisStreamBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.kms_alias_builder import KmsAliasBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.kms_keys_builder import KmsKeysBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.kms_keys_policy_builder import KmsKeyPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.lambda_function.lambda_alias_builder import LambdaAliasBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.lambda_function.lambda_function_builder import LambdaFunctionBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.lambda_function.lambda_policy_builder import LambdaPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.launch_configuration_builder import \
    LaunchConfigurationBuilder, AutoScalingGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.launch_templates_builder import LaunchTemplateBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.load_balancer_attributes_builder import LoadBalancerAttributesBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.load_balancer_builder import LoadBalancerBuilder, \
    LoadBalancerTargetGroupBuilder, LoadBalancerTargetBuilder, LoadBalancerTargetGroupAssociationBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.load_balancer_listener_builder import LoadBalancerListenerBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.main_route_table_associations_builder import MainRouteTableAssociationsBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.mq_broker_builder import MqBrokerBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.nat_gateway_builder import NatGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.neptune_cluster_builder import NeptuneClusterBuilder, NeptuneInstanceBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.network_acl_builder import NetworkAclBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.network_acl_inline_rules_builder import NetworkAclInlineRulesBuilder, \
    DefaultNetworkAclInlineRulesBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.network_acl_rule_builder import NetworkAclRuleBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.network_interface_builder import NetworkInterfaceBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.peering_connection_builder import PeeringConnectionBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.policies_builder import S3BucketPolicyBuilder, \
    ManagedPolicyBuilder, S3BucketInlinePolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.rds_cluster_builder import RdsClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.rds_cluster_instance_builder import RdsClusterInstanceBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.rds_global_cluster_builder import RdsGlobalClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.rds_instance_builder import RdsInstanceBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.redshift_builder import RedshiftBuilder, RedshiftLoggingBuilder, \
    RedshiftSubnetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.rest_api_gw_builder import ApiGatewayStageBuilder, RestApiGwBuilder, \
    RestApiGwDomainBuilder, \
    RestApiGwMappingBuilder, ApiGatewayMethodSettingsBuilder, RestApiGwPolicyBuilder, ApiGateWayIntegrationBuilder, ApiGateWayMethodBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.route_builder import RouteBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.route_table_associations_builder import \
    RouteTableAssociationsBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.route_table_builder import RouteTableBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.route_table_inline_routes_builder import \
    RouteTableInlineRoutesBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.s3_bucket_builder import S3BucketBuilder, \
    S3AccessPointBuilder, S3AclBuilder, PublicAccessBlockSettingsBuilder, AccountPublicAccessBlockSettingsBuilder, S3BucketEncryptionBuilder, \
    S3BucketLoggingBuilder, S3BucketObjectBuilder, S3BucketVersioningBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.s3outpost_endpoint_builder import S3OutpostEndpointBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.sagemaker_endpoint_config_builder import SageMakerEndpointConfigBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.sagemaker_notebook_instance_builder import SageMakerNotebookInstanceBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.secrets_manager_secret_builder import SecretsManagerSecretBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.secrets_manager_secret_policy_builder import SecretsManagerSecretPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.security_group_builder import SecurityGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.security_group_inline_rules_builder import SecurityGroupInlineRulesBuilder, \
    DefaultSecurityGroupInlineRulesBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.security_group_rule_builder import SecurityGroupRuleBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.sns_topic_builder import SnsTopicBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.sqs_queue_builder import SqsQueueBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.sqs_queue_policy_builder import SqsQueuePolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.ssm_parameter_builder import SsmParameterBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.subnet_builder import SubnetBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.transit_gateway_builder import TransitGatewayBuilder, \
    TransitGatewayRouteBuilder, TransitGatewayRouteTableBuilder, TransitGatewayAttachmentBuilder, TransitGatewayRouteTableAssociationBuilder, \
    TransitGatewayRouteTablePropagationBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.vpc_attributes_builder import VpcAttributeBuilder, DefaultVpcAttributeBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.vpc_builder import VpcBuilder, VpcEndpointBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.vpc_endpoint_route_table_association_builder \
    import VpcEndpointRouteTableAssociationBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.vpc_gateway_attachment_builder import VpcGatewayAttachmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.worklink_fleet_builder import WorkLinkFleetBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.workspaces_builder import WorkspacesBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.workspaces_directory_builder import WorkspacesDirectoryBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.xray_encryption_builder import XrayEncryptionBuilder
from cloudrail.knowledge.exceptions import UnknownResultOfTerraformApply
from cloudrail.knowledge.context.environment_context.terraform_resources_helper import get_raw_resources_by_type
from cloudrail.knowledge.context.environment_context.terraform_resources_metadata_parser import TerraformResourcesMetadataParser
from cloudrail.knowledge.context.environment_context.terraform_unknown_blocks_parser import TerraformUnknownBlocksParser
from cloudrail.knowledge.context.aws.terraform.aws_terraform_utils import AwsTerraformUtils
from cloudrail.knowledge.context.environment_context.iac_context_builder import IacContextBuilder
from cloudrail.knowledge.utils.checkov_utils import to_checkov_results


class AwsTerraformContextBuilder(IacContextBuilder):

    @classmethod
    def build(cls,
              iac_file: str,
              account_id: str,
              scanner_environment_context: Optional[BaseEnvironmentContext] = None,
              salt: Optional[str] = None,
              **extra_args) -> AwsEnvironmentContext:
        if not iac_file:
            return AwsEnvironmentContext()
        use_after_data: bool = bool(extra_args['use_after_data']) if 'use_after_data' in extra_args else True
        keep_deleted_entities: bool = bool(extra_args['keep_deleted_entities']) if 'keep_deleted_entities' in extra_args else True
        iac_url_template: Optional[str] = extra_args.get('iac_url_template')
        data = file_utils.read_all_text(iac_file)
        TerraformOutputValidator.validate(data)
        dic = json.loads(data)

        resources_metadata = TerraformResourcesMetadataParser.parse(dic['configuration'])
        resources = get_raw_resources_by_type(dic['resource_changes'], resources_metadata, use_after_data, keep_deleted_entities)
        unknown_blocks = TerraformUnknownBlocksParser.parse(dic['resource_changes'])
        managed_resources_summary = cls._to_managed_resources_summary(dic.get('managed_resources_summary', {}))
        aws_terraform_utils = AwsTerraformUtils(dic)
        for resource in resources.values():
            for entity in resource:
                entity['account_id'] = account_id
                entity['salt'] = salt
                entity['region'] = aws_terraform_utils.get_resource_region(entity['tf_address'])
                entity['iac_url_template'] = iac_url_template

        ecs_cluster_list: List[EcsCluster] = EcsClusterBuilder(resources).build()
        ecs_service_list: List[EcsService] = EcsServiceBuilder(resources).build()
        cloud_watch_event_target_list: List[CloudWatchEventTarget] = CloudWatchEventTargetBuilder(resources).build()
        ecs_targets_list: List[EcsTarget] = []
        for event_target in cloud_watch_event_target_list:
            for target in event_target.ecs_target_list:
                target.iac_state = IacState(address=event_target.iac_state.address + 'ecs_target',
                                            action=IacActionType.NO_OP,
                                            resource_metadata=event_target.iac_state.resource_metadata,
                                            is_new=event_target.iac_state.is_new,
                                            iac_type=IacType.TERRAFORM)
                ecs_targets_list.append(target)
        ecs_task_definitions: List[EcsTaskDefinition] = EcsTaskDefinitionBuilder(resources).build()

        vpcs = AliasesDict(*VpcBuilder(resources).build())
        default_vpcs = DefaultVpcBuilder(resources).build()
        vpcs.update(*default_vpcs)

        vpcs_attributes = VpcAttributeBuilder(resources).build()
        default_vpcs_attributes = DefaultVpcAttributeBuilder(resources).build()
        vpcs_attributes.extend(default_vpcs_attributes)

        subnets = AliasesDict(*SubnetBuilder(resources).build())
        default_subnets = DefaultSubnetBuilder(resources).build()
        subnets.update(*default_subnets)

        security_groups = AliasesDict(*SecurityGroupBuilder(resources).build())
        default_security_groups = DefaultSecurityGroupBuilder(resources).build()
        security_groups.update(*default_security_groups)

        route_tables = AliasesDict(*RouteTableBuilder(resources).build())

        default_route_tables = AliasesDict(*DefaultRouteTableBuilder(resources).build())
        route_tables.update(*default_route_tables)

        network_acls = AliasesDict(*NetworkAclBuilder(resources).build())

        default_network_acls = AliasesDict(*DefaultNetworkAclBuilder(resources).build())
        network_acls.update(*default_network_acls)

        network_acl_associations = AliasesDict(*NetworkAclAssociationBuilder(resources).build())

        security_group_rules = SecurityGroupRuleBuilder(resources).build()

        security_group_inline_rules = SecurityGroupInlineRulesBuilder(resources).build()

        default_security_group_inline_rules = DefaultSecurityGroupInlineRulesBuilder(resources).build()

        security_group_rules = security_group_rules + security_group_inline_rules + default_security_group_inline_rules

        internet_gateways = InternetGatewayBuilder(resources).build()

        vpc_gateway_attachments = VpcGatewayAttachmentBuilder(resources).build()

        egress_only_igw_list = EgressOnlyInternetGatewayBuilder(resources).build()
        internet_gateways.extend(egress_only_igw_list)

        peering_connections = PeeringConnectionBuilder(resources).build()

        transit_gateways = TransitGatewayBuilder(resources).build()

        transit_gateway_routes = TransitGatewayRouteBuilder(resources).build()

        transit_gateway_route_tables = TransitGatewayRouteTableBuilder(resources).build()

        transit_gateway_attachments = TransitGatewayAttachmentBuilder(resources).build()

        transit_gateway_route_table_associations = TransitGatewayRouteTableAssociationBuilder(resources).build()

        transit_gateway_route_table_propagation = TransitGatewayRouteTablePropagationBuilder(resources).build()

        ec2s = Ec2Builder(resources).build()

        network_interfaces = AliasesDict(*NetworkInterfaceBuilder(resources).build())

        load_balancers = LoadBalancerBuilder(resources).build()

        load_balancers_target_groups = LoadBalancerTargetGroupBuilder(resources).build()

        load_balancer_target_group_associations = LoadBalancerTargetGroupAssociationBuilder(resources).build()

        load_balancer_targets = LoadBalancerTargetBuilder(resources).build()

        launch_configurations = LaunchConfigurationBuilder(resources).build()

        auto_scaling_groups = AutoScalingGroupBuilder(resources).build()

        s3_buckets = S3BucketBuilder(resources).build()

        s3_inline_buckets_policies = S3BucketInlinePolicyBuilder(resources).build()

        s3_buckets_policies = S3BucketPolicyBuilder(resources).build()

        s3_buckets_policies = s3_buckets_policies + s3_inline_buckets_policies

        s3_bucket_access_points = S3AccessPointBuilder(resources).build()

        s3_acls = S3AclBuilder(resources).build()

        s3_public_access_block_settings_list = PublicAccessBlockSettingsBuilder(resources).build()

        s3_public_access_block_settings_list.extend(AccountPublicAccessBlockSettingsBuilder(resources).build())

        routes = RouteBuilder(resources).build()

        route_table_inline_routes = RouteTableInlineRoutesBuilder(resources).build()

        default_route_table_inline_routes = DefaultRouteTableInlineRoutesBuilder(resources).build()

        routes = routes + route_table_inline_routes + default_route_table_inline_routes

        route_table_associations = RouteTableAssociationsBuilder(resources).build()

        main_route_table_associations = MainRouteTableAssociationsBuilder(resources).build()

        network_acl_rules = NetworkAclRuleBuilder(resources).build()

        network_acl_inline_rules = NetworkAclInlineRulesBuilder(resources).build()

        default_network_acl_inline_rules = DefaultNetworkAclInlineRulesBuilder(resources).build()

        network_acl_rules = network_acl_rules + network_acl_inline_rules + default_network_acl_inline_rules

        policies = ManagedPolicyBuilder(resources).build()

        policy_role_attachments = PolicyRoleAttachmentBuilder(resources).build()

        roles = IamRoleBuilder(resources).build()

        iam_instance_profiles = IamInstanceProfileBuilder(resources).build()

        role_inline_policy_standard = RoleInlinePolicieBuilder(resources).build()

        role_inline_policy_nested = RoleInlineNestedPolicyBuilder(resources).build()

        role_inline_policies = role_inline_policy_standard + role_inline_policy_nested

        vpc_endpoints = VpcEndpointBuilder(resources).build()

        s3_bucket_regions = [S3BucketRegions(bucket.bucket_name, bucket.region) for bucket in s3_buckets]

        users = IamUserBuilder(resources).build()

        groups = IamGroupBuilder(resources).build()

        policy_group_attachments = PolicyGroupAttachmentBuilder(resources).build()

        group_inline_policies = GroupInlinePolicieBuilder(resources).build()

        user_inline_policies = UserInlinePolicieBuilder(resources).build()

        policy_user_attachments = PolicyUserAttachmentBuilder(resources).build()

        iam_group_membership = IamGroupMembershipBuilder(resources).build()

        iam_user_group_membership = IamUserGroupMembershipBuilder(resources).build()

        redshift_clusters = RedshiftBuilder(resources).build()

        redshift_subnet_groups = RedshiftSubnetGroupBuilder(resources).build()

        rds_instances = RdsInstanceBuilder(resources).build()

        db_subnet_groups = DbSubnetGroupBuilder(resources).build()

        rds_clusters = RdsClusterBuilder(resources).build()

        rds_cluster_instances = RdsClusterInstanceBuilder(resources).build()

        rds_global_clusters = RdsGlobalClusterBuilder(resources).build()

        elastic_search_domains = ElasticSearchDomainBuilder(resources).build()

        eks_clusters = EksClusterBuilder(resources).build()

        cloudfront_distribution_list = CloudFrontDistributionListBuilder(resources).build()

        origin_access_identity_list = OriginAccessIdentityBuilder(resources).build()

        load_balancer_listeners = LoadBalancerListenerBuilder(resources).build()

        launch_templates = LaunchTemplateBuilder(resources).build()

        elastic_ips = ElasticIpBuilder(resources).build()

        athena_workgroups = AthenaWorkGroupsBuilder(resources).build()

        rest_api_gw = RestApiGwBuilder(resources).build()

        rest_api_gw_methods = ApiGatewayMethodSettingsBuilder(resources).build()

        users_login_profile = IamUsersLoginProfileBuilder(resources).build()

        dynamodb_table_list = DynamoDbTableBuilder(resources).build()

        nat_gateway_list = NatGatewayBuilder(resources).build()

        aws_ami = AwsAmiBuilder(resources).build()

        aws_ami_copy = AwsAmiCopyBuilder(resources).build()

        aws_ami_from_instance = AwsAmiFromInstanceBuilder(resources).build()

        ec2_images = aws_ami + aws_ami_copy + aws_ami_from_instance

        dax_cluster = DaxClusterBuilder(resources).build()

        docdb_cluster = DocDbClusterBuilder(resources).build()

        docdb_cluster_parameter_groups = DocDbClusterParameterGroupBuilder(resources).build()

        s3_bucket_encryption = S3BucketEncryptionBuilder(resources).build()

        s3_bucket_versioning = S3BucketVersioningBuilder(resources).build()

        s3_bucket_objects = S3BucketObjectBuilder(resources).build()

        codebuild_projects = CodeBuildProjectsBuilder(resources).build()

        codebuild_report_groups = CodeBuildReportGroupBuilder(resources).build()

        cloudtrail = CloudTrailBuilder(resources).build()

        cloud_watch_log_groups = CloudWatchLogGroupsBuilder(resources).build()

        kms_keys = KmsKeysBuilder(resources).build()

        vpc_endpoint_route_table_associations = VpcEndpointRouteTableAssociationBuilder(resources).build()

        sqs_queues = SqsQueueBuilder(resources).build()

        sqs_queues_policy = SqsQueuePolicyBuilder(resources).build()

        elasti_cache_replication_groups = ElastiCacheReplicationGroupBuilder(resources).build()

        sns_topics = SnsTopicBuilder(resources).build()

        neptune_clusters = NeptuneClusterBuilder(resources).build()

        ecr_repositories = EcrRepositoryBuilder(resources).build()

        ecr_repositories_policy = EcrRepositoryPolicyBuilder(resources).build()

        cloudwatch_logs_destinations = CloudWatchLogsDestinationBuilder(resources).build()

        cloudwatch_logs_destination_policies = CloudWatchLogsDestinationPolicyBuilder(resources).build()

        rest_api_gw_policies = RestApiGwPolicyBuilder(resources).build()

        kms_keys_policies = KmsKeyPolicyBuilder(resources).build()

        elastic_search_domains_policies = ElasticSearchDomainPolicyBuilder(resources).build()

        lambda_function_list = LambdaFunctionBuilder(resources).build()

        lambda_policies = LambdaPolicyBuilder(resources).build()

        lambda_aliases = AliasesDict(*LambdaAliasBuilder(resources).build())

        glacier_vaults = GlacierVaultBuilder(resources).build()

        glacier_vaults_policies = GlacierVaultPolicyBuilder(resources).build()

        efs_file_systems = EfsBuilder(resources).build()

        efs_file_systems_policies = EfsPolicyBuilder(resources).build()

        glue_data_catalog_policy = GlueDataCatalogPolicyBuilder(resources).build()

        secrets_manager_secrets = SecretsManagerSecretBuilder(resources).build()

        secrets_manager_secrets_policies = SecretsManagerSecretPolicyBuilder(resources).build()

        rest_api_gw_mappings = RestApiGwMappingBuilder(resources).build()

        rest_api_gw_domains = RestApiGwDomainBuilder(resources).build()

        api_gateway_integrations: List[ApiGatewayIntegration] = ApiGateWayIntegrationBuilder(resources).build()

        api_gateway_methods: List[ApiGatewayMethod] = ApiGateWayMethodBuilder(resources).build()

        kinesis_streams = KinesisStreamBuilder(resources).build()

        glue_data_catalog_crawlers = GlueDataCatalogCrawlerBuilder(resources).build()

        glue_data_catalog_tables = GlueDataCatalogTableBuilder(resources).build()

        xray_encryption_configurations = XrayEncryptionBuilder(resources).build()

        kinesis_firehose_streams = KinesisFirehoseStreamBuilder(resources).build()

        checkov_results = to_checkov_results(dic.get('checkov_results', {}))

        iam_account_pass_policies = IamPasswordPolicyBuilder(resources).build()

        workspaces = WorkspacesBuilder(resources).build()

        kms_aliases = KmsAliasBuilder(resources).build()

        neptune_cluster_instances = NeptuneInstanceBuilder(resources).build()

        iam_policy_attachments = IamPolicyAttachmentBuilder(resources).build()

        cls._check_duplication_of_attachments(policy_role_attachments, policy_user_attachments, policy_group_attachments,
                                              iam_policy_attachments)

        ssm_parameters = SsmParameterBuilder(resources).build()

        dms_replication_instance_subnet_groups = DmsReplicationInstanceSubnetGroupsBuilder(resources).build()

        dms_replication_instances = DmsReplicationInstanceBuilder(resources).build()

        sagemaker_endpoint_config_list = SageMakerEndpointConfigBuilder(resources).build()

        assume_role_policies = AssumeRolePolicyBuilder(resources).build()

        sagemaker_notebook_instances = SageMakerNotebookInstanceBuilder(resources).build()

        elasticache_clusters = ElastiCacheClusterBuilder(resources).build()
        elasticache_subnet_groups = ElastiCacheSubnetGroupBuilder(resources).build()

        efs_mount_targets = EfsMountTargetBuilder(resources).build()

        workspaces_directories = WorkspacesDirectoryBuilder(resources).build()

        cloud_directories = CloudDirectoryBuilder(resources).build()

        batch_compute_environments = BatchComputeEnvironmentBuilder(resources).build()

        mq_brokers = MqBrokerBuilder(resources).build()

        api_gateways_v2 = ApiGatewayBuilder(resources).build()

        api_gateway_v2_integrations = ApiGatewayV2IntegrationBuilder(resources).build()

        api_gateway_v2_vpc_links = ApiGatewayVpcLinkBuilder(resources).build()

        emr_clusters = EmrClusterBuilder(resources).build()

        global_accelerators = GlobalAcceleratorBuilder(resources).build()

        global_accelerator_listeners = GlobalAcceleratorListenerBuilder(resources).build()

        global_accelerator_endpoint_groups = GlobalAcceleratorEndpointGroupBuilder(resources).build()

        cloudhsm_v2_clusters = CloudHsmV2ClusterBuilder(resources).build()

        cloudhsm_list = CloudHsmV2HsmBuilder(resources).build()

        s3outpost_endpoints = S3OutpostEndpointBuilder(resources).build()

        worklink_fleets = WorkLinkFleetBuilder(resources).build()

        glue_connections = GlueConnectionBuilder(resources).build()

        load_balancers_attributes = LoadBalancerAttributesBuilder(resources).build()

        aws_config_aggregators = ConfigAggregatorBuilder(resources).build()

        rest_api_stages = ApiGatewayStageBuilder(resources).build()

        cloudfront_log_settings = CloudfrontDistributionLoggingBuilder(resources).build()

        global_accelerator_attributes = GlobalAcceleratorAttributeBuilder(resources).build()

        redshift_logs = RedshiftLoggingBuilder(resources).build()

        s3_bucket_logs = S3BucketLoggingBuilder(resources).build()

        athena_databases = AthenaDatabaseBuilder(resources).build()

        fsx_windows_file_systems = AliasesDict(*FsxWindowsFileSystemBuilder(resources).build())

        return AwsEnvironmentContext(vpcs=vpcs,
                                     vpcs_attributes=vpcs_attributes,
                                     internet_gateways=internet_gateways,
                                     vpc_gateway_attachment=AliasesDict(*vpc_gateway_attachments),
                                     subnets=subnets,
                                     transit_gateways=transit_gateways,
                                     ec2s=ec2s,
                                     load_balancers=load_balancers,
                                     s3_buckets=AliasesDict(*s3_buckets),
                                     accounts=AliasesDict(),
                                     peering_connections=peering_connections,
                                     security_groups=security_groups,
                                     security_group_rules=security_group_rules,
                                     route_tables=route_tables,
                                     routes=routes,
                                     route_table_associations=route_table_associations,
                                     main_route_table_associations=main_route_table_associations,
                                     network_acls=network_acls,
                                     network_acl_associations=network_acl_associations,
                                     network_acl_rules=network_acl_rules,
                                     load_balancer_target_groups=load_balancers_target_groups,
                                     load_balancer_target_group_associations=load_balancer_target_group_associations,
                                     load_balancer_targets=load_balancer_targets,
                                     launch_configurations=launch_configurations,
                                     auto_scaling_groups=auto_scaling_groups,
                                     roles=roles,
                                     users=users,
                                     user_inline_policies=user_inline_policies,
                                     policy_user_attachments=policy_user_attachments,
                                     iam_user_group_membership=iam_user_group_membership,
                                     groups=groups,
                                     policy_group_attachments=policy_group_attachments,
                                     users_login_profile=users_login_profile,
                                     group_inline_policies=group_inline_policies,
                                     iam_group_membership=iam_group_membership,
                                     role_inline_policies=role_inline_policies,
                                     policies=policies,
                                     policy_role_attachments=policy_role_attachments,
                                     vpc_endpoints=vpc_endpoints,
                                     s3_bucket_regions=s3_bucket_regions,
                                     s3_bucket_acls=s3_acls,
                                     s3_bucket_policies=s3_buckets_policies,
                                     s3_bucket_access_points=s3_bucket_access_points,
                                     s3_bucket_access_points_policies=[],
                                     s3_public_access_block_settings_list=s3_public_access_block_settings_list,
                                     transit_gateway_routes=transit_gateway_routes,
                                     transit_gateway_attachments=transit_gateway_attachments,
                                     transit_gateway_route_tables=transit_gateway_route_tables,
                                     transit_gateway_route_table_associations=transit_gateway_route_table_associations,
                                     transit_gateway_route_table_propagations=transit_gateway_route_table_propagation,
                                     network_interfaces=network_interfaces,
                                     redshift_clusters=redshift_clusters,
                                     redshift_subnet_groups=redshift_subnet_groups,
                                     ecs_cluster_list=ecs_cluster_list,
                                     ecs_service_list=ecs_service_list,
                                     cloud_watch_event_target_list=cloud_watch_event_target_list,
                                     ecs_targets_list=ecs_targets_list,
                                     ecs_task_definitions=ecs_task_definitions,
                                     rds_instances=rds_instances + rds_cluster_instances,
                                     db_subnet_groups=db_subnet_groups,
                                     rds_clusters=rds_clusters,
                                     rds_global_clusters=rds_global_clusters,
                                     elastic_search_domains=elastic_search_domains,
                                     iam_instance_profiles=iam_instance_profiles,
                                     eks_clusters=eks_clusters,
                                     cloudfront_distribution_list=cloudfront_distribution_list,
                                     origin_access_identity_list=origin_access_identity_list,
                                     load_balancer_listeners=load_balancer_listeners,
                                     launch_templates=launch_templates,
                                     elastic_ips=elastic_ips,
                                     unknown_blocks=unknown_blocks,
                                     rest_api_gw=rest_api_gw,
                                     api_gateway_method_settings=rest_api_gw_methods,
                                     athena_workgroups=athena_workgroups,
                                     prefix_lists=[],
                                     dynamodb_table_list=dynamodb_table_list,
                                     nat_gateway_list=nat_gateway_list,
                                     dax_cluster=dax_cluster,
                                     docdb_cluster=docdb_cluster,
                                     docdb_cluster_parameter_groups=docdb_cluster_parameter_groups,
                                     s3_bucket_encryption=s3_bucket_encryption,
                                     s3_bucket_versioning=s3_bucket_versioning,
                                     s3_bucket_objects=s3_bucket_objects,
                                     cloud_watch_log_groups=cloud_watch_log_groups,
                                     ec2_images=ec2_images,
                                     cloudtrail=cloudtrail,
                                     vpc_endpoint_route_table_associations=vpc_endpoint_route_table_associations,
                                     codebuild_projects=codebuild_projects,
                                     codebuild_report_groups=codebuild_report_groups,
                                     kms_keys=kms_keys,
                                     sqs_queues=sqs_queues,
                                     elasti_cache_replication_groups=elasti_cache_replication_groups,
                                     neptune_clusters=neptune_clusters,
                                     sqs_queues_policy=sqs_queues_policy,
                                     sns_topics=sns_topics,
                                     ecr_repositories=ecr_repositories,
                                     ecr_repositories_policy=ecr_repositories_policy,
                                     kms_keys_policies=kms_keys_policies,
                                     rest_api_gw_policies=rest_api_gw_policies,
                                     cloudwatch_logs_destinations=cloudwatch_logs_destinations,
                                     cloudwatch_logs_destination_policies=cloudwatch_logs_destination_policies,
                                     elastic_search_domains_policies=elastic_search_domains_policies,
                                     lambda_function_list=lambda_function_list,
                                     lambda_policies=lambda_policies,
                                     lambda_aliases=lambda_aliases,
                                     efs_file_systems=efs_file_systems,
                                     efs_file_systems_policies=efs_file_systems_policies,
                                     glacier_vaults=glacier_vaults,
                                     glacier_vaults_policies=glacier_vaults_policies,
                                     secrets_manager_secrets=secrets_manager_secrets,
                                     secrets_manager_secrets_policies=secrets_manager_secrets_policies,
                                     glue_data_catalog_policy=glue_data_catalog_policy,
                                     rest_api_gw_mappings=rest_api_gw_mappings,
                                     rest_api_gw_domains=rest_api_gw_domains,
                                     api_gateway_integrations=api_gateway_integrations,
                                     api_gateway_methods=api_gateway_methods,
                                     kinesis_streams=kinesis_streams,
                                     kinesis_firehose_streams=kinesis_firehose_streams,
                                     xray_encryption_configurations=xray_encryption_configurations,
                                     checkov_results=checkov_results,
                                     workspaces=workspaces,
                                     kms_aliases=kms_aliases,
                                     glue_data_catalog_crawlers=glue_data_catalog_crawlers,
                                     glue_data_catalog_tables=glue_data_catalog_tables,
                                     iam_account_pass_policies=iam_account_pass_policies,
                                     iam_policy_attachments=iam_policy_attachments,
                                     neptune_cluster_instances=neptune_cluster_instances,
                                     ssm_parameters=ssm_parameters,
                                     resources_tagging_list=[],
                                     sagemaker_endpoint_config_list=sagemaker_endpoint_config_list,
                                     sagemaker_notebook_instances=sagemaker_notebook_instances,
                                     assume_role_policies=assume_role_policies,
                                     dms_replication_instances=dms_replication_instances,
                                     dms_replication_instance_subnet_groups=dms_replication_instance_subnet_groups,
                                     managed_resources_summary=managed_resources_summary,
                                     elasticache_clusters=elasticache_clusters,
                                     elasticache_subnet_groups=elasticache_subnet_groups,
                                     efs_mount_targets=efs_mount_targets,
                                     workspaces_directories=workspaces_directories,
                                     cloud_directories=cloud_directories,
                                     roles_last_used=[],
                                     batch_compute_environments=batch_compute_environments,
                                     mq_brokers=mq_brokers,
                                     api_gateways_v2=api_gateways_v2,
                                     api_gateway_v2_integrations=api_gateway_v2_integrations,
                                     api_gateway_v2_vpc_links=api_gateway_v2_vpc_links,
                                     emr_clusters=emr_clusters,
                                     emr_public_access_configurations=[],
                                     global_accelerators=global_accelerators,
                                     global_accelerator_listeners=global_accelerator_listeners,
                                     global_accelerator_endpoint_groups=global_accelerator_endpoint_groups,
                                     cloudhsm_v2_clusters=cloudhsm_v2_clusters,
                                     cloudhsm_list=cloudhsm_list,
                                     s3outpost_endpoints=s3outpost_endpoints,
                                     worklink_fleets=worklink_fleets,
                                     glue_connections=glue_connections,
                                     load_balancers_attributes=load_balancers_attributes,
                                     ec2_instance_types=[],
                                     aws_config_aggregators=aws_config_aggregators,
                                     rest_api_stages=rest_api_stages,
                                     cloudfront_log_settings=cloudfront_log_settings,
                                     global_accelerator_attributes=global_accelerator_attributes,
                                     redshift_logs=redshift_logs,
                                     s3_bucket_logs=s3_bucket_logs,
                                     athena_databases=athena_databases,
                                     fsx_windows_file_systems=fsx_windows_file_systems)

    @classmethod
    def validate(cls, iac_context: AwsEnvironmentContext):
        cls._check_duplication_of_attachments(iac_context.policy_role_attachments,
                                              iac_context.policy_user_attachments,
                                              iac_context.policy_group_attachments,
                                              iac_context.iam_policy_attachments)

    @staticmethod
    def _check_duplication_of_attachments(roles_attachments: List[PolicyRoleAttachment], users_attachments: List[PolicyUserAttachment],
                                          groups_attachments: List[PolicyGroupAttachment], policy_attachments: List[IamPolicyAttachment]):
        all_iam_unique_attachments = roles_attachments + users_attachments + groups_attachments
        for policy_attachment in policy_attachments:
            policies_affected = [iam_attachment.policy_arn for iam_attachment in all_iam_unique_attachments
                                 if iam_attachment.policy_arn == policy_attachment.policy_arn]
            if policies_affected:
                raise UnknownResultOfTerraformApply(f'The Terraform content provided uses both “aws_iam_policy_attachment” and'
                                                    f' one of the unique policy attachments (aws_iam_user_policy_attachment,'
                                                    f' aws_iam_role_policy_attachment, aws_iam_user_group_attachment),'
                                                    f' for the same policy (policy arn: {policies_affected[0]}). '
                                                    f'This creates an unknown end-result and is not supported by Cloudrail.')

    @staticmethod
    def _to_managed_resources_summary(dic: Dict[str, int]):
        return ManagedResourcesSummary(dic.get('created', 0), dic.get('updated', 0), dic.get('deleted', 0), dic.get('total', 0))
