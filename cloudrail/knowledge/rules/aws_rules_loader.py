# pylint: disable=line-too-long
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudtrail_trail_exists import EnsureCloudtrailTrailExists
from typing import Dict, List

from cloudrail.knowledge.rules.aws.context_aware.disallow_ec2_classic_mode_rule import DisallowEc2ClassicModeRule
from cloudrail.knowledge.rules.aws.context_aware.disallow_resources_in_default_vpc_rule import DisallowResourcesInDefaultVpcRule
from cloudrail.knowledge.rules.aws.context_aware.ec2_role_share_rule import Ec2RoleShareRule
from cloudrail.knowledge.rules.aws.context_aware.ensure_all_used_default_security_groups_restrict_all_traffic_rule import \
    EnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule
from cloudrail.knowledge.rules.aws.context_aware.ensure_iam_entities_policy_managed_solely_rule import EnsureIamEntitiesPolicyManagedSolely
from cloudrail.knowledge.rules.aws.context_aware.ensure_no_unused_security_groups_rule import EnsureNoUnusedSecurityGroups
from cloudrail.knowledge.rules.aws.context_aware.iam_privilege_escalation_policy_rule import IamPrivilegeEscalationPolicyRule
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_db_rds_rule import IndirectPublicAccessDbRds
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_db_redshift_rule import \
    IndirectPublicAccessDbRedshift
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_elastic_search_rule import \
    IndirectPublicAccessElasticSearchRule
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.s3_bucket_lambda_indirect_exposure_rule import \
    S3BucketLambdaIndirectExposureRule
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_neptune_rule import PublicAccessDbNeptuneRule
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_rds_rule import PublicAccessDbRdsRule
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_redshift_rule import PublicAccessDbRedshiftRule
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_dms_replication_instance_rule import \
    PublicAccessDmsReplicationInstanceRule
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_eks_api_rule import PublicAccessEksApiRule
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_elasticsearch_rule import PublicAccessElasticSearchRule
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_security_groups_port_rule import \
    PublicAccessSecurityGroupsAllPortsRule, PublicAccessSecurityGroupsCassandraMngPortRule, PublicAccessSecurityGroupsCassandraPortRule, \
    PublicAccessSecurityGroupsCassandraThriftPortRule, PublicAccessSecurityGroupsElasticsearchNodesPortRule, \
    PublicAccessSecurityGroupsElasticsearchPortRule, PublicAccessSecurityGroupsKibanaPortRule, PublicAccessSecurityGroupsMemcachedPortRule, \
    PublicAccessSecurityGroupsMongodbPortRule, PublicAccessSecurityGroupsMongodbShardClusterPortRule, PublicAccessSecurityGroupsMySqlPortRule, \
    PublicAccessSecurityGroupsOracleDbDefaultPortRule, PublicAccessSecurityGroupsOracleDbPortRule, PublicAccessSecurityGroupsOracleDbSslPortRule, \
    PublicAccessSecurityGroupsPostgresPortRule, PublicAccessSecurityGroupsRdpPortRule, PublicAccessSecurityGroupsRedisPortRule, \
    PublicAccessSecurityGroupsSshPortRule
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.s3_acl_allow_public_access_rule import S3AclAllowPublicAccessRule
from cloudrail.knowledge.rules.aws.context_aware.s3_bucket_policy_vpc_endpoint_rule import S3BucketPolicyVpcEndpointRule
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_interface_availability_zone_rule import \
    SqsVpcEndpointInterfaceAvailabilityZoneRule
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_interface_not_used_rule import Ec2VpcEndpointExposureRule, \
    SqsVpcEndpointExposureRule
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.vpc_endpoint_gateway_not_used_rule import DynamoDbVpcEndpointGatewayNotUsedRule, \
    S3VpcEndpointGatewayNotUsedRule
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.vpc_endpoint_route_table_exposure_rule import \
    DynamoDbVpcEndpointRouteTableExposureRule, S3VpcEndpointRouteTableExposureRule
