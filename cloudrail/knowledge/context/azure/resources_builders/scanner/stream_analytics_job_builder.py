from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
from cloudrail.knowledge.context.azure.resources.stream_analytics.azure_stream_analytics_job import AzureStreamAnalyticsJob, StreamAnalyticsJobCompatibilityLevel, \
    StreamAnalyticsJobEventsPolicy, StreamAnalyticsJobIdentity, StreamAnalyticsJobIdentityType, StreamAnalyticsJobOutputErrorPolicy
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class StreamAnalyticsJobBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'list-stream_analytics_jobs.json'

    def do_build(self, attributes: dict) -> AzureStreamAnalyticsJob:
        properties = attributes['properties']
        transformation_data = properties['transformation']['properties']

        ## Identity
        identity = None
        if identity_data := attributes.get('identity'):
            identity = StreamAnalyticsJobIdentity(enum_implementation(StreamAnalyticsJobIdentityType, identity_data['type']))
        return AzureStreamAnalyticsJob(name=attributes['name'],
                                       compatibility_level=enum_implementation(StreamAnalyticsJobCompatibilityLevel, properties['compatibilityLevel']),
                                       data_locale=properties['dataLocale'],
                                       events_late_arrival_max_delay_in_seconds=properties['eventsLateArrivalMaxDelayInSeconds'],
                                       events_out_of_order_max_delay_in_seconds=properties['eventsOutOfOrderMaxDelayInSeconds'],
                                       events_out_of_order_policy=enum_implementation(StreamAnalyticsJobEventsPolicy, properties['eventsOutOfOrderPolicy']),
                                       identity=identity,
                                       output_error_policy=enum_implementation(StreamAnalyticsJobOutputErrorPolicy, properties['outputErrorPolicy']),
                                       stream_units=transformation_data['streamingUnits'],
                                       transformation_query=transformation_data['query'])
