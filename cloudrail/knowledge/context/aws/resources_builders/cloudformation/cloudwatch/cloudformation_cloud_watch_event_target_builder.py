from typing import Dict, List, Optional

from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_event_target import CloudWatchEventTarget
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_cluster import EcsCluster
from cloudrail.knowledge.context.aws.resources.ecs.ecs_constants import LaunchType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.resources.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.resources.ecs.load_balancing_configuration import LoadBalancingConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationCloudWatchEventTargetBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CLOUDWATCH_EVENT_TARGET, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Optional[CloudWatchEventTarget]:
        properties: dict = cfn_res_attr['Properties']
        ecs_target_list: List[EcsTarget] = []
        network_conf_list: List[NetworkConfiguration] = []
        for event_target_dict in properties["Targets"]:
            ecs_parameters = event_target_dict.get("EcsParameters", {})
            conf = ecs_parameters.get("NetworkConfiguration", {}).get("AwsvpcConfiguration")
            if conf:
                network_conf_list = [NetworkConfiguration(self.get_property(conf, "AssignPublicIp"),
                                                          self.get_property(conf, "SecurityGroups"),
                                                          self.get_property(conf, "Subnets"))]
                arn = self.get_property(event_target_dict, "Arn", self.create_random_pseudo_identifier())
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
            return CloudWatchEventTarget(account=cfn_res_attr['account_id'],
                                         region=cfn_res_attr['region'],
                                         name=arn,
                                         rule_name=cfn_res_attr["Name"],
                                         target_id=attributes["target_id"],
                                         role_arn=attributes["role_arn"],
                                         cluster_arn=attributes["arn"],
                                         ecs_target_list=ecs_target_list)
        return None

        ecs_target_list: List[EcsTarget] = []
        counter: int = 1
        for event_target_dict in attributes["ecs_target"]:
            network_conf_list: List[NetworkConfiguration] = \
                [NetworkConfiguration(conf["assign_public_ip"], conf["security_groups"], conf["subnets"])
                 for conf in event_target_dict["network_configuration"]]
            target: EcsTarget = EcsTarget(attributes["tf_address"] + str(counter)
                                          if not _is_known_value(attributes, 'arn') else attributes['arn'].split(':')[-1] + '.target.name',
                                          attributes["target_id"],
                                          LaunchType(event_target_dict["launch_type"]),
                                          attributes['account_id'],
                                          attributes['region'],
                                          attributes["arn"],
                                          attributes["role_arn"],
                                          network_conf_list,
                                          event_target_dict.get("task_definition_arn", None))
            ecs_target_list.append(target)
            counter += 1
        if ecs_target_list:
            return CloudWatchEventTarget(account=attributes['account_id'],
                                         region=attributes['region'],
                                         name=attributes["tf_address"] if not _is_known_value(attributes, 'arn') else attributes['arn'].split(':')[-1],
                                         rule_name=attributes["rule"],
                                         target_id=attributes["target_id"],
                                         role_arn=attributes["role_arn"],
                                         cluster_arn=attributes["arn"],
                                         ecs_target_list=ecs_target_list)
        return None