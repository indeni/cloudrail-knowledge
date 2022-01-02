from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.iot.azure_iot_hub import IoTHubSkuName, IoTHubIpFilterRuleAction, IoTHubEndpointType, IoTHubEndpointEncoding, \
    IoTHubRouteSource
from cloudrail.knowledge.context.mergeable import EntityOrigin
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestIoTHub(AzureContextTest):

    def get_component(self):
        return "iot_hub"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        iot_hub = next((hub for hub in ctx.iot_hubs if hub.name == 'cr3685-IoTHub'), None)
        self.assertIsNotNone(iot_hub)
        self.assertEqual(iot_hub.sku.name, IoTHubSkuName.S1)
        self.assertEqual(iot_hub.sku.capacity, 1)
        self.assertEqual(iot_hub.event_hub_partition_count, 2)
        self.assertEqual(iot_hub.event_hub_retention_in_days, 1)
        self.assertEqual(len(iot_hub.ip_filter_rule_list), 1)
        ip_filter_rule = next((rule for rule in iot_hub.ip_filter_rule_list if rule.name == 'sample'), None)
        self.assertIsNotNone(ip_filter_rule)
        self.assertEqual(ip_filter_rule.action, IoTHubIpFilterRuleAction.ACCEPT)
        self.assertEqual(ip_filter_rule.ip_mask, '10.0.10.0/24')
        self.assertFalse(iot_hub.public_network_access_enabled)
        self.assertEqual(iot_hub.min_tls_version, '1.2')
        self.assertEqual(len(iot_hub.endpoint_list), 1)
        endpoint = next((endpoint for endpoint in iot_hub.endpoint_list if endpoint.name == 'export'), None)
        self.assertIsNotNone(endpoint)
        self.assertEqual(endpoint.batch_frequency_in_seconds, 60)
        self.assertEqual(endpoint.max_chunk_size_in_bytes, 10485760)
        self.assertEqual(endpoint.container_name, 'examplecontainer')
        self.assertEqual(endpoint.encoding, IoTHubEndpointEncoding.AVRO)
        self.assertEqual(endpoint.file_name_format, '{iothub}/{partition}_{YYYY}_{MM}_{DD}_{HH}_{mm}')
        self.assertEqual(endpoint.resource_group_name, 'cr3685-RG')
        self.assertEqual(endpoint.type, IoTHubEndpointType.STORAGE_CONTAINER)
        if iot_hub.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(endpoint.connection_string,
                             'DefaultEndpointsProtocol=https;BlobEndpoint='
                             'https://cr3685tststacc.blob.core.windows.net/;AccountName=cr3685tststacc;AccountKey=****')
        else:
            self.assertEqual(endpoint.connection_string, 'azurerm_storage_account.storacc.primary_blob_connection_string')
        self.assertEqual(iot_hub.fallback_route.condition, 'true')
        self.assertTrue(iot_hub.fallback_route.enabled)
        self.assertEqual(iot_hub.fallback_route.source, IoTHubRouteSource.DEVICE_MESSAGES)
        self.assertEqual(iot_hub.fallback_route.endpoint_names, ["export"])
        self.assertTrue(iot_hub.file_upload)
        self.assertEqual(iot_hub.file_upload.container_name, 'examplecontainer')
        self.assertEqual(iot_hub.file_upload.sas_ttl, 'PT1H')
        self.assertFalse(iot_hub.file_upload.notifications)
        self.assertEqual(iot_hub.file_upload.lock_duration, 'PT1M')
        self.assertEqual(iot_hub.file_upload.default_ttl, 'PT1H')
        self.assertEqual(iot_hub.file_upload.max_delivery_count, 10)
        if iot_hub.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(iot_hub.file_upload.connection_string,
                             'DefaultEndpointsProtocol=https;BlobEndpoint='
                             'https://cr3685tststacc.blob.core.windows.net/;AccountName=cr3685tststacc;AccountKey=****')
        else:
            self.assertEqual(iot_hub.file_upload.connection_string, 'azurerm_storage_account.storacc.primary_blob_connection_string')
        self.assertEqual(len(iot_hub.route_list), 1)
        route = next((route for route in iot_hub.route_list if route.name == 'export'), None)
        self.assertIsNotNone(route)
        self.assertEqual(route.condition, 'true')
        self.assertEqual(route.source, IoTHubRouteSource.DEVICE_MESSAGES)
        self.assertEqual(route.endpoint_names, ["export"])
        self.assertTrue(route.enabled)
        self.assertEqual(len(iot_hub.enrichment_list), 1)
        enrichment = next((enrichment for enrichment in iot_hub.enrichment_list if enrichment.key == 'tenant'), None)
        self.assertIsNotNone(enrichment)
        self.assertEqual(enrichment.value, '$twin.tags.Tenant')
        self.assertEqual(enrichment.endpoint_names, ["export"])
        self.assertEqual(len(iot_hub.monitor_diagnostic_settings), 1)
        diag = next((diag for diag in iot_hub.monitor_diagnostic_settings if diag.name == 'example'), None)
        self.assertIsNotNone(diag)
