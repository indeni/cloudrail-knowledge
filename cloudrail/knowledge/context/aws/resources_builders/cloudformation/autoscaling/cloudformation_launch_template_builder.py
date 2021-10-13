from typing import Dict, List, Optional
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLaunchTemplateBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.LAUNCH_TEMPLATE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> LaunchTemplate:
        properties: dict = cfn_res_attr['Properties']
        lt_data = self.get_property(properties, 'LaunchTemplateData', {})
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        template_id = self.get_resource_id(cfn_res_attr)
        name = self.get_property(properties, 'LaunchTemplateName')
        token_data = self.get_property(lt_data, 'MetadataOptions', {})
        http_token = self.get_property(token_data, 'HttpTokens', 'optional')
        image_id = self.get_property(lt_data, 'ImageId')
        security_group_ids = self.get_property(lt_data, 'SecurityGroupIds')
        version_number = None
        iam_instance_profile_data = self.get_property(lt_data, 'IamInstanceProfile', {})
        iam_instance_profile = self.get_property(iam_instance_profile_data, 'Name')
        ebs_optimized = self.get_property(lt_data, 'EbsOptimized', False)
        monitoring_data = self.get_property(lt_data, 'Monitoring', {})
        monitoring_enabled = self.get_property(monitoring_data, 'Enabled', False)
        instance_type = self.get_property(lt_data, 'InstanceType')

        network_configurations: List[NetworkConfiguration] = []
        for net_conf in self.get_property(lt_data, 'NetworkInterfaces', []):
            assign_public_ip: Optional[bool] = self.get_property(net_conf, 'AssociatePublicIpAddress')
            security_groups: List[str] = self.get_property(net_conf, 'Groups', [])
            subnet_id: str = self.get_property(net_conf, 'SubnetId')
            network_configurations.append(NetworkConfiguration(assign_public_ip=assign_public_ip, security_groups_ids=security_groups,
                                                            subnet_list_ids=[subnet_id] if subnet_id else []))
        return LaunchTemplate(account=account, region=region, template_id=template_id, name=name, http_token=http_token,
                              image_id=image_id, security_group_ids=security_group_ids, version_number=version_number,
                              iam_instance_profile=iam_instance_profile, ebs_optimized=ebs_optimized, monitoring_enabled=monitoring_enabled,
                              instance_type=instance_type, network_configurations=network_configurations)
