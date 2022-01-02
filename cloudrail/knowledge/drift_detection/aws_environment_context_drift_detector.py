from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_domain import RestApiGwDomain
from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw_mapping import RestApiGwMapping
from cloudrail.knowledge.context.aws.resources.athena.athena_database import AthenaDatabase
from cloudrail.knowledge.context.aws.resources.cloudhsmv2.cloudhsm_v2_cluster import CloudHsmV2Cluster
from cloudrail.knowledge.context.aws.resources.cloudhsmv2.cloudhsm_v2_hsm import CloudHsmV2Hsm
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route import TransitGatewayRoute
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table import TransitGatewayRouteTable
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_route_table_propagation import TransitGatewayRouteTablePropagation
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint_route_table_association import VpcEndpointRouteTableAssociation
from cloudrail.knowledge.context.aws.resources.glue.glue_connection import GlueConnection
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group_association import LoadBalancerTargetGroupAssociation
from cloudrail.knowledge.context.aws.resources.iam.iam_group_membership import IamGroupMembership
from cloudrail.knowledge.context.aws.resources.iam.iam_policy_attachment import IamPolicyAttachment
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_object import S3BucketObject
from cloudrail.knowledge.context.aws.resources.s3outposts.s3outpost_endpoint import S3OutpostEndpoint
from cloudrail.knowledge.context.aws.resources.worklink.worklink_fleet import WorkLinkFleet
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.drift_detection.base_environment_context_drift_detector import BaseEnvironmentContextDriftDetector


class AwsEnvironmentContextDriftDetector(BaseEnvironmentContextDriftDetector):

    @classmethod
    def supported_drift_resource(cls, mergeable: Mergeable) -> bool:
        return not (isinstance(mergeable, (AthenaDatabase, GlueConnection, WorkLinkFleet,
                                           S3OutpostEndpoint, CloudHsmV2Hsm, CloudHsmV2Cluster,
                                           S3BucketObject, TransitGatewayRouteTablePropagation, IamGroupMembership,
                                           VpcEndpointRouteTableAssociation, IamPolicyAttachment, RestApiGwDomain,
                                           RestApiGwMapping, LoadBalancerTargetGroupAssociation, TransitGatewayRoute,
                                           TransitGatewayRouteTable)))
