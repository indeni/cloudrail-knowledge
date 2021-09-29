from dataclasses import dataclass
from typing import Optional, List

from dataclasses_json import DataClassJsonMixin


@dataclass
class Drift(DataClassJsonMixin):
    resource_type: str
    resource_id: str
    resource_iac: dict
    resource_live: dict
    resource_metadata: Optional[dict] = None
    hint: Optional[str] = None
    cloud_resource_url: Optional[str] = None
    iac_resource_url: Optional[str] = None
    cloud_entity_id: Optional[str] = None


@dataclass
class DriftDetectionResult:
    drifts: List[Drift]
    iac_coverage: int
    workspace_id: str
