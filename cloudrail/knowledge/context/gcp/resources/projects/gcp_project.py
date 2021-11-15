from typing import List, Optional

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class Project(GcpResource):
    """
        Attributes:
            project_name: The name of the project.
            project_number: The project number.
            gcp_project_id: The project ID.
    """
    def __init__(self,
                 project_name: Optional[str],
                 project_number: Optional[int],
                 gcp_project_id: str):

        super().__init__(GcpResourceType.GOOGLE_PROJECT)
        self.project_name: Optional[str] = project_name
        self.project_number: Optional[int] = project_number
        self.gcp_project_id: str = gcp_project_id
        self.with_aliases(self.gcp_project_id)

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_id(self) -> str:
        return self.gcp_project_id

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}iam-admin/settings?project={self.gcp_project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Google Project'
        else:
            return 'Google Projects'

    @property
    def is_labeled(self) -> bool:
        return True

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'labels': self.labels}
