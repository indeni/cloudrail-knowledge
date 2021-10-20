from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.databases.azure_cosmos_db_account import AzureCosmosDBAccount, \
    CosmosDBAccountConsistencyPolicy, CosmosDBAccountConsistencyLevel, CosmosDBAccountGeoLocation, \
    CosmosDBAccountCapabilities, CosmosDBAccountVirtualNetworkRule, CosmosDBAccountMongoServerVersion, \
    CosmosDBAccountBackup, CosmosDBAccountCorsRule, CosmosDBAccountIdentity, ComosDBAccountBackupType

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class CosmosDBAccountBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureCosmosDBAccount:
        consistency_policy_list = []
        geo_location_list = []
        capabilities_list = []
        virtual_network_rule_list = []
        cors_rule_list = []
        identity_list = []
        backup_list = []
        for consistency_policy in attributes['consistency_policy']:
            consistency_policy_list.append(
                CosmosDBAccountConsistencyPolicy(CosmosDBAccountConsistencyLevel(self._get_known_value(consistency_policy, 'consistency_level')),
                                                 self._get_known_value(consistency_policy, 'max_interval_in_seconds'),
                                                 self._get_known_value(consistency_policy, 'max_staleness_prefix')))
        for geo_location in attributes['geo_location']:
            geo_location_list.append(CosmosDBAccountGeoLocation(self._get_known_value(geo_location, 'prefix'),
                                                                self._get_known_value(geo_location, 'location'),
                                                                self._get_known_value(geo_location, 'failover_priority'),
                                                                self._get_known_value(geo_location, 'zone_redundant')))
        if isinstance(attributes['backup'], list):
            for backup in attributes['backup']:
                if self._is_known_value(backup, 'typtypee') and self._is_known_value(backup, 'interval_in_minutes') and self._is_known_value(backup, 'retention_in_hours'):
                    backup_list.append(CosmosDBAccountBackup(ComosDBAccountBackupType(self._get_known_value(backup, 'type')),
                                                            self._get_known_value(backup, 'interval_in_minutes'),
                                                            self._get_known_value(backup, 'retention_in_hours')))

        for cors_rule in attributes['cors_rule']:
            cors_rule_list.append(CosmosDBAccountCorsRule(self._get_known_value(cors_rule, 'allowed_headers'),
                                                          self._get_known_value(cors_rule, 'allowed_methods'),
                                                          self._get_known_value(cors_rule, 'allowed_origins'),
                                                          self._get_known_value(cors_rule, 'exposed_headers'),
                                                          self._get_known_value(cors_rule, 'max_age_in_seconds')))

        for capabilities in attributes['capabilities']:
            capabilities_list.append(CosmosDBAccountCapabilities(self._get_known_value(capabilities, 'name')))

        for virtual_network_rule in attributes['virtual_network_rule']:
            virtual_network_rule_list.append(CosmosDBAccountVirtualNetworkRule(self._get_known_value(virtual_network_rule, 'id'),
                                                                               self._get_known_value(virtual_network_rule,
                                                                                                     'ignore_missing_vnet_service_endpoint')))
        for identity in attributes['identity']:
            identity_list.append(
                CosmosDBAccountIdentity(self._get_known_value(identity, 'type')))
        if attributes['mongo_server_version'].isnumeric():
            mongo_server_version = CosmosDBAccountMongoServerVersion(attributes['mongo_server_version'])
        else:
            mongo_server_version = None
        return AzureCosmosDBAccount(name=attributes['name'],
                                    offer_type=attributes['offer_type'],
                                    kind=self._get_known_value(attributes, 'kind'),
                                    consistency_policy_list=consistency_policy_list,
                                    geo_location_list=geo_location_list,
                                    ip_range_filter=self._get_known_value(attributes, 'ip_range_filter'),
                                    enable_free_tier=self._get_known_value(attributes, 'enable_free_tier'),
                                    analytical_storage_enabled=self._get_known_value(attributes, 'analytical_storage_enabled'),
                                    enable_automatic_failover=self._get_known_value(attributes, 'enable_automatic_failover'),
                                    public_network_access_enabled=self._get_known_value(attributes, 'public_network_access_enabled'),
                                    capabilities_list=capabilities_list,
                                    is_virtual_network_filter_enabled=self._get_known_value(attributes,'is_virtual_network_filter_enabled'),
                                    virtual_network_rule_list=virtual_network_rule_list,
                                    enable_multiple_write_locations=self._get_known_value(attributes,'enable_multiple_write_locations'),
                                    access_key_metadata_writes_enabled=self._get_known_value(attributes,'access_key_metadata_writes_enabled'),
                                    mongo_server_version=mongo_server_version,
                                    network_acl_bypass_for_azure_services=self._get_known_value(attributes,'network_acl_bypass_for_azure_services'),
                                    network_acl_bypass_ids=self._get_known_value(attributes,'network_acl_bypass_ids'),
                                    local_authentication_disabled=self._get_known_value(attributes,'local_authentication_disabled'),
                                    backup=backup_list,
                                    cors_rule_list=cors_rule_list,
                                    identity=identity_list,
                                    tags=self._get_known_value(attributes, 'tags'),
                                    key_vault_key_id=self._get_known_value(attributes,'key_vault_key_id'))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_COSMOSDB_ACCOUNT
