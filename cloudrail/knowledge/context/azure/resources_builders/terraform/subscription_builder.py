from cloudrail.knowledge.context.azure.resources.subscription.azure_subscription import AzureSubscription
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class SubscriptionBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSubscription:
        subscription_name = attributes["subscription_name"]
        subscription_id = attributes["subscription_id"]
        return AzureSubscription(subscription_name, subscription_id)

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_SUBSCRIPTION
