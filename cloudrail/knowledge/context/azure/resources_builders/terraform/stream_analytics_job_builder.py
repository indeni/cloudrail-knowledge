from cloudrail.knowledge.context.azure.resources.stream_analytics.azure_stream_analytics_job import AzureStreamAnalyticsJob, StreamAnalyticsJobCompatibilityLevel, \
    StreamAnalyticsJobEventsPolicy, StreamAnalyticsJobIdentity, StreamAnalyticsJobIdentityType, StreamAnalyticsJobOutputErrorPolicy
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class StreamAnalyticsJobBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureStreamAnalyticsJob:
        identity = None
        if identity_data := self._get_known_value(attributes, 'identity'):
            identity = StreamAnalyticsJobIdentity(type=StreamAnalyticsJobIdentityType(self._get_known_value(identity_data[0], 'type','SystemAssigned')))
        return AzureStreamAnalyticsJob(name=attributes['name'],
                                       compatibility_level=enum_implementation(StreamAnalyticsJobCompatibilityLevel,
                                                                               self._get_known_value(attributes, 'compatibility_level', '1.0')),
                                       data_locale=self._get_known_value(attributes, 'data_locale', 'en-US'),
                                       events_late_arrival_max_delay_in_seconds=self._get_known_value(attributes,
                                                                                                      'events_late_arrival_max_delay_in_seconds', 5),
                                       events_out_of_order_max_delay_in_seconds=self._get_known_value(attributes,
                                                                                                      'events_out_of_order_max_delay_in_seconds', 0),
                                       events_out_of_order_policy=enum_implementation(StreamAnalyticsJobEventsPolicy,
                                                                                      self._get_known_value(attributes, 'events_out_of_order_policy', 'Adjust')),
                                       identity=identity,
                                       output_error_policy=enum_implementation(StreamAnalyticsJobOutputErrorPolicy,
                                                                               self._get_known_value(attributes, 'output_error_policy', 'Drop')),
                                       stream_units=attributes['streaming_units'],
                                       transformation_query=attributes['transformation_query'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_STREAM_ANALYTICS_JOB
