from dataclasses import dataclass
from typing import Optional

from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.iac_resource_metadata import IacResourceMetadata
from cloudrail.knowledge.context.iac_type import IacType


@dataclass
class IacState:
    address: str
    action: IacActionType
    resource_metadata: Optional[IacResourceMetadata]
    is_new: bool
    iac_resource_url: Optional[str] = None
    iac_type: IacType = None
