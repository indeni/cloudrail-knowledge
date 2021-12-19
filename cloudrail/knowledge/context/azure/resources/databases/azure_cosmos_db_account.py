from typing import Optional, List, Dict
from enum import Enum
from dataclasses import dataclass

import dataclasses
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting


class CosmosDBAccountIdentityType(Enum):
    SYSTEM_ASSIGNED = 'SystemAssigned'


class CosmosDBAccountKind(Enum):
    GLOBAL_DOCUMENTDB = 'GlobalDocumentDB'
    MONGODB = 'MongoDB'


class CosmosDBAccountConsistencyLevel(Enum):
    BOUNDED_STALENESS = 'BoundedStaleness'
    EVENTUAL = 'Eventual'
    SESSION = 'Session'
    STRONG = 'Strong'
    CONSISTENT_PREFIX = 'ConsistentPrefix'


class CosmosDBAccountMongoServerVersion(Enum):
    VERSION40 = '4.0'
    VERSION36 = '3.6'
    VERSION32 = '3.2'


class CosmosDBAccountCapabilitiesName(Enum):
    ALLOW_SELF_SERVER_UPGRADE_TO_MONGO36 = 'AllowSelfServeUpgradeToMongo36'
    DISABLE_RATE_LIMITING_RESPONSES = 'DisableRateLimitingResponses'
    ENABLE_AGGREAGATION_PIPELINE = 'EnableAggregationPipeline'
    ENABLE_CASSANDRA = 'EnableCassandra'
    ENABLE_GREMLIN = 'EnableGremlin'
    ENABLE_MONGO = 'EnableMongo'
    ENABLE_TABLE = 'EnableTable'
    ENABLE_SERVERLESS = 'EnableServerless'
    MONGODBV34 = 'MongoDBv3.4'
    MONGO_ENABLE_DOCLEVEL_TTL = 'mongoEnableDocLevelTTL'


class ComosDBAccountBackupType(Enum):
    CONTINUOUS = 'Continuous'
    PERIODIC = 'Periodic'


@dataclass
class CosmosDBAccountConsistencyPolicy:
    """
        Attributes:
            consistency_level: The Consistency Level to use for this CosmosDB Account - can be either BoundedStaleness,
                                Eventual, Session, Strong or ConsistentPrefix.
            max_interval_in_seconds: The time that staleness is tolerated.
            max_staleness_prefix: Number of stale requests tolerated.
    """
    consistency_level: CosmosDBAccountConsistencyLevel
    max_interval_in_seconds: Optional[int]
    max_staleness_prefix: Optional[int]


@dataclass
class CosmosDBAccountGeoLocation:
    """
        Attributes:
            prefix: The string used to generate the document endpoints for this region.
            location: The name of the Azure region to host replicated data.
            failover_priority: The failover priority of the region.
            zone_redundant: If zone redundancy should be enabled for this region.
    """
    prefix: Optional[str]
    location: str
    failover_priority: int
    zone_redundant: Optional[bool]


@dataclass
class CosmosDBAccountCapabilities:
    """
        Attributes:
            name: The capability to enable.
    """
    name: CosmosDBAccountCapabilitiesName


@dataclass
class CosmosDBAccountVirtualNetworkRule:
    """
        Attributes:
            id: The ID of the virtual network subnet
            ignore_missing_vnet_service_endpoint: If set to true, the specified subnet will be added as a virtual
                network rule even if its CosmosDB service endpoint is not active.
    """
    id: str
    ignore_missing_vnet_service_endpoint: Optional[bool]


@dataclass
class CosmosDBAccountBackup:
    """
        Attributes:
            type: Type of backup. Possible values 'Continuous' or 'Periodic'. Defaults to 'Periodic'
            interval_in_minutes: Internal in minutes between two backups.
            retention_in_hours: The time in hours that each backup is retained.
    """
    type: ComosDBAccountBackupType
    interval_in_minutes: Optional[int]
    retention_in_hours: Optional[int]


