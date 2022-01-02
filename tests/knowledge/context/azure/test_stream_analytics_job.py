from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.stream_analytics.azure_stream_analytics_job import StreamAnalyticsJobCompatibilityLevel, StreamAnalyticsJobOutputErrorPolicy, \
    StreamAnalyticsJobEventsPolicy, StreamAnalyticsJobIdentity, StreamAnalyticsJobIdentityType
from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestStreamAnalyticsJob(AzureContextTest):

    def get_component(self):
        return "stream_analytics_job"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        sa_job = next((job for job in ctx.stream_analytics_jobs if job.name == 'cr3689a-stream-job'), None)
        self.assertIsNotNone(sa_job)
        self.assertEqual(sa_job.compatibility_level, StreamAnalyticsJobCompatibilityLevel.LEVEL_1_1)
        self.assertEqual(sa_job.data_locale, 'en-GB')
        self.assertEqual(sa_job.events_late_arrival_max_delay_in_seconds, 60)
        self.assertEqual(sa_job.events_out_of_order_max_delay_in_seconds, 50)
        self.assertEqual(sa_job.events_out_of_order_policy, StreamAnalyticsJobEventsPolicy.ADJUST)
        self.assertEqual(sa_job.identity, StreamAnalyticsJobIdentity(StreamAnalyticsJobIdentityType.SYSTEM_ASSIGNED))
        self.assertEqual(sa_job.output_error_policy, StreamAnalyticsJobOutputErrorPolicy.DROP)
        self.assertEqual(sa_job.stream_units, 3)
        self.assertEqual(sa_job.transformation_query, 'SELECT *\nINTO [YourOutputAlias]\nFROM [YourInputAlias]\n')
