from abc import abstractmethod
from typing import Dict

from cloudrail.knowledge.rules.base_rule import BaseRule


class AbstractRulesLoader:

    @abstractmethod
    def load(self) -> Dict[str, BaseRule]:
        pass
