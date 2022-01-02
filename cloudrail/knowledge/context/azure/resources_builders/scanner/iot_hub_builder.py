from cloudrail.knowledge.context.azure.resources.iot.azure_iot_hub import AzureIoTHub, IoTHubSku, IoTHubSkuName, IoTHubIpFilterRule, IoTHubIpFilterRuleAction, \
    IoTHubEndpoint, IoTHubEndpointType, IoTHubEndpointEncoding, IoTHubFallbackRoute, IoTHubRouteSource, IoTHubFileUpload, IoTHubRoute, IoTHubEnrichment
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class IoTHubBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-iot-hubs.json'

    def do_build(self, attributes: dict) -> AzureIoTHub:

        iot_propertries = attributes['properties']
        routing_data = iot_propertries['routing']
        ## Endpoints
        endpoint_list = []
        endpoints_data = routing_data['endpoints']

        for endpoint in endpoints_data.get('serviceBusQueues', []):
            endpoint['type'] = 'AzureIotHub.ServiceBusQueue'
            endpoint_list.append(self._build_iot_hub_endpoint(endpoint))

        for endpoint in endpoints_data.get('serviceBusTopics', []):
            endpoint['type'] = 'AzureIotHub.ServiceBusTopic'
            endpoint_list.append(self._build_iot_hub_endpoint(endpoint))

        for endpoint in endpoints_data.get('eventHubs', []):
            endpoint['type'] = 'AzureIotHub.EventHub'
            endpoint_list.append(self._build_iot_hub_endpoint(endpoint))

        for endpoint in endpoints_data.get('storageContainers', []):
            endpoint['type'] = 'AzureIotHub.StorageContainer'
            endpoint_list.append(self._build_iot_hub_endpoint(endpoint))

        ## Fallback route
        fall_back_route_data = routing_data['fallbackRoute']
        fallback_route = IoTHubFallbackRoute(source=IoTHubRouteSource(fall_back_route_data['source']),
                                             condition=fall_back_route_data['condition'],
                                             endpoint_names=fall_back_route_data['endpointNames'],
                                             enabled=fall_back_route_data['isEnabled'])

        ## File Upload
        file_upload = None
        if file_upload_data := iot_propertries.get('storageEndpoints', {}).get('$default'):
            cloud_to_device_data = iot_propertries['cloudToDevice']
            file_upload = IoTHubFileUpload(connection_string=file_upload_data['connectionString'],
                                           container_name=file_upload_data['containerName'],
                                           sas_ttl=file_upload_data['sasTtlAsIso8601'],
                                           notifications=iot_propertries['enableFileUploadNotifications'],
                                           lock_duration=iot_propertries['messagingEndpoints']['fileNotifications']['lockDurationAsIso8601'],
                                           default_ttl=cloud_to_device_data['defaultTtlAsIso8601'],
                                           max_delivery_count=cloud_to_device_data['maxDeliveryCount'])

        ## IP Filter rules
        ip_filter_rule_list = []
        for rule in iot_propertries.get('ipFilterRules'):
            ip_filter_rule_list.append(IoTHubIpFilterRule(name=rule['filterName'],
                                                          ip_mask=rule['ipMask'],
                                                          action=IoTHubIpFilterRuleAction(rule['action'])))

        ## Routes
        route_list = []
        for route in routing_data.get('routes'):
            route_list.append(IoTHubRoute(name=route['name'],
                                          source=IoTHubRouteSource(route['source']),
                                          condition=route.get('condition', 'true'),
                                          endpoint_names=route['endpointNames'],
                                          enabled=route['isEnabled']))

        ## Encrichment
        enrichment_list = []
        for enrichment in routing_data.get('enrichments'):
            enrichment_list.append(IoTHubEnrichment(key=enrichment['key'],
                                                    value=enrichment['value'],
                                                    endpoint_names=enrichment['endpointNames']))

        sku_data = attributes['sku']
        event_hub_data = iot_propertries['eventHubEndpoints']['events']
        return AzureIoTHub(name=attributes['name'],
                           sku=IoTHubSku(IoTHubSkuName(sku_data['name']), sku_data['capacity']),
                           event_hub_partition_count=event_hub_data['partitionCount'],
                           event_hub_retention_in_days=event_hub_data['retentionTimeInDays'],
                           endpoint_list=endpoint_list,
                           fallback_route=fallback_route,
                           file_upload=file_upload,
                           ip_filter_rule_list=ip_filter_rule_list,
                           route_list=route_list,
                           enrichment_list=enrichment_list,
                           public_network_access_enabled=iot_propertries.get('publicNetworkAccess') == 'Enabled',
                           min_tls_version=iot_propertries['minTlsVersion'])


    @staticmethod
    def _build_iot_hub_endpoint(attributes: dict) -> IoTHubEndpoint:
        if encoding := attributes.get('encoding'):
            encoding = IoTHubEndpointEncoding(encoding.lower())
        return IoTHubEndpoint(type=IoTHubEndpointType(attributes['type']),
                              name=attributes['name'],
                              connection_string=attributes['connectionString'],
                              batch_frequency_in_seconds=attributes.get('batchFrequencyInSeconds'),
                              max_chunk_size_in_bytes=attributes.get('maxChunkSizeInBytes'),
                              container_name=attributes.get('containerName'),
                              encoding=encoding,
                              file_name_format=attributes.get('fileNameFormat'),
                              resource_group_name=attributes['resourceGroup'])
