from typing import List, Dict, Optional

from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.iac_action_type import IacActionType


# pylint: disable=unsupported-membership-test,unsupported-assignment-operation
class TerraformResourceFinder:
    _tf_path_to_resource: Dict[str, List[Mergeable]] = None

    @classmethod
    def add_resource(cls, resource: Mergeable):
        if cls._tf_path_to_resource is None:
            raise Exception('can not add_resource, you should initialize before adding resources')
        if resource.iac_state:
            state = resource.iac_state
            if state.action not in [IacActionType.CREATE, IacActionType.READ, IacActionType.NO_OP]:
                return
            if state.resource_metadata:
                metadata = state.resource_metadata
                key = cls._get_key(metadata.file_name, metadata.start_line, metadata.end_line)
                if not key:
                    return
                if key not in cls._tf_path_to_resource:
                    cls._tf_path_to_resource[key] = []
                cls._tf_path_to_resource[key].append(resource)

    @staticmethod
    def _get_key(file_name: str, start_line: int, end_line: int) -> Optional[str]:
        if not file_name:
            return None
        return '{}::{}::{}'.format(file_name, start_line, end_line)

    @classmethod
    def get_resources(cls, file_name: str, start_line: int, end_line: int):
        if cls._tf_path_to_resource is None:
            raise Exception('can not get_resources, you should initialize before using class')
        key = cls._get_key(file_name, start_line, end_line)
        return cls._tf_path_to_resource.get(key, [])

    @classmethod
    def destroy(cls):
        cls._tf_path_to_resource = None

    @classmethod
    def initialize(cls):
        cls._tf_path_to_resource = {}
