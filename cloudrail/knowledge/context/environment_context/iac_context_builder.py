from abc import abstractmethod
from typing import Optional

from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext


class IacContextBuilder:

    @staticmethod
    @abstractmethod
    def build(iac_file: str, account_id: str, scanner_environment_context: Optional[BaseEnvironmentContext], salt: Optional[str], **extra_args) -> BaseEnvironmentContext:
        pass

    @staticmethod
    def validate(iac_context: BaseEnvironmentContext):
        pass
