from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.tags_utils import filter_tags


class LaunchConfiguration(AwsResource):
    """
        Attributes:
            arn: The ARN of the launch config.
            image_id: The EC2 Image ID of the instance.
            instance_type: The Instance Type of the instance to launch.
            key_name: The Key Name used for the instance.
            name: The Name of the launch configuration.
            security_group_ids: The security groups used with the instance.
            http_tokens: Either "optional" or "required" (if None, means "optional").
            iam_instance_profile: The IAM Instance Profile to associate with launched instances (may be None).
            associate_public_ip_address: May be True to associate a public IP address with the launched instances.
            ebs_optimized: Indication whether the EC2 instance has EBS optimization enabled of not.
            monitoring_enabled: Indication if the launched EC2 instance will have detailed monitoring enabled.
    """

    def __init__(self,
                 arn: str,
                 image_id: str,
                 instance_type: str,
                 key_name: str,
                 name: str,
                 security_group_ids: List[str],
                 http_tokens: str,
                 iam_instance_profile: Optional[str],
                 region: str,
                 account: str,
                 associate_public_ip_address: Optional[bool],
                 ebs_optimized: bool,
                 monitoring_enabled: bool):
        super().__init__(account, region, AwsServiceName.AWS_LAUNCH_CONFIGURATION)
        self.arn: str = arn
        self.image_id: str = image_id
        self.instance_type: str = instance_type
        self.key_name: str = key_name
        self.name: str = name
        self.security_group_ids: List[str] = security_group_ids
        self.http_tokens: str = http_tokens
        self.associate_public_ip_address: Optional[bool] = associate_public_ip_address
        self.with_aliases(self.name)
        self.iam_instance_profile: Optional[str] = iam_instance_profile
        self.ebs_optimized: bool = ebs_optimized
        self.monitoring_enabled: bool = monitoring_enabled

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.name]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Launch configuration'
        else:
            return 'Launch configurations'

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2autoscaling/home?region={1}#/lc?launchConfigurationName={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.name)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'image_id': self.image_id,
                'instance_type': self.instance_type,
                'key_name': self.key_name,
                'name': self.name,
                'security_group_ids': self.security_group_ids,
                'http_tokens': self.http_tokens,
                'iam_instance_profile': self.iam_instance_profile,
                'associate_public_ip_address': self.associate_public_ip_address,
                'ebs_optimized': self.ebs_optimized,
                'monitoring_enabled': self.monitoring_enabled}


@dataclass
class LaunchTemplateData:
    """
        Attributes:
            template_id: The id of the template.
            version: The number of the version.
            template_name: The name of the template.
    """
    template_id: str
    version: str
    template_name: str


@dataclass
class AutoScalingGroupRawData:
    """
        Attributes:
            launch_configuration_name: The name of the launch configuration
                as read directly from the live environment.
            launch_template_data: The launch template data as read directly
                from the live environment.
    """
    launch_configuration_name: Optional[str] = None
    launch_template_data: Optional[LaunchTemplateData] = None


class AutoScalingGroup(AwsResource):
    """
        Attributes:
            arn: The ARN of the auto-scaling group.
            target_group_arns: May list the ALB/ELB target groups to be used with this ASG.
            name: The name of the auto-scaling group.
            availability_zones: The availability zones to initialize instances in.
            subnet_ids: The subnets to initialize instances in.
            launch_configuration: Points to the associated launch configuration, if there is one.
            launch_template: Points to the associated launch template, if there is one.
    """

    def __init__(self,
                 arn: str,
                 target_group_arns: List[str],
                 name: str,
                 availability_zones: List[str],
                 subnet_ids: List[str],
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_AUTO_SCALING_GROUP)
        self.arn = arn  # todo - network attributes are missing
        self.target_group_arns = target_group_arns
        self.name = name
        self.availability_zones = availability_zones
        self.subnet_ids = subnet_ids
        self.launch_configuration: Optional[LaunchConfiguration] = None
        self.launch_template: Optional[LaunchTemplate] = None
        self.raw_data: AutoScalingGroupRawData = AutoScalingGroupRawData()
        self.region: str = region
        self.account: str = account

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.name]

    def with_raw_data(self, launch_configuration_name: Optional[str] = None,
                      launch_template_id: Optional[str] = None,
                      launch_template_version: Optional[str] = None,
                      launch_template_name: Optional[str] = None) -> AutoScalingGroup:
        self.raw_data.launch_configuration_name = launch_configuration_name
        if launch_template_id and launch_template_version:
            self.raw_data.launch_template_data = LaunchTemplateData(launch_template_id, launch_template_version, launch_template_name)
        return self

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Auto Scaling group'
        else:
            return 'Auto Scaling groups'

    def get_cloud_resource_url(self) -> str:
        return 'https://console.aws.amazon.com/ec2autoscaling/home?region={0}#/details/{1}?view=details' \
            .format(self.region, self.name)

    def get_arn(self) -> str:
        return self.arn

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'target_group_arns': self.target_group_arns,
                'name': self.name,
                'subnet_ids': self.subnet_ids}
