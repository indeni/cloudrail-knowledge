from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class WorkLinkFleet(NetworkEntity):
    """
        Attributes:
            fleet_name: The name of the worklink fleet.
            arn: The ARN of the worklink fleet.
            vpc_config: The network configuration of the worklink fleet, if configured.
    """

    def __init__(self,
                 fleet_name: str,
                 arn: str,
                 account: str,
                 region: str,
                 vpc_config: NetworkConfiguration):
        super().__init__(fleet_name, account, region, AwsServiceName.AWS_WORKLINK_FLEET)
        self.fleet_name: str = fleet_name
        self.arn: str = arn
        self.vpc_config: NetworkConfiguration = vpc_config

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.fleet_name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'WorkLink Fleet'
        else:
            return 'WorkLink Fleets'

    def get_all_network_configurations(self) -> Optional[List[NetworkConfiguration]]:
        if self.vpc_config:
            return [NetworkConfiguration(self.vpc_config.assign_public_ip,
                                         self.vpc_config.security_groups_ids,
                                         self.vpc_config.subnet_list_ids)]
        else:
            return []

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}worklink/home?region={1}#/fleets/details/{2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.fleet_name)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'fleet_name': self.fleet_name,
                'assign_public_ip': self.vpc_config and self.vpc_config.assign_public_ip,
                'security_groups_ids': self.vpc_config and self.vpc_config.security_groups_ids,
                'subnet_list_ids': self.vpc_config and self.vpc_config.subnet_list_ids}
