from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_client import AwsClient
from cloudrail.knowledge.context.aws.resources.ecs.ecs_constants import NetworkMode
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.ip_protocol import IpProtocol


@dataclass
class PortMappings:
    container_port: int
    host_port: int
    protocol: IpProtocol


@dataclass
class ContainerDefinition:
    container_name: str
    image: str
    port_mappings: List[PortMappings] = field(default_factory=list)


@dataclass
class EfsVolume:
    volume_name: str
    efs_id: str
    encrypt_efs_in_transit: bool


class EcsTaskDefinition(AwsResource):
    """
        Attributes:
            task_arn: The ARN of the task definition.
            family: The family the definition is a part of.
            revision: The revision of the task definition.
            task_role_arn: The IAM Role used by the task.
            execution_role_arn: The IAM Role used to execute the task.
            network_mode: The network mode to use with this task.
            container_definitions: A list (potentially empty) of container
                definitions.
            iam_role: The actual IAM Role referenced by execution_role_arn.
            efs_volume_data: The EFS configuration in the task, if one is configured.
            is_volume_efs: True if there is EFS configured.
    """
    def __init__(self, task_arn: str, family: str, revision: str, account: str, region: str, efs_volume_data: List[EfsVolume] = None,
                 task_role_arn: str = None, execution_role_arn: str = None, network_mode: NetworkMode = None, is_volume_efs: bool = False,
                 container_definitions: List[ContainerDefinition] = None) -> None:
        super().__init__(account, region, AwsServiceName.AWS_ECS_TASK_DEFINITION)
        self.task_arn: str = task_arn
        self.family: str = family
        self.revision: str = revision
        self.task_role_arn: str = task_role_arn  # todo - add methods to assigner role and connections builder
        self.execution_role_arn: str = execution_role_arn
        self.network_mode: NetworkMode = network_mode
        if container_definitions is None:
            self.container_definitions = []
        else:
            self.container_definitions = container_definitions
        self.iam_role: Optional[Role] = None
        if efs_volume_data is None:
            self.efs_volume_data = []
        else:
            self.efs_volume_data = efs_volume_data
        self.is_volume_efs = is_volume_efs
        self.is_volume_efs: bool = bool(self.efs_volume_data)

    def get_keys(self) -> List[str]:
        return [self.task_arn]

    def get_name(self) -> str:
        return f"{self.family}:{self.revision}"

    def get_arn(self) -> str:
        return self.task_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ECS task definition'
        else:
            return 'ECS task definitions'

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}ecs/home?region={1}#/taskDefinitions/{2}/{3}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.family, self.revision)

    @property
    def is_tagable(self) -> bool:
        return True


class IEcsInstance(AwsClient):

    @abstractmethod
    def get_task_definition(self) -> EcsTaskDefinition:
        pass

    @abstractmethod
    def set_task_definition(self, task: EcsTaskDefinition) -> None:
        pass

    @abstractmethod
    def get_task_definition_arn(self) -> str:
        pass
