from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.iot.azure_iot_hub import AzureIoTHub, IoTHubSku, IoTHubSkuName, IoTHubIpFilterRule, IoTHubIpFilterRuleAction, \
    IoTHubEndpoint, IoTHubEndpointType, IoTHubEndpointEncoding, IoTHubFallbackRoute, IoTHubRouteSource, IoTHubFileUpload, IoTHubRoute, IoTHubEnrichment
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class IoTHubBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureIoTHub:

        ## Endpoints
        endpoint_list = []
        for endpoint in self._get_known_value(attributes, 'endpoint', []):
            endpoint_type = IoTHubEndpointType(endpoint['type'])
            batch_frequency_in_seconds = None
            max_chunk_size_in_bytes = None
            encoding = None
            if endpoint_type == IoTHubEndpointType.STORAGE_CONTAINER:
                batch_frequency_in_seconds = self._get_known_value(endpoint, 'batch_frequency_in_seconds', 300)
                max_chunk_size_in_bytes = self._get_known_value(endpoint, 'max_chunk_size_in_bytes', 314572800)
                encoding = IoTHubEndpointEncoding(self._get_known_value(endpoint, 'encoding', 'avro').lower())
            endpoint_list.append(IoTHubEndpoint(type=endpoint_type,
                                                connection_string=endpoint['connection_string'],
                                                name=endpoint['name'],
                                                batch_frequency_in_seconds=batch_frequency_in_seconds,
                                                max_chunk_size_in_bytes=max_chunk_size_in_bytes,
                                                container_name=self._get_known_value(endpoint, 'container_name'),
                                                encoding=encoding,
                                                file_name_format=self._get_known_value(endpoint, 'file_name_format'),
                                                resource_group_name=self._get_known_value(endpoint, 'resource_group_name')))

        ## Fallback route
        fallback_route = IoTHubFallbackRoute(IoTHubRouteSource('DeviceMessages'), 'true', ['events'], False)

        if fallback_route_data := self._get_known_value(attributes, 'fallback_route'):
            source = None
            if source_value := self._get_known_value(fallback_route_data[0], 'source'):
                source = IoTHubRouteSource(source_value)
            fallback_route = IoTHubFallbackRoute(source=source,
                                                 condition=self._get_known_value(fallback_route_data[0], 'condition', 'true'),
                                                 endpoint_names=self._get_known_value(fallback_route_data[0], 'endpoint_names', []),
                                                 enabled=self._get_known_value(fallback_route_data[0], 'enabled', True))

        ## File Upload
        file_upload = None
        if file_data := self._get_known_value(attributes, 'file_upload'):
            file_upload = IoTHubFileUpload(connection_string=file_data[0]['connection_string'],
                                           container_name=file_data[0]['container_name'],
                                           sas_ttl=self._get_known_value(file_data[0], 'sas_ttl', 'PT1M'),
                                           notifications=self._get_known_value(file_data[0], 'notifications', False),
                                           lock_duration=self._get_known_value(file_data[0], 'lock_duration', 'PT1M'),
                                           default_ttl=self._get_known_value(file_data[0], 'default_ttl', 'PT1M'),
                                           max_delivery_count=self._get_known_value(file_data[0], 'max_delivery_count', 10))

        ## IP Filter rules
        ip_filter_rule_list = []
        for rule in self._get_known_value(attributes, 'ip_filter_rule', []):
            ip_filter_rule_list.append(IoTHubIpFilterRule(name=rule['name'],
                                                          ip_mask=rule['ip_mask'],
                                                          action=IoTHubIpFilterRuleAction(rule['action'])))

        ## Routes
        route_list = []
        for route in self._get_known_value(attributes, 'route', []):
            route_list.append(IoTHubRoute(name=route['name'],
                                          source=IoTHubRouteSource(route['source']),
                                          condition=self._get_known_value(route, 'condition', 'true'),
                                          endpoint_names=route['endpoint_names'],
                                          enabled=route['enabled']))

        ## Encrichment
        enrichment_list = []
        for route in self._get_known_value(attributes, 'enrichment', []):
            enrichment_list.append(IoTHubEnrichment(key=route['key'],
                                                    value=route['value'],
                                                    endpoint_names=route['endpoint_names']))

        sku_data = attributes['sku']
        return AzureIoTHub(name=attributes['name'],
                           sku=IoTHubSku(IoTHubSkuName(sku_data[0]['name']), sku_data[0]['capacity']),
                           event_hub_partition_count=self._get_known_value(attributes, 'event_hub_partition_count', 4),
                           event_hub_retention_in_days=self._get_known_value(attributes, 'event_hub_retention_in_days', 1),
                           endpoint_list=endpoint_list,
                           fallback_route=fallback_route,
                           file_upload=file_upload,
                           ip_filter_rule_list=ip_filter_rule_list,
                           route_list=route_list,
                           enrichment_list=enrichment_list,
                           public_network_access_enabled=self._get_known_value(attributes, 'public_network_access_enabled', False),
                           min_tls_version=self._get_known_value(attributes, 'min_tls_version', '1.0'))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_IOT_HUB
