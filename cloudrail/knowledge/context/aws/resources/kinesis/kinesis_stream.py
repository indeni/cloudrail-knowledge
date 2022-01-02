from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.utils.tags_utils import filter_tags


class KinesisStream(AwsResource):
    """
        Attributes:
            stream_name: The name of the Kinesis Stream.
            stream_arn: The ARN of the Kinesis Stream.
            encrypted_at_rest: True if the stream is set to be encrypted at rest.
    """

    def __init__(self,
                 stream_name: str,
                 stream_arn: str,
                 encrypted_at_rest: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_KINESIS_STREAM)
        self.stream_name: str = stream_name
        self.stream_arn: str = stream_arn
        self.encrypted_at_rest: bool = encrypted_at_rest

    def get_keys(self) -> List[str]:
        return [self.stream_arn]

    def get_name(self) -> str:
        return self.stream_name

    def get_arn(self) -> str:
        return self.stream_arn

    def get_id(self) -> str:
        return self.stream_name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Kinesis Data Stream'
        else:
            return 'Kinesis Data Streams'

    def get_cloud_resource_url(self) -> str:
        return '{0}kinesis/home?region={1}#/streams/details/{2}/details'\
            .format(self.AWS_CONSOLE_URL, self.region, self.stream_name)

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags), 'stream_name': self.stream_name,
                'encrypted_at_rest': self.encrypted_at_rest}
