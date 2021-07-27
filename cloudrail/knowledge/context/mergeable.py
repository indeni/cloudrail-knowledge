# pylint: disable=no-member
import re
from abc import abstractmethod
from enum import Enum
from typing import List, Set, Dict, Optional

from cloudrail.knowledge.context.iac_state import IacState


class EntityOrigin(str, Enum):
    LIVE_ENV = 'live_environment'
    TERRAFORM = 'terraform'
    PSEUDO = 'pseudo'


class Mergeable:

    def __init__(self):
        self.aliases: Set[str] = set()
        self.iac_state: Optional[IacState] = None
        self.is_pseudo = False
        self.tags: Dict[str, str] = {}
        self.invalidation: Set[str] = set()

    def with_aliases(self, *aliases: str):
        self.aliases.update(aliases)
        return self

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    def get_type(self, is_plural: bool = False) -> str:
        class_type = type(self).__name__
        words = re.findall('[A-Z][^A-Z]*', class_type)
        if not is_plural:
            return ' '.join(words)
        else:
            return ' '.join(words) + 's'

    def get_name(self) -> str:
        if hasattr(self, 'name'):
            return self.name
        return None

    def get_id(self) -> str:
        pass

    def get_arn(self) -> str:
        if hasattr(self, 'arn'):
            return self.arn
        return None

    def get_extra_data(self) -> str:
        pass

    @abstractmethod
    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def is_new_resource(self) -> bool:
        return self.iac_state is not None and self.iac_state.is_new

    def get_existing_cloud_resource_url(self) -> Optional[str]:
        if not self.is_new_resource():
            return self.get_cloud_resource_url()
        return None

    def add_invalidation(self, reason: str) -> None:
        self.invalidation.add(reason)

    @property
    def is_invalidated(self) -> bool:
        return bool(self.invalidation)

    @abstractmethod
    def get_friendly_name(self) -> str:
        pass

    @property
    def origin(self) -> EntityOrigin:
        if self.is_pseudo:
            return EntityOrigin.PSEUDO
        elif self.iac_state:
            return EntityOrigin.TERRAFORM
        else:
            return EntityOrigin.LIVE_ENV

    @property
    def is_managed_by_iac(self) -> bool:
        return self.origin == EntityOrigin.TERRAFORM

    @property
    @abstractmethod
    def is_tagable(self) -> bool:
        pass

    # pylint: disable=no-self-use
    def exclude_from_invalidation(self):
        """
        A list of attributes that should be excluded from the invalidation process
        """
        return []

    def custom_invalidation(self) -> List[str]:
        """
        A list of manual reasons why this resource should be invalidated
        """
        return []

    @staticmethod
    def is_standalone() -> bool:
        return True
