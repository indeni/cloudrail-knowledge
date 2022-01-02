from cloudrail.knowledge.context.gcp.resources.projects.gcp_project import Project
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ProjectBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'cloudresourcemanager-v1-projects-list.json'

    def do_build(self, attributes: dict) -> Project:
        return Project(attributes.get('name'),
                       attributes['projectNumber'],
                       attributes['projectId'])
