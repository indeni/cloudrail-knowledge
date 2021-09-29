from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext

from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation


class GcpRelationsAssigner(DependencyInvocation):

    def __init__(self, ctx: GcpEnvironmentContext = None):
        function_pool = [
        ]

        super().__init__(function_pool, context=ctx)