@dataclass
class CosmosDBAccountCorsRule:
    """
        Attributes:
            allowed_headers: A list of headers that are allowed to be a part of the cross-origin request.
            allowed_methods: Valid options are DELETE, GET, HEAD, MERGE, POST, OPTIONS, PUT or PATCH.
            allowed_origins: A list of origin domains that will be allowed by CORS.
            exposed_headers: A list of response headers that are exposed to CORS clients.
            max_age_in_seconds: The number of seconds the client should cache a preflight response.
    """
    allowed_headers: List[str]
    allowed_methods: List[str]
    allowed_origins: List[str]
    exposed_headers: List[str]
    max_age_in_seconds: int


@dataclass
class CosmosDBAccountIdentity:
    """
        Attributes:
            type: The type of Managed Service Identity that should be configured. Possible value is only 'SystemAssigned'.
    """
    type: CosmosDBAccountIdentityType


class AzureCosmosDBAccount(AzureResource):
    """
        Attributes:
            name: The CosmosDB account anem
            tags: A mapping of tags to assign to the Cosmos DB account.
            offer_type: Offer Type to use. Currently, only "Standard" is supported.
            kind: Kind of CosmosDB. Possible values "GlobalDocumentDB (default) or "MongoDB".
            consistency_policy_list: Consistency policy for this CosmosDB account.
            geo_location: Geolocation configuration to define where data should be replicated.
            ip_range_filter: Comma separated value of IP addresses/ranges to be included in the allowed list.
            enable_free_tier: Whether enable Free Tier pricing for Cosmos DB Account.
            analytical_storage_enabled: Enable Analytical Storage option for this Cosmos DB account.
            enable_automatic_failover: Enable automatic fail over for this Cosmos DB account.
            public_network_access_enabled: Whether or not public network access is allowed for this CosmosDB account.
            capabilities_list: The capabilities which should be enabled for this Cosmos DB account.
            is_virtual_network_filter_enabled: Enables virtual network filtering for this Cosmos DB account.
            key_vault_key_id: A versionless Key Vault Key ID for CMK encryption.
            virtual_network_rule: Used to define which subnets are allowed to access this CosmosDB account.
            enable_multiple_write_locations: Enable multiple write locations for this Cosmos DB account.
            access_key_metadata_writes_enabled: Enable write operations on metadata resources.
            mongo_server_version: The Server Version of a MongoDB account. Possible values are 4.0, 3.6, and 3.2.
            network_acl_bypass_for_azure_services: If azure services can bypass ACLs.
            network_acl_bypass_ids: The list of resource Ids for Network Acl Bypass for this Cosmos DB account.
            local_authentication_disabled: Disable local authentication and ensure only MSI and AAD can be used exclusively for authentication.
            backup: CosmosDB account backup configuration.
            cors_rule: CosmosDB account cors rule configuration.
            identity: CosmosDB account identity configuration.
    """
    def __init__(self,
                 name: str,
                 offer_type: str,
                 kind: CosmosDBAccountKind,
                 consistency_policy_list: List[CosmosDBAccountConsistencyPolicy],
                 geo_location_list: List[CosmosDBAccountGeoLocation],
                 ip_range_filter: Optional[str],
                 enable_free_tier: bool,
                 analytical_storage_enabled: bool,
                 enable_automatic_failover: bool,
                 public_network_access_enabled: bool,
                 capabilities_list: List[CosmosDBAccountCapabilities],
                 is_virtual_network_filter_enabled: bool,
                 virtual_network_rule_list: List[CosmosDBAccountVirtualNetworkRule],
                 enable_multiple_write_locations: bool,
                 access_key_metadata_writes_enabled: bool,
                 mongo_server_version: Optional[CosmosDBAccountMongoServerVersion],
                 network_acl_bypass_for_azure_services: bool,
                 network_acl_bypass_ids: List[str],
                 local_authentication_disabled: bool,
                 backup: List[CosmosDBAccountBackup],
                 cors_rule_list: List[CosmosDBAccountCorsRule],
                 identity: List[CosmosDBAccountIdentity],
                 tags: Dict[str, str] = None,
                 key_vault_key_id: Optional[str] = None):

        super().__init__(AzureResourceType.AZURERM_COSMOSDB_ACCOUNT)
        self.name: str = name
        if tags:
            self.tags = tags
        self.offer_type: str = offer_type
        self.kind: Optional[CosmosDBAccountKind] = kind
        self.consistency_policy_list: List[CosmosDBAccountConsistencyPolicy] = consistency_policy_list
        self.geo_location_list: List[CosmosDBAccountGeoLocation] = geo_location_list
        self.ip_range_filter: Optional[str] = ip_range_filter
        self.enable_free_tier: bool = enable_free_tier
        self.analytical_storage_enabled: bool = analytical_storage_enabled
        self.enable_automatic_failover: bool = enable_automatic_failover
        self.public_network_access_enabled: bool = public_network_access_enabled
        self.capabilities_list: List[CosmosDBAccountCapabilities] = capabilities_list
        self.is_virtual_network_filter_enabled: bool = is_virtual_network_filter_enabled
        self.enable_multiple_write_locations: bool = enable_multiple_write_locations
        self.access_key_metadata_writes_enabled: bool = access_key_metadata_writes_enabled
        self.mongo_server_version: Optional[CosmosDBAccountMongoServerVersion] = mongo_server_version
        self.network_acl_bypass_for_azure_services: bool = network_acl_bypass_for_azure_services
        self.local_authentication_disabled: bool = local_authentication_disabled
        self.backup: List[CosmosDBAccountBackup] = backup
        self.cors_rule_list: List[CosmosDBAccountCorsRule] = cors_rule_list
        self.identity: List[CosmosDBAccountIdentity] = identity

        # References to other resources
        self.key_vault_key_id: Optional[str] = key_vault_key_id
        self.virtual_network_rule_list: Optional[List[CosmosDBAccountVirtualNetworkRule]
                                            ] = virtual_network_rule_list
        self.network_acl_bypass_ids: List[str] = network_acl_bypass_ids

        # Resources part of the context
        self.monitor_diagnostic_settings: List[AzureMonitorDiagnosticSetting] = [
        ]

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.DocumentDB/databaseAccounts/{self.name}/overview'

    @property
    def is_tagable(self) -> bool:
        return True

    @staticmethod
    def is_standalone() -> bool:
        return True

    def get_keys(self) -> List[str]:
        return [self._id]

    def get_type(self, is_plural: bool = False) -> str:
        return 'CosmosDB Account' if not is_plural else 'CosmosDB Accounts'

    def get_name(self) -> str:
        return self.name

    def to_drift_detection_object(self) -> dict:
        return {'tags': self.tags, 'name': self.name,
                'offer_type': self.offer_type,
                'kind': self.kind.value,
                'consistency_policy_list': [dataclasses.asdict(location) for location in self.geo_location_list],
                'ip_range_filter': self.ip_range_filter,
                'enable_free_tier': self.enable_free_tier,
                'analytical_storage_enabled': self.analytical_storage_enabled,
                'enable_automatic_failover': self.enable_automatic_failover,
                'public_network_access_enabled': self.public_network_access_enabled,
                'capabilities_list': [dataclasses.asdict(capabilities) for capabilities in self.capabilities_list],
                'is_virtual_network_filter_enabled': self.is_virtual_network_filter_enabled,
                'virtual_network_rule_list': [dataclasses.asdict(rule) for rule in self.virtual_network_rule_list],
                'enable_multiple_write_locations': self.enable_multiple_write_locations,
                'access_key_metadata_writes_enabled': self.access_key_metadata_writes_enabled,
                'mongo_server_version': self.mongo_server_version and self.mongo_server_version.value,
                'network_acl_bypass_for_azure_services': self.network_acl_bypass_for_azure_services,
                'network_acl_bypass_ids': self.network_acl_bypass_ids,
                'local_authentication_disabled': self.local_authentication_disabled,
                'backup': [dataclasses.asdict(back) for back in self.backup],
                'cors_rule_list': [dataclasses.asdict(rule) for rule in self.cors_rule_list],
                'identity': [dataclasses.asdict(iden) for iden in self.identity],
                'key_vault_key_id': self.key_vault_key_id}
