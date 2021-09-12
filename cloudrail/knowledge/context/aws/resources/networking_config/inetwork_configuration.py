from abc import abstractmethod
from typing import List
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration


class INetworkConfiguration:

    @abstractmethod
    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        pass
