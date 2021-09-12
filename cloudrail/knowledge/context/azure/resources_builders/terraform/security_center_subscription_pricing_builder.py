from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.security.azure_security_center_subscription_pricing import AzureSecurityCenterSubscriptionPricing, \
    SubscriptionPricingResourceType, SubscriptionPricingTier

from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class SecurityCenterSubscriptionPricingBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureSecurityCenterSubscriptionPricing:
        return AzureSecurityCenterSubscriptionPricing(resource_type=SubscriptionPricingResourceType(attributes['resource_type']),
                                                      tier=SubscriptionPricingTier(attributes['tier']))

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_SECURITY_CENTER_SUBSCRIPTION_PRICING
