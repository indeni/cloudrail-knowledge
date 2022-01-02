from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_client import AwsClient
from cloudrail.knowledge.context.aws.resources.ec2.ec2_image import Ec2Image
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.networking_config.network_resource import NetworkResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName, AwsServiceAttributes, AwsServiceType
from cloudrail.knowledge.utils.tags_utils import filter_tags
from cloudrail.knowledge.utils.utils import flat_list


class AssociatePublicIpAddress(str, Enum):
    YES = 'Yes'
    NO = 'No'
    USE_SUBNET_SETTINGS = 'UseSubnetSettings'

    @staticmethod
    def convert_from_optional_boolean(boolean: Optional[bool]) -> AssociatePublicIpAddress:
        if boolean is None:
            return AssociatePublicIpAddress.USE_SUBNET_SETTINGS
        if boolean:
            return AssociatePublicIpAddress.YES
        return AssociatePublicIpAddress.NO


@dataclass
class Ec2RawData:
    """
        Internal implementation detail, ignore.
    """
    subnet_id: Optional[str] = None
    private_ip_address: Optional[str] = None  # Why is this singular?
    public_ip_address: Optional[str] = None
    ipv6_addresses: List[str] = field(default_factory=list)
    associate_public_ip_address: Optional[AssociatePublicIpAddress] = None
    security_groups_ids: List[str] = field(default_factory=list)


class Ec2Instance(NetworkEntity, AwsClient):
    """
        Attributes:
            instance_id: The ID of the instance.
            name: The name of the EC2 instance, if set.
            network_interfaces_ids: The network interfaces attached to the
                intance.
            state: The state of the instance.
            image_id: The ID of the AMI used for EC2.
            image_data: A pointer to the Ec2Image if found.
            iam_profile_arn: The IAM profile assigned to this image, if one is assigned.
            iam_profile_id: The ID of the IAM profile.
            http_tokens: The HTTP tokens setting - optional or required.
            availability_zone: The availability zone the EC2 is in, if configured.
            instance_type: The Instance type (i.e. 'm5.8xlarge').
            ebs_optimized: Indication whether the EC2 instance has EBS optimization enabled of not.
            monitoring_enabled: Indication if the launched EC2 instance will have detailed monitoring enabled.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 instance_id: str,
                 name: str,
                 network_interfaces_ids: List[str],
                 state: str,
                 image_id: str,
                 iam_profile_name: Optional[str],
                 http_tokens: str,
                 availability_zone: Optional[str],
                 tags: dict,
                 instance_type: str,
                 ebs_optimized: bool,
                 monitoring_enabled: bool):
        NetworkEntity.__init__(self, name or instance_id, account, region, AwsServiceName.AWS_EC2_INSTANCE,
                               AwsServiceAttributes(aws_service_type=AwsServiceType.EC2.value, region=region))
        AwsClient.__init__(self)
        self.network_resource: NetworkResource = NetworkResource()
        self.instance_id: str = instance_id
        self.network_interfaces_ids: List[str] = network_interfaces_ids
        self.state: str = state
        self.image_id: str = image_id
        self.iam_profile_name: Optional[str] = iam_profile_name
        self.http_tokens: str = http_tokens
        self.availability_zone: Optional[str] = availability_zone
        self.image_data: Optional[Ec2Image] = None
        self.raw_data: Ec2RawData = Ec2RawData()
        if tags:
            self.tags.update(tags)
        self.instance_type: str = instance_type
        self.ebs_optimized: bool = ebs_optimized
        self.monitoring_enabled: bool = monitoring_enabled

    def __str__(self):
        name_or_id_msg = 'Instance Name: {}'.format(
            self.name) if self.name else 'Instance Id: {}'.format(self.instance_id)
        private_ips_msg = 'Private IP(s): {}'.format(
            ', '.join(self.network_resource.private_ip_addresses))
        public_ips_msg = 'Public IP(s): {}'.format(
            self.network_resource.public_ip_addresses) \
            if self.network_resource.public_ip_addresses \
            else 'Public IP(s): None'
        vpc_name_or_id_msg = 'VPC Name: {}'.format(
            self.network_resource.vpc_name) \
            if self.network_resource.vpc_name else \
            f'VPC Id: {self.network_resource.vpc_id}'

        return '{} {} {} {}'.format(name_or_id_msg, vpc_name_or_id_msg, public_ips_msg, private_ips_msg)

    def get_keys(self) -> List[str]:
        return [self.instance_id]

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.instance_id

    def get_extra_data(self) -> str:
        return str(self)

    def with_raw_data(self,
                      subnet_id: Optional[str] = None,
                      # Why is this singular?
                      private_ip_address: Optional[str] = None,
                      public_ip_address: Optional[str] = None,
                      ipv6_addresses: List[str] = None,
                      associate_public_ip_address: AssociatePublicIpAddress = None,
                      security_groups_ids: List[str] = None) -> Ec2Instance:
        self.raw_data = Ec2RawData(subnet_id, private_ip_address, public_ip_address, ipv6_addresses or [],
                                   associate_public_ip_address, security_groups_ids or [])
        return self

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'EC2 Instance'
        else:
            return 'EC2 Instances'

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2/v2/home?region={1}#InstanceDetails:instanceId={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.instance_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        full_security_groups_ids = flat_list([eni.security_groups_ids for eni in self.network_resource.network_interfaces])
        security_groups_ids_no_pseudo = [sg_id for sg_id in full_security_groups_ids if 'pseudo' not in sg_id]
        return {'name': self.name,
                'state': self.state,
                'iam_profile_name': self.iam_profile_name,
                'http_tokens': self.http_tokens,
                'tags': filter_tags(self.tags),
                'instance_type': self.instance_type,
                'ebs_optimized': self.ebs_optimized,
                'monitoring_enabled': self.monitoring_enabled,
                'security_group_ids': security_groups_ids_no_pseudo}
