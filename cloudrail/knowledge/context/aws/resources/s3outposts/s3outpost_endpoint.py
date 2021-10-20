from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class S3OutpostEndpoint(NetworkEntity):
    """
    Attributes:
        account: The account ID in which this resource operates.
        region: The region name in which this resource operates.
        outpost_id: The ID of the S3 outpost endpoint resource.
        arn: The ARN of the S3 outpost endpoint resource.
        vpc_config: Networking information used by the resource.
    """

    def __init__(self,
                 outpost_id: str,
                 arn: str,
                 account: str,
                 region: str,
                 vpc_config: NetworkConfiguration):
        super().__init__(outpost_id, account, region, AwsServiceName.AWS_S_3_OUTPOSTS_ENDPOINT)
        self.outpost_id: str = outpost_id
        self.arn: str = arn
        self.vpc_config: NetworkConfiguration = vpc_config

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return f'Endpoint for outpost ID: {self.outpost_id}'

    def get_arn(self) -> str:
        return self.arn

    def get_all_network_configurations(self) -> Optional[List[NetworkConfiguration]]:
        return [NetworkConfiguration(self.vpc_config.assign_public_ip,
                                     self.vpc_config.security_groups_ids,
                                     self.vpc_config.subnet_list_ids)]

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}outposts/home?region={1}#OutpostDetails:OutpostId={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.outpost_id)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'assign_public_ip': self.vpc_config and self.vpc_config.assign_public_ip,
                'security_groups_ids': self.vpc_config and self.vpc_config.security_groups_ids,
                'subnet_list_ids': self.vpc_config and self.vpc_config.subnet_list_ids}
