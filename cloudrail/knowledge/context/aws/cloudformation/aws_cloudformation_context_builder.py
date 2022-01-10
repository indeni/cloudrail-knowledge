from typing import Dict, List, Optional

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_utils import CloudformationUtils
from cloudrail.knowledge.context.aws.resources.cloudformation.cloudformation_resource_info import CloudformationResourceInfo
from cloudrail.knowledge.context.aws.resources.cloudformation.cloudformation_resource_status import CloudformationResourceStatus
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.dms.cloudformation_dms_replication_instance_builder import \
    CloudformationDmsReplicationInstanceBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.dms.cloudformation_dms_replication_instance_subnet_group_builder import \
    CloudformationDmsReplicationInstanceSubnetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.eks.cloudformation_eks_cluster_builder import CloudformationEksClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_iam_instance_profile_builder import CloudformationIamInstanceProfileBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.docdb.cloudformation_docdb_cluster_builder import CloudformationDocumentDbClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.docdb.cloudformation_docdb_cluster_parameter_group_builder import CloudformationDocDbClusterParameterGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_iam_policies_attachment_builder import \
    CloudformationPolicyRoleAttachmentBuilder, CloudformationPolicyGroupAttachmentBuilder, CloudformationPolicyUserAttachmentBuilder, \
    CloudformationIamPolicyAttachmentGroupBuilder, CloudformationIamPolicyAttachmentUserBuilder, CloudformationIamPolicyAttachmentRoleBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_iam_user_builder import CloudformationIamUserBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_iam_group_builder import CloudformationIamGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_iam_user_login_profile_builder import CloudformationIamUsersLoginProfileBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.cloudformation_load_balancer_attributes_builder import CloudformationLoadBalancerAttributesBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.kms.cloudformation_kms_key_policy_builder import CloudformationKmsKeyPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.nat_gw.cloudformation_nat_gw_builder import CloudformationNatGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.dynamodb.cloudformation_dynamodb_table_builder import CloudformationDynamoDbTableBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.codebuild.cloudformation_codebuild_project_builder import CloudformationCodeBuildProjectBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.configservice.cloudformation_config_service_aggregator_builder import CloudformationConfigServiceAggregatorBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_network_acl_builder import \
    CloudformationNetworkAclAssociationBuilder, CloudformationNetworkAclBuilder, NetworkAclRuleBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_vpc_endpoint_builder import CloudformationVpcEndpointBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_iam_role_builder import CloudformationIamRoleBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_iam_policies_builder import \
    CloudformationAssumeRolePolicyBuilder, CloudformationInlinePolicyFromRoleBuilder, CloudformationInlinePolicyRoleBuilder, CloudformationManagedPolicyBuilder, \
    CloudformationS3BucketPolicyBuilder, CloudformationInlinePolicyFromUserBuilder, CloudformationInlinePolicyUserBuilder, CloudformationInlinePolicyFromGroupBuilder, \
    CloudformationInlinePolicyGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.lambda_function.cloudformation_lambda_function_builder import \
    CloudformationLambdaFunctionBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.rds.cloudformation_rds_cluster_builder import CloudformationRdsClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.rds.cloudformation_rds_instance_builder import CloudformationRdsInstanceBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.rds.cloudformation_rds_db_subnet_group_builder import CloudformationRdsDbSubnetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.rds.cloudformation_rds_global_cluster_builder import CloudformationRdsGlobalClusterBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.s3_bucket.cloudformation_public_access_block_settings_builder import \
    CloudformationPublicAccessBlockSettingsBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.vpc_gateway.cloudformation_transit_gateway_attachment_builder import \
    CloudformationTransitGatewayAttachmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.vpc_gateway.cloudformation_transit_gateway_builder import \
    CloudformationTransitGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.vpc_gateway.cloudformation_transit_gateway_route_table_builder import \
    CloudformationTransitGatewayRouteTableBuilder, CloudformationTransitGatewayRouteTableAssociationBuilder, CloudformationTransitGatewayRouteBuilder
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_metadata_parser import CloudformationMetadataParser
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.api_gateway.v2.cloudformation_api_gateway_v2_builder import \
    CloudformationApiGatewayV2Builder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.api_gateway.v2.cloudformation_api_gateway_v2_integration_builder import \
    CloudformationApiGatewayV2IntegrationBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.api_gateway.v2.cloudformation_api_gateway_v2_vpc_link_builder import \
    CloudformationApiGatewayV2VpcLinkBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.athena.cloudformation_athena_workgroup_builder import \
    CloudformationAthenaWorkgroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.kms.cloudformation_kms_key_builder import CloudformationKmsKeyBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.kms.cloudformation_kms_alias_builder import CloudformationKmsAliasBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.batch.cloudformation_batch_compute_environment_builder import \
    CloudformationBatchComputeEnvironmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.cloudtrail.cloudfromation_cloudtrail_builder import \
    CloudformationCloudtrailBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.cloudfront.cloudformation_cloudfront_distribution_logging_builder import \
    CloudformationCloudfrontDistributionLoggingBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.cloudfront.cloudformation_cloudfront_distribution_list_builder import \
    CloudformationCloudfrontDistributionListBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.cloudwatch.cloudformation_cloudwatch_logs_destination_builder import \
    CloudformationCloudwatchLogsDestinationBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.cloudwatch.cloudformation_cloudwatch_logs_destination_builder import \
    CloudformationCloudwatchLogsDestinationPolicyBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.codebuild.cloudformation_codebuild_report_group_builder import \
    CloudformationCodebuildReportGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_ec2_builder import CloudformationEc2Builder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_elastic_ip_builder import CloudformationElasticIpBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_internet_gateway_builder import \
    CloudformationInternetGatewayBuilder, CloudformationEgressOnlyInternetGatewayBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_route_builder import CloudformationRouteBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_route_table_builder import CloudformationRouteTable
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_security_group_builder import \
    CloudformationSecurityGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_security_group_egress_rule_builder import \
    CloudformationSecurityGroupEgressRuleBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_security_group_ingress_rule_builder import \
    CloudformationSecurityGroupIngressRuleBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_security_group_inline_rule_builder import \
    CloudformationSecurityGroupInlineRuleBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_subnet_builder import CloudformationSubnetBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_subnet_route_table_association_builder import \
    CloudformationSubnetRouteTableAssociationBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.cloudfront.cloudformation_cloudfront_origin_access_identity_builder import \
    CloudformationCloudfrontOriginAccessIdentityBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_vpc_builder import CloudformationVpcBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_vpc_gateway_attachment_builder import \
    CloudformationVpcGatewayAttachmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.cloudformation_load_balancer_builder import \
    CloudformationLoadBalancerBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.cloudformation_load_balancer_listener_builder import \
    CloudformationLoadBalancerListenerBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.cloudformation_load_balancer_target_builder import \
    CloudformationLoadBalancerTargetBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.\
    cloudformation_load_balancer_target_group_association_builder import CloudformationLoadBalancerTargetGroupAssociationBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.cloudformation_load_balancer_target_group_builder import \
    CloudformationLoadBalancerTargetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.s3_bucket.cloudformation_s3_bucket_builder import \
    CloudformationS3BucketBuilder, CloudformationS3BucketEncryptionBuilder, CloudformationS3BucketVersioningBuilder, \
        CloudformationS3BucketLoggingBuilder, CloudformationS3BucketAclBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.autoscaling.cloudformation_auto_scaling_group_builder import CloudformationAutoScalingGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.autoscaling.cloudformation_launch_configuration_builder import CloudformationLaunchConfigurationBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.autoscaling.cloudformation_launch_template_builder import CloudformationLaunchTemplateBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.kinesis.cloudformation_kinesis_stream_builder import CloudformationKinesisStreamBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.dax.cloudformation_dax_cluster_builder import CloudformationDaxClusterBuilder
