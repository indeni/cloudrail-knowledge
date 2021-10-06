import functools
import logging
from typing import List, Union, Iterable, Callable, Optional, Dict, TypeVar, Set

from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.aws.resources.networking_config.network_resource import NetworkResource
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.exceptions import ResourceDependencyNotFoundException, UnsupportedResourceCollectionTypeException


class ResourceInvalidator:

    def __init__(self, ctx: BaseEnvironmentContext):
        self.env_context: BaseEnvironmentContext = ctx
        self.all_visited_nodes: Set[Mergeable] = set()
        self._direct_dependency_invalidation_reason_format = 'This resource depends on {} which is an invalid resource'

    def remove_invalid_resources(self) -> None:
        try:
            self._invalidate_resources()

            for invalidated_resources in self.env_context.invalidated_resources:
                for reason in invalidated_resources.invalidation:
                    logging.warning(f'{invalidated_resources.get_friendly_name()} is invalidated because: {reason}')

            for attribute_name, attribute in vars(self.env_context).items():
                if attribute is self.env_context.invalidated_resources:
                    continue
                if attribute and isinstance(attribute, AliasesDict) and isinstance(next(iter(attribute)), Mergeable):
                    new_attribute = AliasesDict(*(x for x in attribute if not x.is_invalidated))
                    setattr(self.env_context, attribute_name, new_attribute)
                elif attribute and isinstance(attribute, list) and isinstance(next(iter(attribute)), Mergeable):
                    new_attribute = [x for x in attribute if not x.is_invalidated]
                    setattr(self.env_context, attribute_name, new_attribute)
        finally:
            self._mergeable_attributes.cache_clear()

    def _invalidate_resources(self) -> None:
        visited_nodes = []
        for attribute in vars(self.env_context).values():
            if attribute and isinstance(attribute, (AliasesDict, list)):
                if isinstance(next(iter(attribute)), Mergeable):
                    for item in attribute:
                        self._cascading_invalidations(item, visited_nodes)

    def _set_direct_dependency_invalidations(self, resource: Union[Mergeable, List[Mergeable]]) -> bool:
        invalidation_set = False
        for dependency in self._mergeable_attributes(resource):
            if dependency.is_invalidated:
                resource.add_invalidation(self._direct_dependency_invalidation_reason_format.format(dependency.get_friendly_name()))
                invalidation_set = True

        return invalidation_set

    def _cascading_invalidations(self, resource: Union[Mergeable, List[Mergeable]], branch_visited_nodes: List[Mergeable]):
        if isinstance(resource, list):
            for item in resource:
                self._cascading_invalidations(item, branch_visited_nodes)
            return

        # custom_invalidation is used for resources that wants to have extra logic for invalidation.
        # for example, a resource with attribute 'X: int' wants to be considered as invalid if X > 5.
        resource.invalidation.update(resource.custom_invalidation())

        if resource.is_invalidated:
            self.env_context.invalidated_resources.add(resource)
            self._set_invalidations(branch_visited_nodes)
            return

        branch_visited_nodes.append(resource)
        if self._set_direct_dependency_invalidations(resource):
            self._set_invalidations(branch_visited_nodes)
            branch_visited_nodes.remove(resource)
            return

        if resource in self.all_visited_nodes:
            branch_visited_nodes.remove(resource)
            return  # Means we already went over this resource, so no point in checking its dependencies again
        self.all_visited_nodes.add(resource)

        # resource is not invalid. Cascading down through all its dependencies until an invalid dependency is found
        for dependency in self._mergeable_attributes(resource):
            if dependency not in branch_visited_nodes:
                self._cascading_invalidations(dependency, branch_visited_nodes)

            if dependency.is_invalidated:
                break

        branch_visited_nodes.remove(resource)

    def _set_invalidations(self, nodes_to_invalidate):
        if nodes_to_invalidate:
            last = nodes_to_invalidate[-1]
            self.env_context.invalidated_resources.add(last)
            for before_last in reversed(nodes_to_invalidate[:-1]):
                before_last.add_invalidation(self._direct_dependency_invalidation_reason_format.format(last.get_friendly_name()))
                self.env_context.invalidated_resources.add(before_last)
                last = before_last

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _mergeable_attributes(mergeable):
        mergeable_attributes = []
        excluded_attributes = list(filter(None, mergeable.exclude_from_invalidation()))
        for attribute in vars(mergeable).values():
            if attribute in excluded_attributes:
                continue
            if isinstance(attribute, Mergeable):
                mergeable_attributes.append(attribute)
            elif isinstance(attribute, NetworkResource):
                mergeable_attributes.extend(attribute.network_interfaces)
            else:
                try:
                    iterable = iter(attribute)
                    if attribute and isinstance(next(iterable), Mergeable):
                        mergeable_attributes.extend(attribute)
                except TypeError:
                    pass

        return mergeable_attributes

    _TMergeable = TypeVar('_TMergeable', bound=Mergeable)
    _T = TypeVar('_T')

    @classmethod
    def get_by_id(cls,
                  resources: Union[AliasesDict[_TMergeable], Iterable, Dict[str, _TMergeable]],
                  resource_id: str,
                  invalidate_if_not_found: bool,
                  resource_to_invalidate: Optional[Mergeable] = None,
                  case_sensitive: bool = True) -> Optional[_TMergeable]:
        def logic():
            if isinstance(resources, (AliasesDict, dict)):
                resource = resources.get(resource_id)
                if resource or case_sensitive:
                    return resource

            return cls._get_by_iterable_logic(resources, resource_id, case_sensitive)

        return ResourceInvalidator.get_by_logic(logic, invalidate_if_not_found, resource_to_invalidate,
                                                f'Resource with id: {resource_id} was not found')

    @staticmethod
    def _get_by_iterable_logic(resources: Union[AliasesDict[_TMergeable], Iterable, Dict[str, _TMergeable]],
                               resource_id: str,
                               case_sensitive: bool) -> Optional[_TMergeable]:
        try:
            if case_sensitive:
                return next((resource for resource in resources
                             if resource_id == resource.get_id() or resource_id in resource.aliases), None)
            else:
                return next((resource for resource in resources
                             if resource_id.lower() == resource.get_id().lower()
                             or any(resource_id.lower() == alias.lower() for alias in resource.aliases)), None)
        except TypeError:
            raise UnsupportedResourceCollectionTypeException(f'The collection of type {type(resources).__name__} is not iterable.')

    @staticmethod
    def get_by_logic(logic: Callable[[], Union[_T, Iterable[_T]]],
                     invalidate_if_not_found: bool,
                     resource_to_invalidate: Optional[Mergeable] = None,
                     invalidation_reason: Optional[str] = None) -> Union[_T, Iterable[_T]]:

        if invalidate_if_not_found and not resource_to_invalidate:
            raise ValueError('Must provide resource to invalidate')
        if invalidate_if_not_found and not invalidation_reason:
            raise ValueError('Must provide invalidation reason')

        try:
            found_resource = logic()
        except UnsupportedResourceCollectionTypeException:
            raise
        except Exception as ex:
            logging.warning('An exception occurred while attempting to get a resource:')
            logging.warning(str(ex))
            found_resource = None

        if invalidate_if_not_found:
            ResourceInvalidator._assert_relation(resource_to_invalidate, found_resource, invalidation_reason)

        return found_resource

    @staticmethod
    def _assert_relation(resource: Mergeable, resource_dependency: any, reason: str):
        if resource_dependency is None or ResourceInvalidator._is_zero_length(resource_dependency):
            resource.add_invalidation(reason)
            raise ResourceDependencyNotFoundException()

    @staticmethod
    def _is_zero_length(obj):
        try:
            return len(obj) == 0
        except Exception:
            return False
