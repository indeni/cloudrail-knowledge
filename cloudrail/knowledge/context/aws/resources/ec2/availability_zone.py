from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class AvailabilityZone(AwsResource):

    def __init__(self, account: str, region: str, zone_id: str, zone_name: str) -> None:
        super().__init__(account=account, region=region, tf_resource_type=AwsServiceName.NONE)
        self.zone_id: str = zone_id
        self.zone_name: str = zone_name
        self.with_aliases(zone_id, zone_name)

    def get_keys(self) -> List[str]:
        return [self.zone_id]

    def get_name(self) -> str:
        return self.zone_name

    def get_id(self) -> str:
        return self.zone_id

    @property
    def is_tagable(self) -> bool:
        return False

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def to_drift_detection_object(self) -> dict:
        return {}
