from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_user_assigned_identity import AzureAssignedUserIdentity
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder


class AssignedUserIdentityBuilder(AzureTerraformBuilder):

    def do_build(self, attributes: dict) -> AzureAssignedUserIdentity:
        return AzureAssignedUserIdentity(identity_name=attributes['name'],
                                         client_id=attributes.get('client_id'),
                                         principal_id=attributes.get('principal_id'),
                                         tenant_id=attributes.get('tenant_id') or attributes['tenant_id'])

    def get_service_name(self) -> AzureResourceType:
        return AzureResourceType.AZURERM_USER_ASSIGNED_IDENTITY
