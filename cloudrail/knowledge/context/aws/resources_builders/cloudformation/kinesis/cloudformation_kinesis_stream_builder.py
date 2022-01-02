from typing import Dict

from cloudrail.knowledge.context.aws.resources.kinesis.kinesis_stream import KinesisStream
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationKinesisStreamBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.KINESIS_STREAM, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> KinesisStream:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        stream_name = self.get_property(properties, 'Name', self.get_resource_id(cfn_res_attr))
        stream_arn = build_arn('kinesis', region, account, 'stream', None, stream_name)
        encrypted_at_rest = bool(self.get_property(properties, 'StreamEncryption'))
        return KinesisStream(account=account,
                             region=region,
                             stream_name=stream_name,
                             stream_arn=stream_arn,
                             encrypted_at_rest=encrypted_at_rest)
