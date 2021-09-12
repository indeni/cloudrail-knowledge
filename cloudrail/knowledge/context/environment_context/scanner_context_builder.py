from abc import abstractmethod
from typing import Optional

from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext


class ScannerContextBuilder:

    @staticmethod
    @abstractmethod
    def build(account_data_dir: Optional[str], account_id: Optional[str], salt: Optional[str], **extra_args) -> BaseEnvironmentContext:
        pass
