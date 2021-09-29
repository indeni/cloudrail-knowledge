from dataclasses import dataclass, field
from typing import Dict, List
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType


@dataclass
class CloudformationTransformContext:
    logical_to_physical_id_map: dict = field(default_factory=dict)
    cfn_template_params: dict = field(default_factory=dict)
    cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, dict]] = field(default_factory=dict)
    cfn_resources_by_type_map: Dict[CloudformationResourceType, AliasesDict[Mergeable]] = field(default_factory=dict)
    cfn_template_dict: dict = field(default_factory=dict)
    references_map: dict = field(default_factory=dict)
    cfn_resources_map: Dict[str, dict] = field(default_factory=dict)
    availability_zones: Dict[str, List[str]] = field(default_factory=dict)
