from abc import abstractmethod
from typing import List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName, AwsServiceAttributes
from cloudrail.knowledge.context.aws.resources.networking_config.network_resource import NetworkResource


class NetworkEntity(AwsResource):
    """
        This class is the parent of all resources that have a network connection.

        Attributes:
            name: Name of the network entity.
            network_resource: Networking information of the entity.
    """
    def __init__(self, name: str, account: str, region: str, tf_resource_type: AwsServiceName,
                 aws_service_attributes: AwsServiceAttributes = None) -> None:
        super().__init__(account, region, tf_resource_type, aws_service_attributes)
        self.name: str = name
        self.network_resource: NetworkResource = NetworkResource()

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
