from cloudrail.knowledge.context.azure.resources.security.azure_security_center_subscription_pricing import AzureSecurityCenterSubscriptionPricing, \
    SubscriptionPricingTier, SubscriptionPricingResourceType

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class SecurityCenterSubscriptionPricingBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'subscription-security-pricings.json'

    def do_build(self, attributes: dict) -> AzureSecurityCenterSubscriptionPricing:
        return AzureSecurityCenterSubscriptionPricing(tier=SubscriptionPricingTier(attributes['properties']['pricingTier']),
                                                      resource_type=SubscriptionPricingResourceType(attributes['name']))
