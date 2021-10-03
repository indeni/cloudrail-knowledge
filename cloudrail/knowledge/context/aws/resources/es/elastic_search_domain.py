from dataclasses import dataclass
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain_policy import ElasticSearchDomainPolicy
from cloudrail.knowledge.context.aws.resources.indirect_public_connection_data import IndirectPublicConnectionData
from cloudrail.knowledge.context.aws.resources.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


@dataclass
class LogPublishingOptions:
    """
        Attributes:
            log_type: The type of Elasticsearch log to publish.
            cloudwatch_log_group_arn: The ARN of the Cloudwatch log group to publish logs into.
            enable: Indication if log publishing is enabled.

    """
    log_type: str
    cloudwatch_log_group_arn: str
    enabled: bool


class ElasticSearchDomain(NetworkEntity, INetworkConfiguration):
    """
        Attributes:
            domain_id: The ID of the ElasticSearch Domain.
            domain_name: The name of the domain.
            arn: The ARN of the domain.
            enforce_https: True if only HTTPS is allowed.
            subnet_ids: The IDs of the subnets the domain is attached to, if any.
            security_group_ids: The IDs of the security groups used with the ElasticSearch
                Domain, if any.
            encrypt_at_rest_state: True if encryption at rest is enabled.
            encrypt_node_to_node_state: True if node-to-node traffic is encrypted.
            is_public: True if the ElasticSearch Domain is public.
            is_in_vpc: True if the ElasticSearch Domain is accessible at a specific
                VPC.
            ports: The ports the ElasticSearch is listening on.
            policy: The resource policy used with the domain.
            indirect_public_connection_data: The data that describes that a publicly-accessible resource can access this resource by a security group of this resource.
            log_publishing_options: Set of data about the publishing logs to CloudWatch, if enabled.
            es_domain_version: The ElasticSearch Domain version.
            es_domain_cluster_instance_type: The ElasticSearch Domain cluster instance type.
    """
    def __init__(self,
                 domain_id: str,
                 domain_name: str,
                 arn: str,
                 enforce_https: bool,
                 subnet_ids: Optional[List[str]],
                 security_group_ids: Optional[List[str]],
                 encrypt_at_rest_state: bool,
                 encrypt_node_to_node_state: bool,
                 account: str,
                 region: str,
                 log_publishing_options: Optional[List[LogPublishingOptions]],
                 es_domain_version: str,
                 es_domain_cluster_instance_type: str):
        """
        `ElasticSearch Domain` can either be `Publicly Accessible` and not in any VPC, or it can be `Publicly In-Accessible` if its in a VPC.
        Subsequently, if an `ElasticSearch Domain` does not belong to a subnet then it means it is can only be accessed from within the VPC.

        """
        self.encrypt_at_rest_state: bool = encrypt_at_rest_state
        self.encrypt_node_to_node_state: bool = encrypt_node_to_node_state

        super().__init__(domain_name, account, region, AwsServiceName.AWS_ELASTIC_SEARCH_DOMAIN)
        self.domain_id: str = domain_id
        self.arn: str = arn
        self._network_configuration: NetworkConfiguration = NetworkConfiguration(False, security_group_ids, subnet_ids)
        self.is_public: bool = subnet_ids is None
        self.is_in_vpc: bool = not self.is_public
        self.ports: List[int] = [443]
        if not enforce_https:
            self.ports.append(80)
        self.policy: ElasticSearchDomainPolicy = None
        self.log_publishing_options: Optional[List[LogPublishingOptions]] = log_publishing_options
        self.indirect_public_connection_data: Optional[IndirectPublicConnectionData] = None
        self.es_domain_version: str = es_domain_version
        self.es_domain_cluster_instance_type: str = es_domain_cluster_instance_type

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_id(self) -> str:
        return self.domain_id

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [self._network_configuration]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ElasticSearch Domain'
        else:
            return 'ElasticSearch Domains'

    def get_cloud_resource_url(self) -> str:
        return '{0}es/home?region={1}#domain:resource={2};action=dashboard' \
            .format(self.AWS_CONSOLE_URL, self.region, self.name)

    @property
    def is_tagable(self) -> bool:
        return True
