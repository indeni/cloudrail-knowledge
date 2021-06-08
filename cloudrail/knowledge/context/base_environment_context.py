from dataclasses import dataclass
from typing import Set, List

from cloudrail.knowledge.context.managed_resources_summary import ManagedResourcesSummary

from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.unknown_block import UnknownBlock


class BaseEnvironmentContext:

    def __init__(self, invalidated_resources: Set[Mergeable] = None, unknown_blocks: List[UnknownBlock] = None,
                 managed_resources_summary: ManagedResourcesSummary = None) -> None:
        super().__init__()
        self.invalidated_resources: Set[Mergeable] = invalidated_resources or set()
        self.unknown_blocks: List[UnknownBlock] = unknown_blocks or list()
        self.managed_resources_summary = managed_resources_summary or ManagedResourcesSummary(0, 0, 0, 0)

    def clear_cache(self):
        for attr in dir(self):
            func = getattr(self, attr)
            if callable(func):
                try:
                    func.cache_clear()  # clearing lru_cache
                except Exception:
                    pass


@dataclass
class CheckovResult:
    check_id: str
    file_path: str
    resource: str
    start_line: int
    end_line: int

    @staticmethod
    def from_dict(dic: dict):
        return CheckovResult(dic['check_id'], dic['file_path'], dic['resource'], dic['start_line'], dic['end_line'])
