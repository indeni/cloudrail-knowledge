from cloudrail.knowledge.context.azure.azure_connection_builder import AzureConnectionBuilder
from cloudrail.knowledge.context.azure.azure_relations_assigner import AzureRelationsAssigner
from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator
from cloudrail.knowledge.context.environment_context.environment_context_enrichment import EnvironmentContextEnrichment
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext


class AzureEnvironmentContextEnrichment(EnvironmentContextEnrichment):

    @staticmethod
    def enrich(environment_context: AzureEnvironmentContext, **extra_args) -> AzureEnvironmentContext:
        AzureRelationsAssigner(environment_context).run()
        environment_context.clear_cache()
        ResourceInvalidator(environment_context).remove_invalid_resources()
        AzureConnectionBuilder(environment_context).run()
        return environment_context
