from cloudrail.knowledge.context.azure.resources.subscription.azure_subscription import AzureSubscription
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class SubscriptionBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'subscription-list.json'

    def do_build(self, attributes: dict) -> AzureSubscription:
        subscription_name = attributes["displayName"]
        subscription_id = attributes["subscriptionId"]
        return AzureSubscription(subscription_name, subscription_id)
