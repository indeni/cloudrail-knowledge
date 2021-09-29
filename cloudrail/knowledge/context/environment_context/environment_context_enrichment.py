from abc import abstractmethod

from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext


class EnvironmentContextEnrichment:

    @staticmethod
    @abstractmethod
    def enrich(environment_context: BaseEnvironmentContext, **extra_args) -> BaseEnvironmentContext:
        pass
