import unittest

from parameterized import parameterized

from cloudrail.knowledge.context.cloud_provider import CloudProvider


class TestCloudProvider(unittest.TestCase):
    @parameterized.expand(
        [
            ['AWS', CloudProvider.AMAZON_WEB_SERVICES, 'aws'],
            ['Azure', CloudProvider.AZURE, 'azure'],
            ['GCP', CloudProvider.GCP, 'gcp'],
        ]
    )
    def test_to_shorthand_string(self, unused_name: str, cloud_provider: CloudProvider, expected_result: str):
        self.assertEqual(cloud_provider.to_shorthand_string(), expected_result)

    @parameterized.expand(
        [
            ['aws', CloudProvider.AMAZON_WEB_SERVICES, 'aws'],
            ['AMAZON_WEB_SERVICES', CloudProvider.AMAZON_WEB_SERVICES, 'AMAZON_WEB_SERVICES'],
            ['amazon_web_services', CloudProvider.AMAZON_WEB_SERVICES, 'amazon_web_services'],
            ['AmaZon_WeB_services', CloudProvider.AMAZON_WEB_SERVICES, 'AmaZon_WeB_services'],
            ['azure', CloudProvider.AZURE, 'azure'],
            ['AZURE', CloudProvider.AZURE, 'AZURE'],
            ['AzUrE', CloudProvider.AZURE, 'AzUrE'],
            ['gcp', CloudProvider.GCP, 'gcp'],
            ['GCP', CloudProvider.GCP, 'GCP'],
            ['GcP', CloudProvider.GCP, 'GcP'],
            ['google_cloud_provider', CloudProvider.GCP, 'google_cloud_provider'],
            ['GoOgLE_cloud_provider', CloudProvider.GCP, 'GoOgLE_cloud_provider'],
        ]
    )
    def test_from_string(self, unused_name: str, expected_cloud_provider: CloudProvider, value: str):
        self.assertEqual(CloudProvider.from_string(value), expected_cloud_provider)
