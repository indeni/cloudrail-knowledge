import logging
from abc import abstractmethod
from typing import List, Dict, Set

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.dms.dms_replication_instance import DmsReplicationInstance
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRulePropertyType
from cloudrail.knowledge.context.aws.resources.eks.eks_cluster import EksCluster
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.context.aws.resources.neptune.neptune_cluster import NeptuneCluster
from cloudrail.knowledge.context.aws.resources.neptune.neptune_instance import NeptuneInstance
from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.connection import ConnectionType, PortConnectionProperty, ConnectionDetail
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.constants.known_ports import KnownPorts
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils.port_utils import is_all_ports
from cloudrail.knowledge.utils.utils import is_port_in_range, is_all_ips


class PublicAccessSecurityGroupsPortRule(AwsBaseRule):

    def __init__(self, port: KnownPorts) -> None:
        self.port = port

    @abstractmethod
    def get_id(self) -> str:
        pass

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.get_used_network_interfaces())

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        eni_list: AliasesDict[NetworkInterface] = env_context.get_used_network_interfaces()
        logging.error(f'len of eni_list {len(eni_list)}')
        self.remove_from_eni_list(eni_list, parameters)
        if self.port.value == KnownPorts.ALL:
            eni_to_sg_map: Dict[NetworkInterface, Set[SecurityGroup]] = self.find_sg_issues(eni_list)
            message: str = ("~Internet~. {0} `{1}` has internet gateway. "
                            "Instance `{2}` is on `{1}`. {0} routes traffic from instance to internet gateway. "
                            "{0} uses Network ACL's `{3}` which allows all ports range. Instance uses security group `{4}`. "
                            "`{4}` allows all ports range. ~Instance~")
            return [
                Issue(
                    message.format(
                        eni.subnet.get_type(),
                        eni.subnet.get_friendly_name(),
                        eni.owner.get_friendly_name(),
                        eni.subnet.network_acl.get_friendly_name(),
                        sg.get_friendly_name()),
                    eni.owner,
                    sg)
                for eni in eni_to_sg_map for sg in eni_to_sg_map[eni]]

        else:
            eni_to_sg_map: Dict[NetworkInterface, Set[SecurityGroup]] = self.find_sg_issues(eni_list)
            message: str = ("~Internet~. {0} `{1}` has internet gateway. "
                            "Instance `{2}` is on `{1}`. {0} routes traffic from instance to internet gateway. "
                            "{0} uses Network ACL's `{3}` which allows port `{4}`. Instance uses security group `{5}`. "
                            "`{5}` allows port `{4}`. ~Instance~")

            return [
                Issue(
                    message.format(
                        eni.subnet.get_type(),
                        eni.subnet.get_friendly_name(),
                        eni.owner.get_friendly_name(),
                        eni.subnet.network_acl.get_friendly_name(),
                        self.port.value,
                        sg.get_friendly_name()),
                    eni.owner,
                    sg)
                for eni in eni_to_sg_map for sg in eni_to_sg_map[eni]]

    @staticmethod
    def remove_from_eni_list(eni_list: AliasesDict[NetworkInterface], parameters: Dict[ParameterType, any]):
        eni_exclude_list = {
            NeptuneCluster,
            NeptuneInstance,
            RedshiftCluster,
            RdsCluster,
            RdsInstance,
            ElasticSearchDomain,
            EksCluster,
            DmsReplicationInstance,
        }
        for ec2 in parameters.get(ParameterType.FIREWALL_EC2, []):
            for eni in ec2.network_resource.network_interfaces:
                eni_list.remove(eni)
        enis_to_delete = [eni for eni in eni_list if type(eni.owner) in eni_exclude_list]
        for eni in enis_to_delete:
            eni_list.remove(eni)

    def find_sg_issues(self, eni_list: AliasesDict[NetworkInterface]) -> Dict[NetworkInterface, Set[SecurityGroup]]:
        eni_to_sg_rules_map: Dict[NetworkInterface, Set[SecurityGroup]] = {}
        for eni in eni_list:
            is_eni_accessible_from_all_ips_on_port = any(
                self._is_public_connection(x) and
                self._is_all_ips_connection(x.connection_property) and
                self._is_connection_open_on_port(x.connection_property)
                for x in eni.inbound_connections
            )

            # Get security group that allows public access (any)
            if is_eni_accessible_from_all_ips_on_port:
                if self.port == KnownPorts.ALL:
                    eni_to_sg_rules_map[eni] = self._get_all_allow_all_port_range_sg(eni)
                else:
                    eni_to_sg_rules_map[eni] = self._get_all_allow_in_bound_port_sg(eni)

        return eni_to_sg_rules_map

    def _get_all_allow_in_bound_port_sg(self, eni: NetworkInterface) -> Set[SecurityGroup]:
        return {sg for sg in eni.security_groups for permission in sg.inbound_permissions
                if permission.is_in_range(self.port.value)
                and permission.property_type == SecurityGroupRulePropertyType.IP_RANGES and
                is_all_ips(permission.property_value)}

    @staticmethod
    def _get_all_allow_all_port_range_sg(eni: NetworkInterface) -> Set[SecurityGroup]:
        return {sg for sg in eni.security_groups for permission in sg.inbound_permissions
                if is_all_ports((permission.from_port, permission.to_port))
                and permission.property_type == SecurityGroupRulePropertyType.IP_RANGES and
                is_all_ips(permission.property_value)}

    @staticmethod
    def _is_public_connection(con_detail: ConnectionDetail):
        return con_detail.connection_type == ConnectionType.PUBLIC

    @staticmethod
    def _is_all_ips_connection(connection_property: PortConnectionProperty):
        return is_all_ips(connection_property.cidr_block)

    def _is_connection_open_on_port(self, connection_property: PortConnectionProperty):
        return any(port_range for port_range in connection_property.ports
                   if (self.port != KnownPorts.ALL and not is_all_ports(port_range) and is_port_in_range(port_range, self.port.value))
                   or (self.port == KnownPorts.ALL and is_all_ports(port_range)))


class PublicAccessSecurityGroupsSshPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_ssh_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.SSH)


class PublicAccessSecurityGroupsRdpPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_rdp_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.RDP)


class PublicAccessSecurityGroupsOracleDbDefaultPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_oracle_db_default_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.ORACLE_DB_DEFAULT)


class PublicAccessSecurityGroupsOracleDbPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_oracle_db_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.ORACLE_DB)


class PublicAccessSecurityGroupsOracleDbSslPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_oracle_db_ssl_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.ORACLE_DB_SSL)


class PublicAccessSecurityGroupsMySqlPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_mysql_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.MYSQL)


class PublicAccessSecurityGroupsPostgresPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_postgres_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.POSTGRES)


class PublicAccessSecurityGroupsRedisPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_redis_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.REDIS)


class PublicAccessSecurityGroupsMongodbPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_mongodb_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.MONGODB)


class PublicAccessSecurityGroupsMongodbShardClusterPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_mongodb_shard_cluster_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.MONGODB_SHARD_CLUSTER)


class PublicAccessSecurityGroupsCassandraPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_cassandra_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.CASSANDRA)


class PublicAccessSecurityGroupsCassandraThriftPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_cassandra_thrift_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.CASSANDRA_THRIFT)


class PublicAccessSecurityGroupsCassandraMngPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_cassandra_mng_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.CASSANDRA_MNG)


class PublicAccessSecurityGroupsMemcachedPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_memcached_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.MEMCACHED)


class PublicAccessSecurityGroupsElasticsearchNodesPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_elasticsearch_nodes_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.ELASTICSEARCH_NODES)


class PublicAccessSecurityGroupsElasticsearchPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_elasticsearch_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.ELASTICSEARCH)


class PublicAccessSecurityGroupsKibanaPortRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_kibana_port_rule'

    def __init__(self):
        super().__init__(KnownPorts.KIBANA)


class PublicAccessSecurityGroupsAllPortsRule(PublicAccessSecurityGroupsPortRule):

    def get_id(self) -> str:
        return 'public_access_security_groups_all_ports_rule'

    def __init__(self):
        super().__init__(KnownPorts.ALL)