from cloudrail.knowledge.context.environment_context.iac_context_builder import IacContextBuilder
from cloudrail.knowledge.context.aws.aws_relations_assigner import AwsRelationsAssigner


class AwsCloudformationContextBuilder(IacContextBuilder):

    @staticmethod
    def build(iac_file: str,
              account_id: str = None,
              scanner_environment_context: Optional[BaseEnvironmentContext] = None,
              salt: Optional[str] = None,
              **extra_args) -> AwsEnvironmentContext:
        if not iac_file:
            return AwsEnvironmentContext()
        template_content: dict = CloudformationUtils.load_cfn_template(iac_file)
        iac_url_template: Optional[str] = extra_args.get('iac_url_template')
        extra_params: dict = template_content.get(CloudformationUtils.EXTRA_PARAMETERS_KEY, {})
        region = extra_params.get('region') or extra_args.get('region')
        stack_name = extra_params.get('stack_name') or extra_args.get('stack_name')
        extra_params.update(extra_args.get('cfn_template_params', {}))
        if not region:
            raise Exception('missing \'region\' parameter')

        if scanner_environment_context:
            AwsRelationsAssigner(scanner_environment_context).run()
            scanner_environment_context.clear_cache()
            if account := scanner_environment_context.accounts.get(account_id):
                if not account_id:
                    account_id = account.account
        else:
            scanner_environment_context = AwsEnvironmentContext()

        logical_to_physical_id_map: Dict[str, str] = AwsCloudformationContextBuilder.create_logical_to_physical_id_map(scanner_environment_context,
                                                                                                                       stack_name)
        cfn_template_params = AwsCloudformationContextBuilder._add_extra_params_to_template_params(cfn_template_params=extra_params,
                                                                                                   stack_name=stack_name,
                                                                                                   account_id=account_id,
                                                                                                   region=region)
        cfn_parser: CloudformationMetadataParser = CloudformationMetadataParser(
            cfn_template_file=iac_file,
            logical_to_physical_id_map=logical_to_physical_id_map,
            cfn_template_params=cfn_template_params,
            scanner_context=scanner_environment_context,
            logical_id_to_resource_info_map=AwsCloudformationContextBuilder.create_logical_id_to_resource_info_map(scanner_environment_context,
                                                                                                                   stack_name))

        cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]] = cfn_parser.parse(iac_url_template, salt)

        security_groups: List[SecurityGroup] = CloudformationSecurityGroupBuilder(cfn_by_type_map).build()
        security_groups_rules = CloudformationSecurityGroupEgressRuleBuilder(cfn_by_type_map).build() + \
                                CloudformationSecurityGroupIngressRuleBuilder(cfn_by_type_map).build() + \
                                CloudformationSecurityGroupInlineRuleBuilder(cfn_by_type_map).build()
        role_inline_policies = CloudformationInlinePolicyFromRoleBuilder(cfn_by_type_map).build() +\
                               CloudformationInlinePolicyRoleBuilder(cfn_by_type_map).build()
        user_inline_policies = CloudformationInlinePolicyFromUserBuilder(cfn_by_type_map).build() +\
                               CloudformationInlinePolicyUserBuilder(cfn_by_type_map).build()
        group_inline_policies = CloudformationInlinePolicyFromGroupBuilder(cfn_by_type_map).build() +\
                                CloudformationInlinePolicyGroupBuilder(cfn_by_type_map).build()
        iam_policy_attachments = CloudformationIamPolicyAttachmentGroupBuilder(cfn_by_type_map).build() +\
                                 CloudformationIamPolicyAttachmentRoleBuilder(cfn_by_type_map).build() +\
                                 CloudformationIamPolicyAttachmentUserBuilder(cfn_by_type_map).build()


        return AwsEnvironmentContext(
            nat_gateway_list=CloudformationNatGatewayBuilder(cfn_by_type_map).build(),
            vpcs=AliasesDict(*CloudformationVpcBuilder(cfn_by_type_map).build()),
            s3_buckets=AliasesDict(*CloudformationS3BucketBuilder(cfn_by_type_map).build()),
            s3_bucket_encryption=CloudformationS3BucketEncryptionBuilder(cfn_by_type_map).build(),
            s3_bucket_versioning=CloudformationS3BucketVersioningBuilder(cfn_by_type_map).build(),
            s3_bucket_logs=CloudformationS3BucketLoggingBuilder(cfn_by_type_map).build(),
            athena_workgroups=CloudformationAthenaWorkgroupBuilder(cfn_by_type_map).build(),
            kms_keys=CloudformationKmsKeyBuilder(cfn_by_type_map).build(),
            security_groups=AliasesDict(*security_groups),
            security_group_rules=security_groups_rules,
            dms_replication_instance_subnet_groups=CloudformationDmsReplicationInstanceSubnetGroupBuilder(cfn_by_type_map).build(),
            dms_replication_instances=CloudformationDmsReplicationInstanceBuilder(cfn_by_type_map).build(),
            internet_gateways=CloudformationInternetGatewayBuilder(cfn_by_type_map).build() + CloudformationEgressOnlyInternetGatewayBuilder(cfn_by_type_map).build(),
            vpc_gateway_attachment=AliasesDict(*CloudformationVpcGatewayAttachmentBuilder(cfn_by_type_map).build()),
            subnets=AliasesDict(*CloudformationSubnetBuilder(cfn_by_type_map).build()),
            route_tables=AliasesDict(*CloudformationRouteTable(cfn_by_type_map).build()),
            routes=CloudformationRouteBuilder(cfn_by_type_map).build(),
            route_table_associations=CloudformationSubnetRouteTableAssociationBuilder(cfn_by_type_map).build(),
            load_balancers=CloudformationLoadBalancerBuilder(cfn_by_type_map).build(),
            load_balancer_listeners=CloudformationLoadBalancerListenerBuilder(cfn_by_type_map).build(),
            load_balancer_target_groups=CloudformationLoadBalancerTargetGroupBuilder(cfn_by_type_map).build(),
            load_balancer_targets=CloudformationLoadBalancerTargetBuilder(cfn_by_type_map).build(),
            load_balancer_target_group_associations=CloudformationLoadBalancerTargetGroupAssociationBuilder(cfn_by_type_map).build(),
            api_gateways_v2=CloudformationApiGatewayV2Builder(cfn_by_type_map).build(),
            api_gateway_v2_vpc_links=CloudformationApiGatewayV2VpcLinkBuilder(cfn_by_type_map).build(),
            api_gateway_v2_integrations=CloudformationApiGatewayV2IntegrationBuilder(cfn_by_type_map).build(),
            cloudtrail=CloudformationCloudtrailBuilder(cfn_by_type_map).build(),
            codebuild_report_groups=CloudformationCodebuildReportGroupBuilder(cfn_by_type_map).build(),
            batch_compute_environments=CloudformationBatchComputeEnvironmentBuilder(cfn_by_type_map).build(),
            ec2s=CloudformationEc2Builder(cfn_by_type_map).build(),
            elastic_ips=CloudformationElasticIpBuilder(cfn_by_type_map).build(),
            roles=CloudformationIamRoleBuilder(cfn_by_type_map).build(),
            users=CloudformationIamUserBuilder(cfn_by_type_map).build(),
            groups=CloudformationIamGroupBuilder(cfn_by_type_map).build(),
            assume_role_policies=CloudformationAssumeRolePolicyBuilder(cfn_by_type_map).build(),
            role_inline_policies=role_inline_policies,
            user_inline_policies=user_inline_policies,
            group_inline_policies=group_inline_policies,
            s3_bucket_policies=CloudformationS3BucketPolicyBuilder(cfn_by_type_map).build(),
            dynamodb_table_list=CloudformationDynamoDbTableBuilder(cfn_by_type_map).build(),
            aws_config_aggregators=CloudformationConfigServiceAggregatorBuilder(cfn_by_type_map).build(),
            auto_scaling_groups=CloudformationAutoScalingGroupBuilder(cfn_by_type_map).build(),
            launch_configurations=CloudformationLaunchConfigurationBuilder(cfn_by_type_map).build(),
            launch_templates=CloudformationLaunchTemplateBuilder(cfn_by_type_map).build(),
            cloudwatch_logs_destinations=CloudformationCloudwatchLogsDestinationBuilder(cfn_by_type_map).build(),
            cloudwatch_logs_destination_policies=CloudformationCloudwatchLogsDestinationPolicyBuilder(cfn_by_type_map).build(),
            cloudfront_log_settings=CloudformationCloudfrontDistributionLoggingBuilder(cfn_by_type_map).build(),
            cloudfront_distribution_list=CloudformationCloudfrontDistributionListBuilder(cfn_by_type_map).build(),
            vpc_endpoints=CloudformationVpcEndpointBuilder(cfn_by_type_map).build(),
            lambda_function_list=CloudformationLambdaFunctionBuilder(cfn_by_type_map).build(),
            network_acls=AliasesDict(*CloudformationNetworkAclBuilder(cfn_by_type_map).build()),
            network_acl_associations=AliasesDict(*CloudformationNetworkAclAssociationBuilder(cfn_by_type_map).build()),
            network_acl_rules=NetworkAclRuleBuilder(cfn_by_type_map).build(),
            dax_cluster=CloudformationDaxClusterBuilder(cfn_by_type_map).build(),
            s3_public_access_block_settings_list=CloudformationPublicAccessBlockSettingsBuilder(cfn_by_type_map).build(),
            iam_instance_profiles=CloudformationIamInstanceProfileBuilder(cfn_by_type_map).build(),
            transit_gateway_attachments=CloudformationTransitGatewayAttachmentBuilder(cfn_by_type_map).build(),
            transit_gateways=CloudformationTransitGatewayBuilder(cfn_by_type_map).build(),
            transit_gateway_route_tables=CloudformationTransitGatewayRouteTableBuilder(cfn_by_type_map).build(),
            transit_gateway_route_table_associations=CloudformationTransitGatewayRouteTableAssociationBuilder(cfn_by_type_map).build(),
            transit_gateway_routes=CloudformationTransitGatewayRouteBuilder(cfn_by_type_map).build(),
            codebuild_projects=CloudformationCodeBuildProjectBuilder(cfn_by_type_map).build(),
            docdb_cluster=CloudformationDocumentDbClusterBuilder(cfn_by_type_map).build(),
            docdb_cluster_parameter_groups=CloudformationDocDbClusterParameterGroupBuilder(cfn_by_type_map).build(),
            load_balancers_attributes=CloudformationLoadBalancerAttributesBuilder(cfn_by_type_map).build(),
            kms_aliases=CloudformationKmsAliasBuilder(cfn_by_type_map).build(),
            kms_keys_policies=CloudformationKmsKeyPolicyBuilder(cfn_by_type_map).build(),
            kinesis_streams=CloudformationKinesisStreamBuilder(cfn_by_type_map).build(),
            origin_access_identity_list=CloudformationCloudfrontOriginAccessIdentityBuilder(cfn_by_type_map).build(),
            s3_bucket_acls=CloudformationS3BucketAclBuilder(cfn_by_type_map).build(),
            policies=CloudformationManagedPolicyBuilder(cfn_by_type_map).build(),
            policy_role_attachments=CloudformationPolicyRoleAttachmentBuilder(cfn_by_type_map).build(),
            policy_group_attachments=CloudformationPolicyGroupAttachmentBuilder(cfn_by_type_map).build(),
            policy_user_attachments=CloudformationPolicyUserAttachmentBuilder(cfn_by_type_map).build(),
            users_login_profile=CloudformationIamUsersLoginProfileBuilder(cfn_by_type_map).build(),
            iam_policy_attachments=iam_policy_attachments,
            eks_clusters=CloudformationEksClusterBuilder(cfn_by_type_map).build(),
            rds_clusters=CloudformationRdsClusterBuilder(cfn_by_type_map).build(),
            rds_instances=CloudformationRdsInstanceBuilder(cfn_by_type_map).build(),
            db_subnet_groups=CloudformationRdsDbSubnetGroupBuilder(cfn_by_type_map).build(),
            rds_global_clusters=CloudformationRdsGlobalClusterBuilder(cfn_by_type_map).build(),
        )

    @staticmethod
    def _add_extra_params_to_template_params(cfn_template_params: dict, stack_name: str,
                                             account_id: str = None, region: str = None) -> dict:
        cfn_template_params = cfn_template_params or {}
        if stack_name:
            cfn_template_params['stack_name'] = stack_name
        if region:
            cfn_template_params['region'] = region

        cfn_template_params['account_id'] = account_id or '000000000000'
        return cfn_template_params

    @classmethod
    def create_logical_to_physical_id_map(cls, scanner_context: AwsEnvironmentContext, stack_name: str) -> Dict[str, str]:
        return {resource_info.logical_resource_id: resource_info.physical_resource_id
                for resource_info in cls.create_logical_id_to_resource_info_map(scanner_context, stack_name).values()}

    @staticmethod
    def create_logical_id_to_resource_info_map(scanner_context: AwsEnvironmentContext, stack_name: str) -> Dict[str, CloudformationResourceInfo]:
        logical_id_to_resource_map: Dict[str, CloudformationResourceInfo] = {}
        for cfn_resource in scanner_context.cfn_resources_info:
            if cfn_resource.resource_status in (CloudformationResourceStatus.CREATE_COMPLETE, CloudformationResourceStatus.ROLLBACK_COMPLETE,
                                                CloudformationResourceStatus.UPDATE_COMPLETE, CloudformationResourceStatus.UPDATE_ROLLBACK_COMPLETE,
                                                CloudformationResourceStatus.IMPORT_COMPLETE,
                                                CloudformationResourceStatus.IMPORT_ROLLBACK_COMPLETE) and stack_name == cfn_resource.stack_name:
                logical_id_to_resource_map[cfn_resource.logical_resource_id] = cfn_resource
        return logical_id_to_resource_map
