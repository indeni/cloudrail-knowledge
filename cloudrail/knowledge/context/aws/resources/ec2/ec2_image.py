from typing import List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class Ec2Image(AwsResource):
    """
        Attributes:
            image_id: The ID of the EC2 image (AMI ID).
            is_public: True if the image is publicly shared.
    """

    def __init__(self,
                 image_id: str,
                 is_public: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.NONE)
        self.image_id: str = image_id
        self.is_public: bool = is_public

    def get_keys(self) -> List[str]:
        return [self.image_id]

    def get_id(self) -> str:
        return self.image_id

    def get_name(self) -> str:
        return self.image_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'EC2 Image'
        else:
            return 'EC2 Images'

    def get_cloud_resource_url(self) -> str:
        if self.is_public:
            return '{0}ec2/v2/home?region={1}#Images:visibility=public-images;imageId={2}'\
                .format(self.AWS_CONSOLE_URL, self.region, self.image_id)
        else:
            return '{0}ec2/v2/home?region={1}#Images:visibility=private-images;imageId={2}'\
                .format(self.AWS_CONSOLE_URL, self.region, self.image_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {}
