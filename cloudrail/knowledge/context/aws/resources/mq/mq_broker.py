from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class MqBroker(NetworkEntity):
    """
    Attributes:
        account: The account ID in which this resource operates.
        region: The region name in which this resource operates.
        broker_name: The MQ broker resource name.
        arn: The ARN of the MQ broker resource.
        broker_id: The ID of the MQ broker resource.
        deployment_mode: Deployment mode of the MQ broker.
        vpc_id: The VPC ID in which the MQ broker is deployed.
        vpc_config: Networking information used by the resource.
    """

    def __init__(self,
                 broker_name: str,
                 arn: str,
                 broker_id: str,
                 account: str,
                 region: str,
                 deployment_mode: str,
                 vpc_config: Optional[NetworkConfiguration]):
        super().__init__(broker_name, account, region, AwsServiceName.AWS_MQ_BROKER)
        self.broker_name: str = broker_name
        self.arn: str = arn
        self.broker_id: str = broker_id
        self.vpc_config: Optional[NetworkConfiguration] = vpc_config
        self.deployment_mode: str = deployment_mode
        self.vpc_id: str = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.broker_name

    def get_arn(self) -> str:
        return self.arn

    def get_id(self) -> str:
        return self.broker_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'MQ Broker'
        else:
            return 'MQ Brokers'

    def get_all_network_configurations(self) -> Optional[List[NetworkConfiguration]]:
        return [NetworkConfiguration(self.vpc_config.assign_public_ip,
                                     self.vpc_config.security_groups_ids,
                                     self.vpc_config.subnet_list_ids)]

    def get_cloud_resource_url(self) -> str:
        return '{0}amazon-mq/home?region={1}#/brokers/details?id={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.broker_id)

    @property
    def is_tagable(self) -> bool:
        return True
