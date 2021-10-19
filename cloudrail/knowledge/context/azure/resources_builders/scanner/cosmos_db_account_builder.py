from typing import List
from cloudrail.knowledge.context.azure.resources.databases.azure_cosmos_db_account import AzureCosmosDBAccount, \
    CosmosDBAccountMongoServerVersion, CosmosDBAccountConsistencyPolicy, CosmosDBAccountConsistencyLevel, \
    CosmosDBAccountGeoLocation, CosmosDBAccountBackup, CosmosDBAccountCorsRule, CosmosDBAccountCapabilities, \
    CosmosDBAccountVirtualNetworkRule, CosmosDBAccountIdentity

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class CosmosDBAccountBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'cosmos-db-account.json'

    def do_build(self, attributes: dict) -> AzureCosmosDBAccount:
        properties = attributes['properties']
        consistency_policy_list = []
        geo_location_list = []
        capabilities_list = []
        virtual_network_rule_list = []
        cors_rule_list = []
        identity_list = []
        backup_list = []
        public_network_access_enabled = True
        mongo_server_version = None
        ip_range_filter = None
        if not isinstance(properties['consistencyPolicy'], list):
            properties['consistencyPolicy'] = [properties['consistencyPolicy']]
        for consistency_policy in properties['consistencyPolicy']:
            consistency_policy_list.append(CosmosDBAccountConsistencyPolicy(
                CosmosDBAccountConsistencyLevel(consistency_policy.get('defaultConsistencyLevel')),
                consistency_policy.get('maxIntervalInSeconds'),
                consistency_policy.get('maxStalenessPrefix')))
        if not isinstance(properties['readLocations'], List):
            properties['readLocations'] = [properties['readLocations']]
        for geo_location in properties['readLocations']:
            geo_location_list.append(CosmosDBAccountGeoLocation(geo_location.get('prefix'),
                                                                geo_location.get('locationName'),
                                                                geo_location.get('failoverPriority'),
                                                                geo_location.get('isZoneRedundant')))
        if not isinstance(properties['backupPolicy'], List):
            properties['backupPolicy'] = [properties['backupPolicy']]
        for backup in properties['backupPolicy']:
            backup_list.append(CosmosDBAccountBackup(backup.get('type'),
                                                     backup['periodicModeProperties'].get('backupIntervalInMinutes'),
                                                     backup['periodicModeProperties'].get('backupRetentionIntervalInHours')))
        if not isinstance(properties['cors'], List):
            properties['cors'] = [properties['cors']]
        for cors_rule in properties['cors']:
            cors_rule_list.append(CosmosDBAccountCorsRule(cors_rule.get('allowedHeaders', '').split(','),
                                                          cors_rule.get('allowedMethods', '').split(','),
                                                          cors_rule.get('allowedOrigins', '').split(','),
                                                          cors_rule.get('exposedHeaders', '').split(','),
                                                          cors_rule.get('maxAgeInSeconds')))
        if not isinstance(properties['capabilities'], List):
            properties['capabilities'] = [properties['capabilities']]
        for capabilities in properties['capabilities']:
            capabilities_list.append(CosmosDBAccountCapabilities(capabilities.get('name')))
        if not isinstance(properties['virtualNetworkRules'], List):
            properties['virtualNetworkRules'] = [properties['virtualNetworkRules']]
        for virtual_network_rule in properties['virtualNetworkRules']:
            virtual_network_rule_list.append(
                CosmosDBAccountVirtualNetworkRule(virtual_network_rule.get('id'),
                                                  virtual_network_rule.get('ignoreMissingVNetServiceEndpoint')))
        if not isinstance(attributes['identity'], List):
            attributes['identity'] = [attributes['identity']]
        for identity in attributes['identity']:
            identity_list.append(
                CosmosDBAccountIdentity(identity.get('type')))
        if properties['publicNetworkAccess'] == 'Disabled':
            public_network_access_enabled = False
        if properties.get('ipRules') and properties['ipRules'][0].get('ipAddressOrRange'):
            ip_range_filter = properties['ipRules'][0]['ipAddressOrRange']

        if properties.get('apiProperties'):
            if properties['apiProperties'].get('serverVersion'):
                mongo_server_version = CosmosDBAccountMongoServerVersion(
                                        properties['apiProperties']['serverVersion'])

        return AzureCosmosDBAccount(name=attributes.get('name'),
                                    offer_type=properties.get('databaseAccountOfferType'),
                                    kind=attributes.get('kind'),
                                    consistency_policy_list=consistency_policy_list,
                                    geo_location_list=geo_location_list,
                                    ip_range_filter=ip_range_filter,
                                    enable_free_tier=properties.get('enableFreeTier'),
                                    analytical_storage_enabled=properties.get('enableAnalyticalStorage'),
                                    enable_automatic_failover=properties.get('enableAutomaticFailover'),
                                    public_network_access_enabled=public_network_access_enabled,
                                    capabilities_list=capabilities_list,
                                    is_virtual_network_filter_enabled=properties.get('isVirtualNetworkFilterEnabled'),
                                    virtual_network_rule_list=virtual_network_rule_list,
                                    enable_multiple_write_locations=properties.get('enableMultipleWriteLocations'),
                                    access_key_metadata_writes_enabled=not properties.get('disableKeyBasedMetadataWriteAccess'),
                                    mongo_server_version=mongo_server_version,
                                    network_acl_bypass_for_azure_services=properties.get('networkAclBypass') == 'AzureServices',
                                    network_acl_bypass_ids=properties.get('networkAclBypassResourceIds'),
                                    local_authentication_disabled=None,
                                    backup=backup_list,
                                    cors_rule_list=cors_rule_list,
                                    identity=identity_list,
                                    tags=attributes.get('tags'),
                                    key_vault_key_id=properties.get('keyVaultKeyUri'))