from cloudrail.knowledge.rules.aws.context_aware.vpc_peering_least_access_rule import VpcPeeringLeastAccessRule
from cloudrail.knowledge.rules.aws.context_aware.vpcs_in_tgw_no_overlapping_cidr_rule import VpcsInTransitGatewayNoOverlappingCidrRule
from cloudrail.knowledge.rules.aws.non_context_aware.access_analyzer_rules.access_analyzer_validation_error_and_security_rule import \
    AccessAnalyzerValidationErrorAndSecurityRule
from cloudrail.knowledge.rules.aws.non_context_aware.access_analyzer_rules.access_analyzer_validation_warning_and_suggestion_rule import \
    AccessAnalyzerValidationWarningAndSuggestionRule
from cloudrail.knowledge.rules.aws.non_context_aware.allow_only_private_amis_rule import AllowOnlyPrivateAmisRule
from cloudrail.knowledge.rules.aws.non_context_aware.backup_checks.ensure_rds_resource_backup_retention_enabled_rule import \
    EnsureRdsResourceBackupRetentionEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_athena_database_encrypted_at_rest_rule import \
    EnsureAthenaDatabaseEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_athena_workgroups_encryption_cmk_rule import \
    EnsureAthenaWorkgroupsEncryptionCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_athena_workgroups_results_encrypted_rule import \
    EnsureAthenaWorkGroupsResultsEncryptedRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_cloud_watch_log_groups_encrypted_rule import \
    EnsureCloudWatchLogGroupsEncryptedRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_cloudtrail_encryption_kms_rule import \
    EnsureCloudTrailEncryptionKmsRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_code_build_projects_encrypted_rule import \
    EnsureCodeBuildProjectsEncryptedRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules. \
    encrypt_at_rest.ensure_code_build_report_group_encrypted_at_rest_with_customer_managed_cmk_rule import \
    EnsureCodeBuildReportGroupEncryptedWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_dax_clusters_encrypted_rule import \
    EnsureDaxClustersEncryptedRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_docdb_clusters_encrypted_customer_managed_cmk_rule \
    import EnsureDocdbClustersEncryptedCustomerManagedCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_docdb_clusters_encrypted_rule import \
    EnsureDocdbClustersEncryptedRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_dynamodb_tables_encrypted_at_rest_with_customer_managed_cmk_rule import \
    EnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_ecr_repositories_encrypt_at_rest_with_customer_cmk_rule import \
    EnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_efs_filesystems_encrypted_at_rest_rule import \
    EnsureEfsFilesystemsEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_elasticache_replication_groups_encrypted_at_rest_rule \
    import EnsureElasticacheReplicationGroupsEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_kinesis_firehose_stream_encypted_at_rest_rule import \
    EnsureKinesisFirehoseStreamEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_kinesis_stream_encrypted_at_rest_rule import \
    EnsureKinesisStreamEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_neptune_cluster_encrypted_at_rest_rule import \
    EnsureNeptuneClusterEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest. \
    ensure_neptune_cluster_encrypted_at_rest_rule_with_customer_managed_cmk import EnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest. \
    ensure_rds_cluster_instances_encrypted_at_rest_rule_with_customer_managed_cmk import EnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_rds_instance_encrypt_at_rest_rule \
    import RdsEncryptAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_redshift_cluster_created_encrypted_rule import \
    EnsureRedshiftClusterCreatedEncryptedRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_s3_buckets_encrypted_rule import \
    EnsureS3BucketsEncryptedRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_s3_buckets_object_encrypted_rule import \
    EnsureS3BucketObjectsEncryptedRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest. \
    ensure_sagemaker_endpoint_config_encrypted_at_rest_rule import EnsureSageMakerEndpointConfigEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sagemaker_notebook_instance_encrypted_by_cmk import \
    EnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest. \
    ensure_secrets_manager_secrets_encrypted_at_rest_with_customer_amanaged_cmk_rule import \
    EnsureSecretsManagersSecretsEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sns_topic_encrypted_at_rest_rule import \
    EnsureSnsTopicEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules. \
    encrypt_at_rest.ensure_sns_topic_encrypted_at_rest_with_customer_managed_cmk_rule import EnsureSnsTopicEncryptedAtRestWithCustomerManagerCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_sqs_queues_encrypted_at_rest_rule import \
    EnsureSqsQueuesEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules. \
    encrypt_at_rest.ensure_sqs_queues_encrypted_at_rest_with_customer_managed_cmk_rule import EnsureSqsQueuesEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules. \
    encrypt_at_rest.ensure_ssm_parameter_store_using_encrypted_customer_managed_kms_rule import \
    EnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_workspace_root_volume_encrypted_at_rest_rule import \
    EnsureWorkspaceRootVolumeEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules. \
    encrypt_at_rest.ensure_workspace_root_volume_encrypted_with_customer_cmk_rule import EnsureWorkspaceRootVolumeEncryptionCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_workspace_user_volume_encrypted_at_rest_rule import \
    EnsureWorkspaceUserVolumeEncryptedAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware. \
    encryption_enforcement_rules.encrypt_at_rest.ensure_workspace_user_volume_encrypted_with_customer_cmk_rule import \
    EnsureWorkspaceUserVolumeEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_xray_encryption_using_customer_cmk_rule import \
    EnsureXrayEncryptionCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.es_encrypt_at_rest_rule import EsEncryptAtRestRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest\
    .fsx_windows_file_system_encrypted_at_rest_with_customer_managed_cmk_rule import \
    FsxWindowsFileSystemEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules. \
    encrypt_in_transit.ensure_cloudfront_distribution_encrypt_in_transit_rule import EnsureCloudfrontDistributionEncryptInTransitRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules. \
    encrypt_in_transit.ensure_cloudfront_distribution_field_level_encryption_rule import EnsureCloudfrontDistributionFieldLevelEncryptionRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_in_transit.ensure_docdb_clusters_encrypted_in_transit_rule import \
    EnsureDocdbClustersEncryptedInTransitRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules. \
    encrypt_in_transit.ensure_ecs_task_definition_created_with_efs_encrypt_in_transit_rule import \
    EnsureEcsTaskDefinitionCreatedWithEfsEncryptInTransitRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules. \
    encrypt_in_transit.ensure_elasticache_replication_groups_encrypted_in_transit_rule import EnsureElasticacheReplicationGroupsEncryptedInTransitRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.ensure_api_gw_caching_encrypted_rule import \
    EnsureApiGwCachingEncryptedRule
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.es_encrypt_node_to_node_rule import EsEncryptNodeToNodeRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_all_resources_tagged_rule import EnsureAllResourcesTaggedRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_cloudtrail_multiregion_enabled_rule import EnsureCloudtrailMultiregionEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_config_aggregator_enabled_all_regions_rule import \
    EnsureConfigAggregatorEnabledAllRegionsRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecr_image_scanning_on_push_enabled_rule import EnsureEcrImageScanningOnPushEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecr_repository_image_tags_immutable_rule import EnsureEcrRepositoryImageTagsImmutableRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecs_cluster_enable_container_insights_rule import \
    EnsureEcsClusterEnableContainerInsightsRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_elasticache_redis_cluster_auto_backup_enabled_rule import \
    EnsureElasticacheRedisClusterAutoBackupEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_lambda_function_cannot_be_invoked_public_rule import \
    EnsureLambdaFunctionCannotBeInvokedPublicRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_no_direct_internet_access_allowed_to_sagemaker_notebook_instance_rule import \
    EnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_no_read_only_access_policy_used_by_role_user_rule import \
    EnsureNoReadOnlyAccessPolicyUsedByRoleUserRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_rds_resource_has_iam_authentication_enabled_rule import \
    EnsureRdsResourceIamAuthenticationEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_rest_api_method_use_authentication_rule import EnsureRestApiMethodUseAuthenticationRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_s3_buckets_versioning_rule import EnsureS3BucketsVersioningRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_security_group_include_description_rule import EnsureSecurityGroupIncludeDescriptionRule
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_unused_roles_removed_rule import EnsureUnusedRolesRemoved
from cloudrail.knowledge.rules.aws.non_context_aware.iam_account_pass_policy.iam_account_pass_policy_rules import EnsureIamPasswordExpiration, \
    EnsureIamPasswordLowerCharacters, EnsureIamPasswordMinimumLength, EnsureIamPasswordNotAllowReuse, EnsureIamPasswordRequiresNumber, \
    EnsureIamPasswordRequiresSymbol, EnsureIamPasswordRequiresUpperCase
