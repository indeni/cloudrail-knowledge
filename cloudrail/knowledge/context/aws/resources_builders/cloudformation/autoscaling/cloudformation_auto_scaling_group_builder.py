from typing import Dict
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_configuration import AutoScalingGroup
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationAutoScalingGroupBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.AUTO_SCALING_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> AutoScalingGroup:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        name = self.get_property(properties, 'AutoScalingGroupName', self.get_resource_id(cfn_res_attr))
        arn = build_arn('autoscaling', region, account, 'autoScalingGroup:',
                        self.create_random_pseudo_identifier() + ':autoScalingGroupName/', name)
        target_group_arns = self.get_property(properties, 'TargetGroupARNs')
        subnet_ids = self.get_property(properties, 'VPCZoneIdentifier')
        availability_zones = self.get_property(properties, 'AvailabilityZones')
        lt_data = self.get_property(properties, 'LaunchTemplate')
        launch_template_version = None
        launch_template_id = None
        launch_template_name = None
        if lt_data:
            launch_template_version = self.get_property(lt_data, 'Version')
            launch_template_id=self.get_property(lt_data, 'LaunchTemplateId')
            launch_template_name=self.get_property(lt_data, 'LaunchTemplateName')
        return AutoScalingGroup(account=account, region=region, arn=arn, name=name, target_group_arns=target_group_arns,
                                subnet_ids=subnet_ids, availability_zones=availability_zones)\
                                    .with_raw_data(launch_configuration_name=properties.get('LaunchConfigurationName'),
                                                   launch_template_id=launch_template_id,
                                                   launch_template_version=launch_template_version,
                                                   launch_template_name=launch_template_name)
