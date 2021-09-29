from typing import Dict, Callable, Optional, Type
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2 import ApiGateway
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2_integration import ApiGatewayV2Integration
from cloudrail.knowledge.context.aws.resources.apigatewayv2.api_gateway_v2_vpc_link import ApiGatewayVpcLink
from cloudrail.knowledge.context.aws.resources.athena.athena_workgroup import AthenaWorkgroup
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.cloudtrail.cloudtrail import CloudTrail
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.aws.resources.ec2.route import Route
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.route_table_association import RouteTableAssociation
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.resources.codebuild.codebuild_report_group import CodeBuildReportGroup
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.ec2.vpc_gateway_attachment import VpcGatewayAttachment
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_listener import LoadBalancerListener
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.resources.batch.batch_compute_environment import BatchComputeEnvironment


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
    def get_none_attribute(unused_aws_resource: AwsResource, unused_attribute_name: str):
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

class CloudformationResourceAttributesMapper:

    RESOURCE_ATTRIBUTES_MAP: Dict[Type[AwsResource], Callable] = {
        Vpc: CloudformationAttributesCallableStore.get_vpc_attribute,
        KmsKey: CloudformationAttributesCallableStore.get_kms_key_attribute,
        S3Bucket: CloudformationAttributesCallableStore.get_s3_bucket_attribute,
        SecurityGroup: CloudformationAttributesCallableStore.get_security_group_attribute,
        AthenaWorkgroup: CloudformationAttributesCallableStore.get_none_attribute,
        InternetGateway: CloudformationAttributesCallableStore.get_vpc_internet_gateway_attribute,
        VpcGatewayAttachment: CloudformationAttributesCallableStore.get_none_attribute,
        RouteTable: CloudformationAttributesCallableStore.get_none_attribute,
        Route: CloudformationAttributesCallableStore.get_none_attribute,
        RouteTableAssociation: CloudformationAttributesCallableStore.get_none_attribute,
        LoadBalancer: CloudformationAttributesCallableStore.get_load_balancer_attribute,
        LoadBalancerListener: CloudformationAttributesCallableStore.get_load_balancer_listener_attribute,
        ApiGateway: CloudformationAttributesCallableStore.get_api_gateway_attribute,
        ApiGatewayVpcLink: CloudformationAttributesCallableStore.get_none_attribute,
        ApiGatewayV2Integration: CloudformationAttributesCallableStore.get_none_attribute,
        Subnet: CloudformationAttributesCallableStore.get_subnet_attribute,
        CloudTrail: CloudformationAttributesCallableStore.get_cloudtrail_attribute,
        CodeBuildReportGroup: CloudformationAttributesCallableStore.get_codebuild_report_group_attribute,
        BatchComputeEnvironment: CloudformationAttributesCallableStore.get_none_attribute,
    }

    @classmethod
    def get_attribute(cls, aws_resource, attribute_name: str) -> Optional[str]:
        if isinstance(aws_resource, AwsResource):
            if get_attr_func := cls.RESOURCE_ATTRIBUTES_MAP.get(aws_resource.__class__):
                return get_attr_func(aws_resource, attribute_name)
        return None