from cloudrail.knowledge.rules.aws.non_context_aware.iam_no_human_users_rule import IamNoHumanUsersRule
from cloudrail.knowledge.rules.aws.non_context_aware.iam_role_assume_role_principal_too_wide import IamRoleAssumeRolePrincipalTooWide
from cloudrail.knowledge.rules.aws.non_context_aware.iam_user_directly_attach_policies_rule import IAMUserDirectlyAttachPoliciesRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_api_gw_xray_tracing_enabled_rule import \
    EnsureApiGwXrayTracingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudfront_distribution_list_access_logging_enabled_rule import \
    EnsureCloudfrontDistributionListAccessLoggingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudtrail_log_validation_enabled_rule import \
    EnsureCloudTrailLogValidationEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudwatch_log_groups_specify_retention_days_rule import \
    EnsureCloudWatchLogGroupsRetentionUsageRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_docdb_logging_enabled_rule import EnsureDocdbLoggingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_ec2_instance_detailed_monitoring_enabled_rule import \
    EnsureEc2InstanceDetailedMonitoringEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_elasticsearch_domain_logging_enabled_rule import \
    EnsureElasticsearchDomainLoggingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_global_acceleration_flow_logs_enabled_rule import \
    EnsureGlobalAccelerationFlowLogsEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_lambda_function_has_non_infinite_log_retention_rule import \
    EnsureLambdaFunctionHasNonInfiniteLogRetentionRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_lambda_function_xray_tracing_enabled_rule import \
    EnsureLambdaFunctionXrayTracingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_load_balancer_logging_enabeld_rule import \
    EnsureLoadBalancerLoggingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_neptune_cluster_logging_enabled_rule import \
    EnsureNeptuneClusterLoggingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_rds_resource_logging_enabled_rule import \
    EnsureRdsResourceLoggingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_redshift_cluster_logging_enabled_rule import \
    EnsureRedshiftClusterLoggingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_rest_api_gw_access_logging_enabled_rule import \
    EnsureRestApiGwAccessLoggingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_s3_bucket_logging_enabled_rule import \
    EnsureS3BucketLoggingEnabledRule
