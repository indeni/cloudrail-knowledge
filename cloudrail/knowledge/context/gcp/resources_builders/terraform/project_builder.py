from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.projects.gcp_project import Project
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder


class ProjectBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> Project:
        return Project(attributes['name'],
                       self._get_known_value(attributes, 'number'),
                       attributes['project_id'])

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_PROJECT
