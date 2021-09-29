from typing import List, Union, Optional

from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_event_target import CloudWatchEventTarget
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.resources.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import IEcsInstance
from cloudrail.knowledge.context.aws.resources.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class EcsCluster(AwsResource):
    """
        Attributes:
            cluster_arn: The ARN of the ECS cluster.
            cluster_id: The ID of the cluster.
            cluster_name: The name of the cluster.
            service_list: The list of services attached to this cluster.
            event_target_list: The list of CloudWatchEventTargets associated with this
                cluster.
            is_container_insights_enabled: Indication if Container Insights enabled for this cluster or not.

    """
    def __init__(self,
                 account: str,
                 region: str,
                 cluster_arn: str,
                 cluster_name: str,
                 is_container_insights_enabled: bool,
                 cluster_id: str = None) -> None:
        super().__init__(account, region, AwsServiceName.AWS_ECS_CLUSTER)
        self.cluster_arn: str = cluster_arn
        self.cluster_id: str = cluster_id or cluster_arn
        self.cluster_name: str = cluster_name
        self.service_list: List[EcsService] = []
        self.event_target_list: List[CloudWatchEventTarget] = []
        self.with_aliases(self.cluster_id, self.cluster_arn)
        self.is_container_insights_enabled: bool = is_container_insights_enabled

    def add_services(self, service_list: List[EcsService]):
        for service in service_list:
            if service in self.service_list:
                self.service_list.remove(service)
            self.service_list.append(service)

    def add_events_targets(self, event_target_list: List[CloudWatchEventTarget]):
        for event_target in event_target_list:
            if event_target in self.event_target_list:
                self.event_target_list.remove(event_target)
            self.event_target_list.append(event_target)

    def get_keys(self) -> List[str]:
        return [self.cluster_arn]

    def get_all_eni_list(self) -> List[NetworkInterface]:
        return [eni for instance in self.get_all_ecs_instances() for eni in instance.network_resource.network_interfaces]

    def __str__(self) -> str:
        return "cluster_name={}".format(self.cluster_name)

    def get_name(self) -> str:
        return self.cluster_name

    def get_id(self) -> str:
        return self.cluster_id

    def get_arn(self) -> str:
        return self.cluster_arn

    def get_extra_data(self) -> str:
        cluster_name = 'cluster_name: {}'.format(self.cluster_name) if self.cluster_name else ''
        service_list = 'service_list: {}'.format(self.service_list) if self.service_list else 'Service list not found or not yet loaded'

        return ', '.join([cluster_name, service_list])

    def get_all_ecs_instances(self) -> List[Union[NetworkEntity, INetworkConfiguration, IEcsInstance, EcsTarget]]:
        return self.service_list + [target for event_target in self.event_target_list for target in event_target.ecs_target_list]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ECS cluster'
        else:
            return 'ECS clusters'

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}ecs/home?region={1}#/clusters/{2}/services'\
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_name)

    @property
    def is_tagable(self) -> bool:
        return True