from cloudrail.knowledge.rules.aws.non_context_aware.performance_optimization.ensure_ec2_instance_ebs_optimized_rule import \
    EnsureEc2InstanceEbsOptimizedRule
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_glue_data_catalog_policy_not_use_wildcard_rule import \
    EnsureGlueDataCatalogPolicyNotUseWildcard
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.policy_wildcard_violation_rules import \
    EnsureCloudWatchLogDestinationPolicyNotUseWildcard, EnsureEcrRepositoryPolicyNotUseWildcard, EnsureEfsPolicyNotUseWildcard, \
    EnsureElasticSearchDomainPolicyNotUseWildcard, EnsureGlacierVaultPolicyNotUseWildcard, EnsureKmsKeyPolicyNotUseWildcard, \
    EnsureLambdaFunctionPolicyNotUseWildcard, EnsureRestApiGwPolicyNotUseWildcard, EnsureS3BucketPolicyNotUseWildcard, \
    EnsureSecretsManagerSecretPolicyNotUseWildcard, EnsureSqsQueuePolicyNotUseWildcard
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.alb_disallow_target_groups_http_rule import AlbDisallowHttpRule
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_alb_is_using_https import EnsureLoadBalancerListenerIsUsingHttps
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_api_gw_use_modern_tls_rule import EnsureApiGwUseModernTlsRule
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_cloudfront_distribution_list_using_waf_rule import \
    CloudFrontEnsureWafUsedRule
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_cloudfront_protocol_version_is_good import \
    CloudFrontEnsureVersionRule
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_imdsv2_is_used_rule import EnsureImdsv2IsUsedRule
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_load_balancer_drops_invalid_http_headers_rule import \
    EnsureLoadBalancerDropsInvalidHttpHeadersRule
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_s3_bucket_policy_use_https_rule import \
    EnsureS3BucketsPolicyUseHttpsRule
