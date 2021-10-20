import inspect
from typing import TypeVar, Type

from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.iac_state import IacState


_T = TypeVar('_T')


def create_empty_entity(class_type: Type[_T], **kwargs) -> _T:
    """
    A test auxiliary function that creates a new instance of type `class_type` and initializes it with the values of kwargs or None
    Args:
        class_type: The instance's `class_type` to create.
        **kwargs: The parameters that will be passed to the instance's __init__ method.

    Returns:
        An instance of type `class_type`, initialized with the parameters in `kwargs`.
    """
    signature = inspect.signature(class_type.__init__)
    params = {}
    for param in list(signature.parameters)[1:]:
        params[param] = None
    params.update(kwargs)
    resource = class_type(**params)
    if isinstance(resource, Mergeable):
        add_terraform_state(resource, resource.__class__.__name__, True)
    return resource


def add_terraform_state(resource: Mergeable, friendly_name: str, as_new_resource: bool = True):
    action_type = IacActionType.CREATE if as_new_resource else IacActionType.UPDATE
    resource.iac_state = IacState(friendly_name, action_type, None, as_new_resource)
