from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.ecs.ecs_constants import LaunchType
from cloudrail.knowledge.context.aws.resources.ecs.load_balancing_configuration import LoadBalancingConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceType, AwsServiceAttributes
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import EcsTaskDefinition, IEcsInstance
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class EcsService(NetworkEntity, INetworkConfiguration, IEcsInstance):
    """
        Attributes:
            name: The name of the service.
            launch_type: The launch type of the service.
            network_conf_list: The list of network configurations set under this
                service.
            elb_list: The load balancing configuration defined under this service.
            task_definition_arn: The ARN of the task definition associated
                with the service.
            cluster_name: The name of the cluster this service belongs to.
    """
    def __init__(self, name: str, launch_type: LaunchType, cluster_arn: str, account: str, region: str,
                 network_conf_list: List[NetworkConfiguration], task_definition_arn: str = None) -> None:
        NetworkEntity.__init__(self, name, account, region, AwsServiceName.AWS_ECS_SERVICE,
                               AwsServiceAttributes(AwsServiceType.ECS.value, region=region))
        IEcsInstance.__init__(self)
        self.launch_type: LaunchType = launch_type
        self.cluster_arn: str = cluster_arn
        self.network_conf_list: List[NetworkConfiguration] = network_conf_list
        self.elb_list: List[LoadBalancingConfiguration] = []
        self.task_definition_arn: str = task_definition_arn
        self._task_definition: Optional[EcsTaskDefinition] = None
        self.cluster_name: str = None

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return self.network_conf_list

    def get_task_definition(self) -> EcsTaskDefinition:
        return self._task_definition

    def set_task_definition(self, task: EcsTaskDefinition) -> None:
        self._task_definition = task

    def get_task_definition_arn(self) -> str:
        return self.task_definition_arn

    def get_keys(self) -> List[str]:
        return [self.name, self.cluster_arn]

    def __str__(self) -> str:
        return "EcsService name={}, cluster_arn={}".format(self.name, self.cluster_arn)

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return str(self.get_keys())

    def get_arn(self) -> str:
        return self.cluster_arn

    def add_elb(self, elb: LoadBalancingConfiguration) -> None:
        self.elb_list.append(elb)

    def get_extra_data(self) -> str:
        launch_type = 'launch_type: {}'.format(self.launch_type) if self.launch_type else ''
        cluster_arn = 'cluster_arn: {}'.format(self.cluster_arn) if self.cluster_arn else ''

        return ', '.join([launch_type, cluster_arn])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ECS service'
        else:
            return 'ECS services'

    def get_cloud_resource_url(self) -> str:
        return '{0}ecs/home?region={1}#/clusters/{2}/services/{3}/details' \
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_name, self.name)

    @property
    def is_tagable(self) -> bool:
        return True