from cloudrail.knowledge.rules.base_rule import BaseRule

from cloudrail.knowledge.rules.abstract_rules_loader import AbstractRulesLoader


class AwsRulesLoader(AbstractRulesLoader):

    def load(self) -> Dict[str, BaseRule]:
        rules: List[BaseRule] = [
            # Ec2InboundRule(), # when add back make sure violated/exposed fields are filled
            # Ec2OutboundRule(), # when add back make sure violated/exposed fields are filled
            # Ec2S3ShareRule(), # when add back make sure violated/exposed fields are filled
            # NoVpcPeeringAllowedRule(), # when add back make sure violated/exposed fields are filled
            Ec2RoleShareRule(),
            VpcsInTransitGatewayNoOverlappingCidrRule(),
            EnsureAllUsedDefaultSecurityGroupsRestrictAllTrafficRule(),
            PublicAccessSecurityGroupsSshPortRule(),
            PublicAccessSecurityGroupsRdpPortRule(),
            PublicAccessSecurityGroupsOracleDbDefaultPortRule(),
            PublicAccessSecurityGroupsOracleDbPortRule(),
            PublicAccessSecurityGroupsOracleDbSslPortRule(),
            PublicAccessSecurityGroupsMySqlPortRule(),
            PublicAccessSecurityGroupsPostgresPortRule(),
            PublicAccessSecurityGroupsRedisPortRule(),
            PublicAccessSecurityGroupsMongodbPortRule(),
            PublicAccessSecurityGroupsMongodbShardClusterPortRule(),
            PublicAccessSecurityGroupsCassandraPortRule(),
            PublicAccessSecurityGroupsCassandraThriftPortRule(),
            PublicAccessSecurityGroupsCassandraMngPortRule(),
            PublicAccessSecurityGroupsMemcachedPortRule(),
            PublicAccessSecurityGroupsElasticsearchNodesPortRule(),
            PublicAccessSecurityGroupsElasticsearchPortRule(),
            PublicAccessSecurityGroupsKibanaPortRule(),
            PublicAccessDbRedshiftRule(),
            IndirectPublicAccessDbRedshift(),
            IndirectPublicAccessDbRds(),
            PublicAccessDbRdsRule(),
            DisallowEc2ClassicModeRule(),
            DisallowResourcesInDefaultVpcRule(),
            PublicAccessElasticSearchRule(),
            IndirectPublicAccessElasticSearchRule(),
            VpcPeeringLeastAccessRule(),
            EsEncryptAtRestRule(),
            EsEncryptNodeToNodeRule(),
            PublicAccessEksApiRule(),
            AlbDisallowHttpRule(),
            S3AclAllowPublicAccessRule(),
            CloudFrontEnsureVersionRule(),
            IAMUserDirectlyAttachPoliciesRule(),
            EnsureCloudfrontDistributionEncryptInTransitRule(),
            EnsureLoadBalancerListenerIsUsingHttps(),
            EnsureImdsv2IsUsedRule(),
            EnsureApiGwCachingEncryptedRule(),
            EnsureAthenaWorkGroupsResultsEncryptedRule(),
            S3VpcEndpointGatewayNotUsedRule(),
            DynamoDbVpcEndpointGatewayNotUsedRule(),
            IamNoHumanUsersRule(),
            EnsureRedshiftClusterCreatedEncryptedRule(),
            S3VpcEndpointRouteTableExposureRule(),
            DynamoDbVpcEndpointRouteTableExposureRule(),
            S3BucketPolicyVpcEndpointRule(),
            EnsureDocdbClustersEncryptedRule(),
            EnsureDaxClustersEncryptedRule(),
            EnsureS3BucketsEncryptedRule(),
            EnsureS3BucketsVersioningRule(),
            EnsureS3BucketObjectsEncryptedRule(),
            RdsEncryptAtRestRule(),
            EnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule(),
            EnsureCloudWatchLogGroupsEncryptedRule(),
            AllowOnlyPrivateAmisRule(),
            EnsureAthenaWorkgroupsEncryptionCmkRule(),
            EnsureCloudTrailEncryptionKmsRule(),
            EnsureCodeBuildProjectsEncryptedRule(),
            EnsureCodeBuildReportGroupEncryptedWithCustomerManagedCmkRule(),
            EnsureSqsQueuesEncryptedAtRestRule(),
            EnsureSqsQueuesEncryptedAtRestWithCustomerManagedCmkRule(),
            IamPrivilegeEscalationPolicyRule(),
            EnsureElasticacheReplicationGroupsEncryptedAtRestRule(),
            EnsureElasticacheReplicationGroupsEncryptedInTransitRule(),
            EnsureNeptuneClusterEncryptedAtRestRule(),
            EnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule(),
            EnsureSqsQueuePolicyNotUseWildcard(),
            EnsureSnsTopicEncryptedAtRestRule(),
            EnsureSnsTopicEncryptedAtRestWithCustomerManagerCmkRule(),
            EnsureEcrRepositoryPolicyNotUseWildcard(),
            EnsureS3BucketPolicyNotUseWildcard(),
            EnsureSecretsManagersSecretsEncryptedAtRestWithCustomerManagedCmkRule(),
            EnsureKmsKeyPolicyNotUseWildcard(),
            EnsureRestApiGwPolicyNotUseWildcard(),
            EnsureCloudWatchLogDestinationPolicyNotUseWildcard(),
            EnsureElasticSearchDomainPolicyNotUseWildcard(),
            EnsureEfsPolicyNotUseWildcard(),
            EnsureGlacierVaultPolicyNotUseWildcard(),
            EnsureGlueDataCatalogPolicyNotUseWildcard(),
            EnsureSecretsManagerSecretPolicyNotUseWildcard(),
            EnsureDocdbClustersEncryptedInTransitRule(),
            EnsureDocdbClustersEncryptedCustomerManagedCmkRule(),
            EnsureEfsFilesystemsEncryptedAtRestRule(),
            EnsureApiGwUseModernTlsRule(),
            EnsureCloudfrontDistributionFieldLevelEncryptionRule(),
            EnsureKinesisStreamEncryptedAtRestRule(),
            EnsureXrayEncryptionCmkRule(),
            EnsureKinesisFirehoseStreamEncryptedAtRestRule(),
            EnsureWorkspaceRootVolumeEncryptedAtRestRule(),
            EnsureWorkspaceRootVolumeEncryptionCmkRule(),
            EnsureWorkspaceUserVolumeEncryptedAtRestRule(),
            EnsureWorkspaceUserVolumeEncryptedAtRestWithCustomerManagedCmkRule(),
            EnsureIamPasswordExpiration(),
            EnsureIamPasswordMinimumLength(),
            EnsureIamPasswordLowerCharacters(),
            EnsureIamPasswordRequiresNumber(),
            EnsureIamPasswordNotAllowReuse(),
            EnsureIamPasswordRequiresSymbol(),
            EnsureIamPasswordRequiresUpperCase(),
            EnsureS3BucketsPolicyUseHttpsRule(),
            EnsureCloudWatchLogGroupsRetentionUsageRule(),
            EnsureCloudTrailLogValidationEnabledRule(),
            PublicAccessSecurityGroupsAllPortsRule(),
            EnsureLambdaFunctionPolicyNotUseWildcard(),
            EnsureSecurityGroupIncludeDescriptionRule(),
            EnsureNoReadOnlyAccessPolicyUsedByRoleUserRule(),
            EnsureIamEntitiesPolicyManagedSolely(),
            PublicAccessDbNeptuneRule(),
            EnsureEcsTaskDefinitionCreatedWithEfsEncryptInTransitRule(),
            SqsVpcEndpointExposureRule(),
            SqsVpcEndpointInterfaceAvailabilityZoneRule(),
            EnsureLambdaFunctionHasNonInfiniteLogRetentionRule(),
            EnsureSsmParameterStoreUsingEncryptedCustomerManagedKmsRule(),
            Ec2VpcEndpointExposureRule(),
            EnsureAllResourcesTaggedRule(),
            EnsureSageMakerEndpointConfigEncryptedAtRestRule(),
            EnsureSageMakerNotebookInstanceEncryptedAtRestByCMKRule(),
            IamRoleAssumeRolePrincipalTooWide(),
            S3BucketLambdaIndirectExposureRule(),
            PublicAccessDmsReplicationInstanceRule(),
            AccessAnalyzerValidationWarningAndSuggestionRule(),
            AccessAnalyzerValidationErrorAndSecurityRule(),
            EnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule(),
            EnsureNoUnusedSecurityGroups(),
            EnsureUnusedRolesRemoved(),
            EnsureEcrImageScanningOnPushEnabledRule(),
            EnsureEcrRepositoryImageTagsImmutableRule(),
            EnsureElasticacheRedisClusterAutoBackupEnabledRule(),
            EnsureEcrRepositoriesEncryptedAtRestWithCustomerManagedCmkRule(),
            CloudFrontEnsureWafUsedRule(),
            EnsureLoadBalancerDropsInvalidHttpHeadersRule(),
            EnsureCloudtrailMultiregionEnabledRule(),
            EnsureDynamoDbTableEncryptedAtRestWithCustomerManagedCmkRule(),
            EnsureEcsClusterEnableContainerInsightsRule(),
            EnsureEc2InstanceEbsOptimizedRule(),
            EnsureRdsResourceBackupRetentionEnabledRule(),
            EnsureRestApiMethodUseAuthenticationRule(),
            EnsureRdsResourceIamAuthenticationEnabledRule(),
            EnsureConfigAggregatorEnabledAllRegionsRule(),
            EnsureApiGwXrayTracingEnabledRule(),
            EnsureCloudfrontDistributionListAccessLoggingEnabledRule(),
            EnsureDocdbLoggingEnabledRule(),
            EnsureEc2InstanceDetailedMonitoringEnabledRule(),
            EnsureElasticsearchDomainLoggingEnabledRule(),
            EnsureLoadBalancerLoggingEnabledRule(),
            EnsureGlobalAccelerationFlowLogsEnabledRule(),
            EnsureLambdaFunctionXrayTracingEnabledRule(),
            EnsureNeptuneClusterLoggingEnabledRule(),
            EnsureRdsResourceLoggingEnabledRule(),
            EnsureRedshiftClusterLoggingEnabledRule(),
            EnsureRestApiGwAccessLoggingEnabledRule(),
            EnsureS3BucketLoggingEnabledRule(),
            EnsureCloudtrailTrailExists(),
            EnsureAthenaDatabaseEncryptedAtRestRule(),
            EnsureLambdaFunctionCannotBeInvokedPublicRule(),
            FsxWindowsFileSystemEncryptedAtRestWithCustomerManagedCmkRule(),
            EnsureLambdaFunctionCannotBeInvokedPublicRule(),
        ]
        return {rule.get_id(): rule for rule in rules}
