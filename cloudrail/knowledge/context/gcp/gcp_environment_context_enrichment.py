from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator
from cloudrail.knowledge.context.gcp.gcp_connection_builder import GcpConnectionBuilder
from cloudrail.knowledge.context.gcp.gcp_relations_assigner import GcpRelationsAssigner
from cloudrail.knowledge.context.environment_context.environment_context_enrichment import EnvironmentContextEnrichment


class GcpEnvironmentContextEnrichment(EnvironmentContextEnrichment):

    @staticmethod
    def enrich(environment_context: GcpEnvironmentContext, **extra_args) -> GcpEnvironmentContext:
        GcpRelationsAssigner(environment_context).run()
        environment_context.clear_cache()
        ResourceInvalidator(environment_context).remove_invalid_resources()
        GcpConnectionBuilder(environment_context).run()
        return environment_context
