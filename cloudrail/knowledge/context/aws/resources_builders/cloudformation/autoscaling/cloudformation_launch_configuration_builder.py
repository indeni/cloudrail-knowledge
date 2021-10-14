from typing import Dict
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_configuration import LaunchConfiguration
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn, is_valid_arn
from arnparse import arnparse


class CloudformationLaunchConfigurationBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.LAUNCH_CONFIGURATION, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> LaunchConfiguration:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        name = self.get_property(properties, 'LaunchConfigurationName', self.get_resource_id(cfn_res_attr))
        arn = build_arn('autoscaling', region, account, 'launchConfiguration:',
                        self.create_random_pseudo_identifier() + ':launchConfigurationName/', name)
        monitoring_enabled = self.get_property(properties, 'InstanceMonitoring', True)

        iam_instance_profile = self.get_property(properties, 'IamInstanceProfile')
        if iam_instance_profile and is_valid_arn(iam_instance_profile):
            iam_instance_profile = arnparse(iam_instance_profile).resource
        image_id = self.get_property(properties, 'ImageId')
        instance_type = self.get_property(properties, 'InstanceType')
        key_name = self.get_property(properties, 'KeyName')
        security_group_ids = self.get_property(properties, 'SecurityGroups')
        metadata_options = self.get_property(properties, 'MetadataOptions', {})
        http_tokens = self.get_property(metadata_options, 'HttpTokens', 'optional')
        associate_public_ip_address = self.get_property(properties, 'AssociatePublicIpAddress', False)
        ebs_optimized = self.get_property(properties, 'EbsOptimized', False)
        return LaunchConfiguration(account=account, region=region, arn=arn, monitoring_enabled=monitoring_enabled, iam_instance_profile=iam_instance_profile,
                                   image_id=image_id, instance_type=instance_type, key_name=key_name, name=name, security_group_ids=security_group_ids,
                                   http_tokens=http_tokens, associate_public_ip_address=associate_public_ip_address, ebs_optimized=ebs_optimized)
