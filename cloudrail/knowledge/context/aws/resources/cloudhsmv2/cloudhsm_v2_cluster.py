from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.cloudhsmv2.cloudhsm_v2_hsm import CloudHsmV2Hsm
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudHsmV2Cluster(NetworkEntity):
    """
    Attributes:
        hsm_type: The HSM type of the cluster.
        subnet_ids: The subnet IDs used for the cluster.
        vpc_id: The VPC ID used for the HSM cluster.
        security_group_id: The security group id which is used for the HSM cluster.
        account: The account ID in which this HSM cluster operates.
        region: The region in which this HSM cluster operates.
        vpc_config: some networking attributes used to associate ENI to the resource.
    """

    def __init__(self,
                 hsm_type: str,
                 subnet_ids: list,
                 cluster_id: str,
                 vpc_id: str,
                 security_group_id: str,
                 account: str,
                 region: str):
        super().__init__(hsm_type, account, region, AwsServiceName.AWS_CLOUDHSM_V_2_CLUSTER)
        self.hsm_type: str = hsm_type
        self.subnet_ids: list = subnet_ids
        self.cluster_id: str = cluster_id
        self.vpc_id: str = vpc_id
        self.security_group_id: str = security_group_id
        self.vpc_config: NetworkConfiguration = None
        self.cluster_hsm: CloudHsmV2Hsm = None

    def get_id(self) -> str:
        return self.cluster_id

    def get_keys(self) -> List[str]:
        return [self.cluster_id]

    def get_arn(self) -> Optional[str]:
        if self.account:
            return f'arn:aws:cloudhsm:{self.region}:{self.account}:cluster/{self.cluster_id}'
        else:
            return None

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudHSM Cluster'
        else:
            return 'CloudHSM Clusters'

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [NetworkConfiguration(self.vpc_config.assign_public_ip,
                                     self.vpc_config.security_groups_ids,
                                     self.vpc_config.subnet_list_ids)]

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}cloudhsm/home?region={1}#/clusters/{2}/'\
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_id)

    @property
    def is_tagable(self) -> bool:
        return True
