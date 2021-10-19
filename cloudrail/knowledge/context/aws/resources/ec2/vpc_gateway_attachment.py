from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class VpcGatewayAttachment(AwsResource):

    def __init__(self, region: str, account: str, gateway_id: str, vpc_id: str):
        AwsResource.__init__(self, account, region)
        self.attachment_id: str = f"{vpc_id}-{gateway_id}"
        self.gateway_id: str = gateway_id
        self.vpc_id: str = vpc_id
        self.with_aliases(self.attachment_id)

    def get_keys(self) -> List[str]:
        return [self.vpc_id, self.gateway_id]

    def get_id(self) -> str:
        return self.attachment_id

    @property
    def is_tagable(self) -> bool:
        return False

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def to_drift_detection_object(self) -> dict:
        return {'gateway_id': self.gateway_id,
                'vpc_id': self.vpc_id}
