from dataclasses import dataclass
from typing import Optional

from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.iac_resource_metadata import IacResourceMetadata


@dataclass
class IacState:
    address: str
    action: TerraformActionType
    resource_metadata: Optional[IacResourceMetadata]
    is_new: bool
    iac_resource_url: Optional[str] = None
