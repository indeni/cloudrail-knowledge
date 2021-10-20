from typing import List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudHsmV2Hsm(AwsResource):
    """
    Attributes:
        cluster_id: The HSM cluster ID.
        hsm_id: The HSM ID.
        subnet_id: The subnet ID in which this HSM operates.
        availability_zone: The availability zone in which this HSM operates.
        hsm_state: The HSM readiness state.
        account: The account ID in which this HSM cluster operates.
        region: The region in which this HSM cluster operates.
    """

    def __init__(self,
                 cluster_id: str,
                 hsm_id: str,
                 subnet_id: str,
                 availability_zone: str,
                 hsm_state: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_CLOUDHSM_V_2_HSM)
        self.cluster_id: str = cluster_id
        self.hsm_id: str = hsm_id
        self.subnet_id: str = subnet_id
        self.hsm_state: str = hsm_state
        self.availability_zone: str = availability_zone

    def get_keys(self) -> List[str]:
        return [self.hsm_id]

    def get_id(self) -> str:
        return self.hsm_id

    def get_arn(self) -> str:
        pass

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudHSM'
        else:
            return 'CloudHSMs'

    def get_cloud_resource_url(self) -> str:
        return '{0}cloudhsm/home?region={1}#/clusters/{2}/'\
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_id)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'cluster_id': self.cluster_id,
                'subnet_id': self.subnet_id,
                'availability_zone': self.availability_zone,
                'hsm_state': self.hsm_state}
