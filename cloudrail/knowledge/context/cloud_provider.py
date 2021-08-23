from enum import Enum


class CloudProvider(str, Enum):
    AMAZON_WEB_SERVICES = 'amazon_web_services'
    AZURE = 'azure'
    GCP = 'google_cloud_provider'

    @staticmethod
    def from_string(string):
        if string.lower() == 'aws':
            return CloudProvider.AMAZON_WEB_SERVICES
        try:
            return CloudProvider(string.lower())
        except Exception:
            return CloudProvider[string.upper()]

    def to_shorthand_string(self):
        if self == CloudProvider.AMAZON_WEB_SERVICES:
            return 'aws'
        return str(self.name).lower()
