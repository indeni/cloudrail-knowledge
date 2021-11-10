from typing import Dict, Callable, Optional, Type

from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2 import ApiGateway
from cloudrail.knowledge.context.aws.resources.cloudfront.origin_access_identity import OriginAccessIdentity
from cloudrail.knowledge.context.aws.resources.dax.dax_cluster import DaxCluster
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_list import CloudFrontDistribution
from cloudrail.knowledge.context.aws.resources.cloudtrail.cloudtrail import CloudTrail
from cloudrail.knowledge.context.aws.resources.codebuild.codebuild_project import CodeBuildProject
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloudwatch_logs_destination import CloudWatchLogsDestination
from cloudrail.knowledge.context.aws.resources.codebuild.codebuild_report_group import CodeBuildReportGroup
from cloudrail.knowledge.context.aws.resources.configservice.config_aggregator import ConfigAggregator
from cloudrail.knowledge.context.aws.resources.dynamodb.dynamodb_table import DynamoDbTable
from cloudrail.knowledge.context.aws.resources.ec2.elastic_ip import ElasticIp
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway import TransitGateway
from cloudrail.knowledge.context.aws.resources.ec2.transit_gateway_vpc_attachment import TransitGatewayVpcAttachment
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpointInterface
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_listener import LoadBalancerListener
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.iam.iam_instance_profile import IamInstanceProfile
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.kinesis.kinesis_stream import KinesisStream

