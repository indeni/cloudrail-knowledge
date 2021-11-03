from typing import Dict, List
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_event_target import CloudWatchEventTarget
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_constants import LaunchType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


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
                arn = self.get_property(event_target_dict, "Arn", self.create_random_pseudo_identifier()) + '.target.name'
                target: EcsTarget = EcsTarget(arn,
                                              event_target_dict["Id"],
                                              LaunchType(ecs_parameters.get("LaunchType")),
                                              cfn_res_attr['account_id'],
                                              cfn_res_attr['region'],
                                              arn,
                                              event_target_dict["RoleArn"],
                                              network_conf_list,
                                              ecs_parameters.get("TaskDefinitionArn"))
                ecs_target_list.append(target)
            if ecs_target_list:
                cloud_watch_event_target_list.append(CloudWatchEventTarget(account=cfn_res_attr['account_id'],
                                                                           region=cfn_res_attr['region'],
                                                                           name=target.cluster_arn,
                                                                           rule_name=properties["Name"],
                                                                           target_id=target.target_id,
                                                                           role_arn=target.role_arn,
                                                                           cluster_arn=target.cluster_arn,
                                                                           ecs_target_list=ecs_target_list))
        return cloud_watch_event_target_list
