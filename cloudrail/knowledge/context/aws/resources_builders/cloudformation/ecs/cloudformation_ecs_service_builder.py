from typing import Dict, List

from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_constants import LaunchType
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.resources.ecs.load_balancing_configuration import LoadBalancingConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationEcsServiceBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ECS_SERVICE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> EcsService:
        properties: dict = cfn_res_attr['Properties']
        network_conf_list: List[NetworkConfiguration] = None
        conf = properties.get("NetworkConfiguration", {}).get("AwsvpcConfiguration")
        if conf:
            network_conf_list = [NetworkConfiguration(self.get_property(conf, "AssignPublicIp"),
                                                      self.get_property(conf, "SecurityGroups"),
                                                      self.get_property(conf, "Subnets"))]

        service: EcsService = EcsService(name=self.get_property(properties, "ServiceName"),
                                         launch_type=LaunchType(self.get_property(properties, "LaunchType", "EC2")),
                                         cluster_arn=self.get_property(properties, "Cluster"),
                                         account=cfn_res_attr['account_id'],
                                         region=cfn_res_attr['region'],
                                         network_conf_list=network_conf_list,
                                         task_definition_arn=self.get_property(properties, 'TaskDefinition'))
        elb_list: dict = properties.get("LoadBalancers", [])
        for elb_dict in elb_list:
            elb: LoadBalancingConfiguration = LoadBalancingConfiguration(self.get_property(elb_dict, "LoadBalancerName"),
                                                                         self.get_property(elb_dict, "TargetGroupArn"),
                                                                         self.get_property(elb_dict, "ContainerName"),
                                                                         self.get_property(elb_dict, "ContainerPort"))
            service.add_elb(elb)
        return service
