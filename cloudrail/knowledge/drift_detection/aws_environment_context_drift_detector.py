from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.aws.resources.athena.athena_database import AthenaDatabase
from cloudrail.knowledge.context.aws.resources.cloudhsmv2.cloudhsm_v2_cluster import CloudHsmV2Cluster
from cloudrail.knowledge.context.aws.resources.cloudhsmv2.cloudhsm_v2_hsm import CloudHsmV2Hsm
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table_propagation import TransitGatewayRouteTablePropagation
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint_route_table_association import VpcEndpointRouteTableAssociation
from cloudrail.knowledge.context.aws.resources.glue.glue_connection import GlueConnection
from cloudrail.knowledge.context.aws.resources.iam.iam_group_membership import IamGroupMembership
from cloudrail.knowledge.context.aws.resources.iam.iam_policy_attachment import IamPolicyAttachment
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_object import S3BucketObject
from cloudrail.knowledge.context.aws.resources.s3outposts.s3outpost_endpoint import S3OutpostEndpoint
from cloudrail.knowledge.context.aws.resources.worklink.worklink_fleet import WorkLinkFleet
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_domain import RestApiGwDomain
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_mapping import RestApiGwMapping
from typing import Set

from cloudrail.knowledge.drift_detection.base_environment_context_drift_detector import BaseEnvironmentContextDriftDetector


class AwsEnvironmentContextDriftDetector(BaseEnvironmentContextDriftDetector):

    @classmethod
    def get_excluded_attributes(cls) -> Set[str]:
        return {'is_managed_by_iac',
                'origin',
                'uuid',
                'creation_date',
                'function_version',
                'policy_evaluation_result_map',
                'aliases',
                'is_pseudo',
                'subnets_by_az_map',
                'account',
                'property_type',
                'AWS_CONSOLE_URL',
                'GLOBAL_REGION',
                'is_invalidated',
                'is_tagable',
                'iac_state',
                'policy_attach_origin_map',
                'friendly_name',
                'is_used',
                'tf_resource_type',
                'raw_data',
                'network_resource',
                'inbound_connections',
                'outbound_connections',
                'publicly_allowing_resources',
                'is_public',
                'invalidation',
                'exposed_to_agw_methods',
                'acls',
                'parameters',
                'policy_to_escalation_actions_map',
                'is_ever_used',
                'api_gw_stages',
                'bucket_objects',
                'permissions_policies',
                'subnets',
                'elasticache_security_group_ids',
                'elasticache_subnet_ids',
                'agw_methods_with_valid_integrations_and_allowed_lambda_access',
                'role_id',
                'policy_id',
                'queue_url',
                'raw_document',
                'lambda_func_arn_set',
                'arn',
                'lambda_func_version',
                'qualified_arn',
                'owner_id',
                'owner_name',
                'groups_attach_origin_map'}

    @classmethod
    def supported_drift_resource(cls, mergeable: Mergeable) -> bool:
        return not (isinstance(mergeable, (AthenaDatabase, GlueConnection, WorkLinkFleet,
                                           S3OutpostEndpoint, CloudHsmV2Hsm, CloudHsmV2Cluster,
                                           S3BucketObject, TransitGatewayRouteTablePropagation, IamGroupMembership,
                                           VpcEndpointRouteTableAssociation, IamPolicyAttachment, RestApiGwDomain,
                                           RestApiGwMapping)))
