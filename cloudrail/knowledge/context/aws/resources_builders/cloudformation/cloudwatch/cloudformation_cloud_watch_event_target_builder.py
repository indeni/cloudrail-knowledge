from typing import Dict, List, Optional

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_utils import ELEMENT_POSITION_KEY
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_event_target import CloudWatchEventTarget
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_constants import LaunchType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.iac_resource_metadata import IacResourceMetadata
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.utils.tags_utils import get_aws_tags

class CloudformationCloudWatchEventTargetBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CLOUDWATCH_EVENT_TARGET, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> List[CloudWatchEventTarget]:
        properties: dict = cfn_res_attr['Properties']
        cloud_watch_event_target_list: List[CloudWatchEventTarget] = []
        for event_target_dict in properties["Targets"]:
            ecs_target_list: List[EcsTarget] = []
            network_conf_list: List[NetworkConfiguration] = []
            if ecs_parameters := event_target_dict.get("EcsParameters", {}):
                conf = ecs_parameters.get("NetworkConfiguration", {}).get("AwsVpcConfiguration")
                if conf:
                    network_conf_list = [NetworkConfiguration(self.get_property(conf, "AssignPublicIp"),
                                                              self.get_property(conf, "SecurityGroups"),
                                                              self.get_property(conf, "Subnets"))]
                region = cfn_res_attr['region']
                account_id = cfn_res_attr['account_id']
                arn = self.get_property(event_target_dict, "Arn")
                target_name = arn.split(':')[-1] + '.target.name' if arn else self.create_random_pseudo_identifier()
                target: EcsTarget = EcsTarget(target_name,
                                              event_target_dict["Id"],
                                              LaunchType(ecs_parameters.get("LaunchType")),
                                              account_id,
                                              region,
                                              arn,
                                              event_target_dict["RoleArn"],
                                              network_conf_list,
                                              ecs_parameters.get("TaskDefinitionArn"))
                self.build_target_iac_state(target, cfn_res_attr)
                ecs_target_list.append(target)
            if ecs_target_list:
                cloud_watch_event_target_list.append(CloudWatchEventTarget(account=account_id,
                                                                           region=region,
                                                                           name=arn.split(':')[-1] if arn else self.create_random_pseudo_identifier(),
                                                                           rule_name=properties["Name"],
                                                                           target_id=target.target_id,
                                                                           role_arn=target.role_arn,
                                                                           cluster_arn=target.cluster_arn,
                                                                           ecs_target_list=ecs_target_list))
        return cloud_watch_event_target_list

    @staticmethod
    def build_target_iac_state(resource: AwsResource, cfn_resource: dict):
        metadata: Optional[IacResourceMetadata] = None
        if cfn_resource.get('iac_action') != IacActionType.DELETE:
            start_line, end_line = cfn_resource[ELEMENT_POSITION_KEY]
            metadata = IacResourceMetadata(iac_entity_id=cfn_resource['logical_id'],
                                           file_name=cfn_resource['cfn_template_file_name'],
                                           start_line=start_line,
                                           end_line=end_line)
        resource.iac_state = IacState(address=cfn_resource['logical_id'],
                                      action=cfn_resource['iac_action'],
                                      is_new=cfn_resource['iac_action'] == IacActionType.CREATE,
                                      resource_metadata=metadata,
                                      iac_type=IacType.CLOUDFORMATION)
        resource.iac_state.iac_resource_url = metadata and metadata.get_iac_resource_url(cfn_resource.get('iac_url_template'))
        attributes = cfn_resource.get('Properties')
        resource.tags = get_aws_tags(attributes)
        resource.with_aliases(cfn_resource['logical_id'], resource.get_id())
