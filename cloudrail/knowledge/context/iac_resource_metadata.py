import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class IacResourceMetadata:
    iac_entity_id: str
    file_name: str
    start_line: int
    end_line: int
    module_metadata: Optional['IacResourceMetadata'] = None
    id: Optional[str] = None
    resource_type: Optional[str] = None
    run_execution_id: str = None

    def __post_init__(self):
        self.id = self.id or str(uuid.uuid4())

    def get_iac_resource_url(self, iac_url_template: Optional[str]) -> Optional[str]:
        if iac_url_template and self.file_name:
            return iac_url_template \
                .replace('{iac_file_path}', self.file_name) \
                .replace('{iac_file_line_no}', str(self.start_line))
        return None
