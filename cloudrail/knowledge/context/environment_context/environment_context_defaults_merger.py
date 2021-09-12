from abc import abstractmethod

from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext


class EnvironmentContextDefaultsMerger:

    @staticmethod
    @abstractmethod
    def merge_defaults(scanner_ctx: BaseEnvironmentContext, iac_ctx: BaseEnvironmentContext):
        pass
