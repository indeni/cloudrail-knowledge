# pylint: disable=no-member
import re
from abc import abstractmethod
from enum import Enum
from typing import List, Set, Optional, FrozenSet

from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.exceptions import UnsupportedIacTypeException


class EntityOrigin(str, Enum):
    LIVE_ENV = 'live_environment'
    TERRAFORM = 'terraform'
    PSEUDO = 'pseudo'
    CLOUDFORMATION = 'cloudformation'


class Mergeable:

    def __init__(self):
        self._aliases: Set[str] = set()
        self.iac_state: Optional[IacState] = None
        self.is_pseudo = False
        self.invalidation: Set[str] = set()
        self.tags = None

    def with_aliases(self, *aliases: str):
        self._aliases.update(filter(None, aliases))
        return self

    @property
    def aliases(self) -> FrozenSet[str]:
        return frozenset(self._aliases)

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

    def get_name(self) -> Optional[str]:
        if hasattr(self, 'name'):
            return self.name
        return None

    def get_id(self) -> str:
        pass

    def get_arn(self) -> Optional[str]:
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
        if not self.is_new_resource() and not self.is_pseudo:
            return self.get_cloud_resource_url()
        return None

    def get_existing_cloud_entity_id(self) -> Optional[str]:
        if not self.is_new_resource() and not self.is_pseudo:
            return self.get_id()
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
            if self.iac_state.iac_type == IacType.TERRAFORM:
                return EntityOrigin.TERRAFORM
            elif self.iac_state.iac_type == IacType.CLOUDFORMATION:
                return EntityOrigin.CLOUDFORMATION
            else:
                raise UnsupportedIacTypeException()
        else:
            return EntityOrigin.LIVE_ENV

    @property
    def is_managed_by_iac(self) -> bool:
        return bool(self.iac_state)

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

    @abstractmethod
    def to_drift_detection_object(self) -> dict:
        pass
