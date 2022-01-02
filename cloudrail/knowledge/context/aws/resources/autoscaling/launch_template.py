from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class LaunchTemplate(AwsResource):
    """
        Attributes:
            template_id: The ID of the template.
            name: The name of the template.
            http_token: "optional" or "required" (if None, means "optional").
            image_id: The EC2 Image ID of the instance.
            security_group_ids: The security groups used with the instance.
            version_number: The version number of this template.
            iam_instance_profile: The IAM Instance Profile to associate with launched instances (may be None).
            network_configurations: The network configuration(s) set in the template (may be None).
            security_groups: Points to the actual security groups set in security_group_ids.
            instance_type: The Instance type (i.e. 'm5.8xlarge').
            ebs_optimized: Indication whether the EC2 instance has EBS optimization enabled of not.
            monitoring_enabled: Indication if the launched EC2 instance will have detailed monitoring enabled.
    """

    def __init__(self,
                 template_id: str,
                 name: str,
                 http_token: str,
                 image_id: str,
                 security_group_ids: List[str],
                 version_number: Optional[int],
                 region: str,
                 account: str,
                 iam_instance_profile: Optional[str],
                 ebs_optimized: bool,
                 monitoring_enabled: bool,
                 instance_type: str,
                 network_configurations: List[NetworkConfiguration] = None):
        super().__init__(account, region, AwsServiceName.AWS_LAUNCH_TEMPLATE)
        self.template_id: str = template_id
        self.name: str = name
        self.http_token: str = http_token
        self.image_id: str = image_id
        self.security_group_ids: List[str] = security_group_ids
        self.version_number: Optional[int] = version_number
        self.iam_instance_profile: Optional[str] = iam_instance_profile
        self.network_configurations: List[NetworkConfiguration] = network_configurations or []
        self.security_groups: List[SecurityGroup] = []
        self.ebs_optimized: bool = ebs_optimized
        self.monitoring_enabled: bool = monitoring_enabled
        self.instance_type: str = instance_type
        self.with_aliases(self.template_id)

    def get_keys(self) -> List[str]:
        return [self.template_id, self.account, self.region]

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.template_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Launch template'
        else:
            return 'Launch templates'

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2/v2/home?region={1}#LaunchTemplateDetails:launchTemplateId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.template_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name,
                'http_token': self.http_token,
                'image_id': self.image_id,
                'iam_instance_profile': self.iam_instance_profile,
                'ebs_optimized': self.ebs_optimized,
                'monitoring_enabled': self.monitoring_enabled,
                'instance_type': self.instance_type}
