from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class KinesisFirehoseStream(NetworkEntity):
    """
        Attributes:
            stream_name: The name of the Kinesis Firehose Stream.
            stream_arn: The ARN of the Kinesis Firehose Stream.
            encrypted_at_rest: True if the stream is set to be encrypted.
            es_domain_arn: The ARN of the related ElasticSearch Domain, if any.
            es_vpc_config: The VPC configuration of the ElasticSearch Domain related
                to this stream, if any.
    """
    def __init__(self,
                 stream_name: str,
                 stream_arn: str,
                 encrypted_at_rest: bool,
                 account: str,
                 region: str,
                 es_domain_arn: Optional[str],
                 es_vpc_config: Optional[NetworkConfiguration]):
        super().__init__(stream_name, account, region, AwsServiceName.AWS_KINESIS_FIREHOSE_DELIVERY_STREAM)
        self.stream_name: str = stream_name
        self.stream_arn: str = stream_arn
        self.encrypted_at_rest: bool = encrypted_at_rest
        self.es_domain_arn: Optional[str] = es_domain_arn
        self.es_vpc_config: Optional[NetworkConfiguration] = es_vpc_config

    def get_keys(self) -> List[str]:
        return [self.stream_arn]

    def get_name(self) -> str:
        return self.stream_name

    def get_arn(self) -> str:
        return self.stream_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Kinesis Data Firehose'
        else:
            return 'Kinesis Data Firehoses'

    def get_all_network_configurations(self) -> Optional[List[NetworkConfiguration]]:
        if self.es_vpc_config:
            return [NetworkConfiguration(self.es_vpc_config.assign_public_ip,
                                         self.es_vpc_config.security_groups_ids,
                                         self.es_vpc_config.subnet_list_ids)]
        else:
            return None

    def get_cloud_resource_url(self) -> str:
        return '{0}firehose/home?region={1}#/details/{2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.stream_name)

    @property
    def is_tagable(self) -> bool:
        return True
