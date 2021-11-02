from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation


class GcpRelationsAssigner(DependencyInvocation):

    def __init__(self, ctx: GcpEnvironmentContext = None):
        super().__init__(context=ctx)
        function_pool = [
        ]
        self.add_func_pool(function_pool)