class CloudformationAttributesCallableStore:

    @staticmethod
    def get_s3_bucket_attribute(s3_bucket: S3Bucket, attribute_name: str):
        if attribute_name == 'Arn':
            return s3_bucket.arn
        if attribute_name == 'DomainName':
            return s3_bucket.bucket_domain_name
        if attribute_name == 'DualStackDomainName':
            return None
        if attribute_name == 'RegionalDomainName':
            return s3_bucket.bucket_regional_domain_name
        if attribute_name == 'WebsiteURL':
            return None
        return None

    @staticmethod
    def get_vpc_attribute(vpc: Vpc, attribute_name: str):
        if attribute_name == "CidrBlock" and vpc.cidr_block:
            return vpc.cidr_block[0]
        if attribute_name == 'CidrBlockAssociations':
            return None
        if attribute_name == "DefaultNetworkAcl" and vpc.default_nacl:
            return vpc.default_nacl.network_acl_id
        if attribute_name == "DefaultSecurityGroup" and vpc.default_security_group:
            return vpc.default_security_group.security_group_id
        if attribute_name == "Ipv6CidrBlocks":
            return None
        return None

    @staticmethod
    def get_vpc_internet_gateway_attribute(internet_gateway: InternetGateway, attribute_name: str):
        if attribute_name == "Tags":
            return internet_gateway.tags
        return None

    @staticmethod
    def get_security_group_attribute(security_group: SecurityGroup, attribute_name: str):
        if attribute_name == "GroupId":
            return security_group.security_group_id
        if attribute_name == "VpcId":
            return security_group.vpc_id
        return None

    @staticmethod
    def get_load_balancer_attribute(load_balancer: LoadBalancer, attribute_name: str):
        if attribute_name == "CanonicalHostedZoneID":
            return None
        if attribute_name == "DNSName":
            return None
        if attribute_name == "LoadBalancerFullName":
            return None
        if attribute_name == "LoadBalancerName":
            return load_balancer.get_name()
        if attribute_name == "SecurityGroups":
            return load_balancer.raw_data.security_groups_ids
        return None

    @staticmethod
    def get_load_balancer_listener_attribute(load_balancer_listener: LoadBalancerListener, attribute_name: str):
        if attribute_name == "ListenerArn":
            return load_balancer_listener.get_arn()
        return None

    @staticmethod
    def get_api_gateway_attribute(api_gateway: ApiGateway, attribute_name: str):
        if attribute_name == "ApiEndpoint":
            return api_gateway.api_endpoint
        return None

    @staticmethod
    def get_dax_cluster_attribute(dax_cluster: DaxCluster, attribute_name: str):
        if attribute_name == "Arn":
            return dax_cluster.cluster_arn
        return None

    @staticmethod
    def get_subnet_attribute(subnet: Subnet, attribute_name: str):
        if attribute_name == "AvailabilityZone":
            return subnet.availability_zone
        if attribute_name == "Ipv6CidrBlocks":
            return None
        if attribute_name == "NetworkAclAssociationId":
            return subnet.network_acl and subnet.network_acl.network_acl_id
        if attribute_name == "OutpostArn":
            return None
        if attribute_name == "VpcId":
            return subnet.vpc_id
        return None

    @staticmethod
    def get_kms_key_attribute(kms_key: KmsKey, attribute_name: str):
        if attribute_name == "Arn":
            return kms_key.get_arn()
        if attribute_name == "KeyId":
            return kms_key.get_id()
        return None

    @staticmethod
    def get_eip_attribute(elastic_ip: ElasticIp, attribute_name: str):
        if attribute_name == "AllocationId":
            return elastic_ip.allocation_id
        return None

    @staticmethod
    def get_cloudtrail_attribute(cloudtrail: CloudTrail, attribute_name: str):
        if attribute_name == "Arn":
            return cloudtrail.arn
        if attribute_name == "SnsTopicArn":
            return None
        return None

    @staticmethod
    def get_codebuild_report_group_attribute(codebuild_report_group: CodeBuildReportGroup, attribute_name: str):
        if attribute_name == "Arn":
            return codebuild_report_group.get_arn()
        return None

    @staticmethod
    def get_dynamo_db_table_attribute(dynamodb_table: DynamoDbTable, attribute_name: str):
        if attribute_name == "Arn":
            return dynamodb_table.get_arn()
        if attribute_name == 'StreamArn':
            return None
        return None

    @staticmethod
    def get_config_service_aggregator_attribute(config_service_aggregator: ConfigAggregator, attribute_name: str):
        # Basically, this field is not yet supported by cloudformation:
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html
        if attribute_name == "ConfigurationAggregatorArn":
            return config_service_aggregator.get_arn()
        return None

    @staticmethod
    def get_launch_template_attribute(launch_template: LaunchTemplate, attribute_name: str):
        if attribute_name in ('DefaultVersionNumber', 'LatestVersionNumber'):
            return launch_template.version_number
        return None

    @staticmethod
    def get_cloudwatch_logs_destination_attribute(cloudwatch_logs_destination: CloudWatchLogsDestination, attribute_name: str):
        if attribute_name == "Arn":
            return cloudwatch_logs_destination.get_arn()
        return None

    @staticmethod
    def get_cloudfront_distribution_list_attribute(cloudfront_dist_list: CloudFrontDistribution, attribute_name: str):
        if attribute_name == "DomainName":
            return cloudfront_dist_list.get_name()
        if attribute_name == "Id":
            return cloudfront_dist_list.get_id()
        return None

    @staticmethod
    def get_vpc_endpoint_interface_attribute(vpc_endpoint: VpcEndpointInterface, attribute_name: str):
        if attribute_name == "NetworkInterfaceIds":
            return vpc_endpoint.network_interface_ids
        return None

    @staticmethod
    def get_iam_role_attribute(iam_role: Role, attribute_name: str):
        if attribute_name == "Arn":
            return iam_role.get_arn()
        if attribute_name == "RoleId":
            return iam_role.role_id
        return None

    @staticmethod
    def get_lambda_func_attribute(lambda_func: LambdaFunction, attribute_name: str):
        if attribute_name == "Arn":
            return lambda_func.get_arn()
        return None

    @staticmethod
    def get_iam_instance_profile_attribute(iam_instance_profile: IamInstanceProfile, attribute_name: str):
        if attribute_name == "Arn":
            return iam_instance_profile.get_arn()
        return None

    @staticmethod
    def get_transit_gateway_attribute(transit_gateway: TransitGateway, attribute_name: str):
        if attribute_name == "Id":
            return transit_gateway.get_id()
        return None

    @staticmethod
    def get_codebuild_project_attribute(codebuild_project: CodeBuildProject, attribute_name: str):
        if attribute_name == "Arn":
            return codebuild_project.get_arn()
        return None

    @staticmethod
    def get_route_table_attribute(route_table: RouteTable, attribute_name: str):
        if attribute_name == "RouteTableId":
            return route_table.get_id()
        return None

    @staticmethod
    def get_kinesis_stream_attribute(kinesis_stream: KinesisStream, attribute_name: str):
        if attribute_name == "Arn":
            return kinesis_stream.get_arn()
        return None

    @staticmethod
    def get_cloudfront_origin_access_idenity_attribute(origin_access_id: OriginAccessIdentity, attribute_name: str):
        if attribute_name == "Id":
            return origin_access_id.get_id()
        if attribute_name == "S3CanonicalUserId":
            return origin_access_id.s3_canonical_user_id
        return None

