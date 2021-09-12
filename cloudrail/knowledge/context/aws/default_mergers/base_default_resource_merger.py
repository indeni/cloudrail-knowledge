from abc import abstractmethod
from typing import List, TypeVar, Iterable

from cloudrail.knowledge.context.mergeable import Mergeable

from cloudrail.knowledge.exceptions import TerraformApplyExpectedToFail

_TMergeable = TypeVar('_TMergeable', bound=Mergeable)


class BaseDefaultResourceMerger:

    def merge(self, existing_entities: Iterable[_TMergeable], new_entities: Iterable[_TMergeable], must_exist: bool, *args) -> List[_TMergeable]:
        affected_entities = []

        for new_entity in new_entities:

            existing_entity = next((existing_entity for existing_entity in existing_entities
                                    if self._merge_condition(existing_entity, new_entity, *args)), None)
            if not existing_entity:
                if not must_exist:
                    continue
                raise TerraformApplyExpectedToFail(f'Could not find an existing default {self.resource_type} '
                                                   f'that is described by {new_entity.iac_state.resource_metadata.file_name}. ')

            existing_entity.with_aliases(*new_entity.aliases)
            existing_entity.iac_state = new_entity.iac_state
            affected_entities.append(existing_entity)
            self._assign_data(existing_entity, new_entity)

        return affected_entities

    @abstractmethod
    def _merge_condition(self, existing_entity: _TMergeable, new_entity: _TMergeable, *args) -> bool:
        pass

    @property
    @abstractmethod
    def resource_type(self) -> str:
        pass

    # pylint: disable=no-self-use
    def _assign_data(self, existing_entity: _TMergeable, new_entity: _TMergeable) -> None:
        existing_entity.tags.update(new_entity.tags)
