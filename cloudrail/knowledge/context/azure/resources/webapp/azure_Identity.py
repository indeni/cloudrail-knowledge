from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Identity:
    """
        Attributes:
            type: identity type of the Function App.
            identity_ids: list of user managed identity ids.
    """
    type: str
    identity_ids: Optional[List[str]]