class CloudformationResourceAttributesMapper:

    _RESOURCE_ATTRIBUTES_MAP: Dict[Type[AwsResource], Callable] = {
        Vpc: CloudformationAttributesCallableStore.get_vpc_attribute,
        KmsKey: CloudformationAttributesCallableStore.get_kms_key_attribute,
        S3Bucket: CloudformationAttributesCallableStore.get_s3_bucket_attribute,
        SecurityGroup: CloudformationAttributesCallableStore.get_security_group_attribute,
        InternetGateway: CloudformationAttributesCallableStore.get_vpc_internet_gateway_attribute,
        LoadBalancer: CloudformationAttributesCallableStore.get_load_balancer_attribute,
        LoadBalancerListener: CloudformationAttributesCallableStore.get_load_balancer_listener_attribute,
        ApiGateway: CloudformationAttributesCallableStore.get_api_gateway_attribute,
        Subnet: CloudformationAttributesCallableStore.get_subnet_attribute,
        CloudTrail: CloudformationAttributesCallableStore.get_cloudtrail_attribute,
        CodeBuildReportGroup: CloudformationAttributesCallableStore.get_codebuild_report_group_attribute,
        ElasticIp: CloudformationAttributesCallableStore.get_eip_attribute,
        DynamoDbTable: CloudformationAttributesCallableStore.get_dynamo_db_table_attribute,
        ConfigAggregator: CloudformationAttributesCallableStore.get_config_service_aggregator_attribute,
        LaunchTemplate: CloudformationAttributesCallableStore.get_launch_template_attribute,
        CloudWatchLogsDestination: CloudformationAttributesCallableStore.get_cloudwatch_logs_destination_attribute,
        CloudFrontDistribution: CloudformationAttributesCallableStore.get_cloudfront_distribution_list_attribute,
        VpcEndpointInterface: CloudformationAttributesCallableStore.get_vpc_endpoint_interface_attribute,
        Role: CloudformationAttributesCallableStore.get_iam_role_attribute,
        LambdaFunction: CloudformationAttributesCallableStore.get_lambda_func_attribute,
        CodeBuildProject: CloudformationAttributesCallableStore.get_codebuild_project_attribute,
        IamInstanceProfile: CloudformationAttributesCallableStore.get_iam_instance_profile_attribute,
        DaxCluster: CloudformationAttributesCallableStore.get_dax_cluster_attribute,
        TransitGatewayVpcAttachment: CloudformationAttributesCallableStore.get_transit_gateway_attribute,
        RouteTable: CloudformationAttributesCallableStore.get_route_table_attribute,
        KinesisStream: CloudformationAttributesCallableStore.get_kinesis_stream_attribute,
        OriginAccessIdentity: CloudformationAttributesCallableStore.get_cloudfront_origin_access_idenity_attribute,
    }

    @classmethod
    def get_attribute(cls, aws_resource, attribute_name: str) -> Optional[str]:
        if isinstance(aws_resource, AwsResource):
            if get_attr_func := cls._RESOURCE_ATTRIBUTES_MAP.get(aws_resource.__class__):
                return get_attr_func(aws_resource, attribute_name)
        return None
