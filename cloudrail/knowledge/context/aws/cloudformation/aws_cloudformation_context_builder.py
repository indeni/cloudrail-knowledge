from typing import Dict, List, Optional

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_utils import CloudformationUtils
from cloudrail.knowledge.context.aws.resources.cloudformation.cloudformation_resource_info import CloudformationResourceInfo
from cloudrail.knowledge.context.aws.resources.cloudformation.cloudformation_resource_status import CloudformationResourceStatus
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
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
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.athena.cloudformation_kms_key_builder import CloudformationKmsKeyBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.batch.cloudformation_batch_compute_environment_builder import \
    CloudformationBatchComputeEnvironmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.cloudtrail.cloudfromation_cloudtrail_builder import \
    CloudformationCloudtrailBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.codebuild.cloudformation_codebuild_report_group_builder import \
    CloudformationCodebuildReportGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_ec2_builder import CloudformationEc2Builder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_elastic_ip_builder import CloudformationElasticIpBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_internet_gateway_builder import \
    CloudformationInternetGatewayBuilder
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
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_vpc_builder import CloudformationVpcBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.ec2.cloudformation_vpc_gateway_attachment_builder import \
    CloudformationVpcGatewayAttachmentBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.cloudformation_load_balancer_builder import \
    CloudformationLoadBalancerBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.cloudformation_load_balancer_listener_builder import \
    CloudformationLoadBalancerListenerBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.cloudformation_load_balancer_target_builder import \
    CloudformationLoadBalancerTargetBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.cloudformation_load_balancer_target_group_association_builder import \
    CloudformationLoadBalancerTargetGroupAssociationBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.load_balancer.cloudformation_load_balancer_target_group_builder import \
    CloudformationLoadBalancerTargetGroupBuilder
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.s3_bucket.cloudformation_s3_bucket_builder import \
    CloudformationS3BucketBuilder, \
    CloudformationS3BucketEncryptionBuilder, CloudformationS3BucketVersioningBuilder, CloudformationS3BucketLoggingBuilder
from cloudrail.knowledge.context.environment_context.iac_context_builder import IacContextBuilder


class AwsCloudformationContextBuilder(IacContextBuilder):

    @staticmethod
    def build(iac_file: str,
              account_id: str = None,
              scanner_environment_context: Optional[BaseEnvironmentContext] = None,
              salt: Optional[str] = None,
              **extra_args) -> AwsEnvironmentContext:
        template_content: dict = CloudformationUtils.load_cfn_template(iac_file)
        iac_url_template: Optional[str] = extra_args.get('iac_url_template')
        extra_params: dict = template_content.get(CloudformationUtils.EXTRA_PARAMETERS_KEY, {})
        region = extra_params.get('region') or extra_args.get('region')
        stack_name = extra_params.get('stack_name') or extra_args.get('stack_name')
        extra_params.update(extra_args.get('cfn_template_params', {}))
        if not region:
            raise Exception('missing \'region\' parameter')

        if scanner_environment_context:
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

        return AwsEnvironmentContext(
            vpcs=AliasesDict(*CloudformationVpcBuilder(cfn_by_type_map).build()),
            s3_buckets=AliasesDict(*CloudformationS3BucketBuilder(cfn_by_type_map).build()),
            s3_bucket_encryption=CloudformationS3BucketEncryptionBuilder(cfn_by_type_map).build(),
            s3_bucket_versioning=CloudformationS3BucketVersioningBuilder(cfn_by_type_map).build(),
            s3_bucket_logs=CloudformationS3BucketLoggingBuilder(cfn_by_type_map).build(),
            athena_workgroups=CloudformationAthenaWorkgroupBuilder(cfn_by_type_map).build(),
            kms_keys=CloudformationKmsKeyBuilder(cfn_by_type_map).build(),
            security_groups=AliasesDict(*security_groups),
            security_group_rules=security_groups_rules,
            internet_gateways=CloudformationInternetGatewayBuilder(cfn_by_type_map).build(),
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
            elastic_ips=CloudformationElasticIpBuilder(cfn_by_type_map).build()
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
        for cfn_resource in scanner_context.cfn_resources_info:  # todo - convert 'cfn_resources_info' to aliases
            if cfn_resource.resource_status in (CloudformationResourceStatus.CREATE_COMPLETE, CloudformationResourceStatus.ROLLBACK_COMPLETE,
                                                CloudformationResourceStatus.UPDATE_COMPLETE, CloudformationResourceStatus.UPDATE_ROLLBACK_COMPLETE,
                                                CloudformationResourceStatus.IMPORT_COMPLETE,
                                                CloudformationResourceStatus.IMPORT_ROLLBACK_COMPLETE) and stack_name == cfn_resource.stack_name:
                logical_id_to_resource_map[cfn_resource.logical_resource_id] = cfn_resource
        return logical_id_to_resource_map
