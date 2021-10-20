from typing import List
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class ResourceTagMappingList(AwsResource):
    """
        This object contains the tags associated with a resource when tags
        are managed by the resource-group tag-editor feature in AWS.

        Attributes:
            resource_arn: The ARN of the resource whose tag mapping this
                object focuses on.
    """
    def __init__(self,
                 resource_arn: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.NONE)
        self.resource_arn: str = resource_arn

    def get_keys(self) -> List[str]:
        return [self.resource_arn]

    def get_name(self) -> str:
        return 'ResourceTagMappingList for region ' + self.region

    def get_type(self, is_plural: bool = False) -> str:
        return 'AWS Resource Groups'

    def get_cloud_resource_url(self) -> str:
        return '{0}resource-groups/tag-editor/find-resources?region={1}'\
            .format(self.AWS_CONSOLE_URL, self.region)

    def get_arn(self) -> str:
        return self.resource_arn

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {}
