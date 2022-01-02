from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_http_proxy import GcpComputeTargetHttpProxy
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class ComputeTargetHttpProxyBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeTargetHttpProxy:
        return GcpComputeTargetHttpProxy(name=attributes['name'],
                                         target_id=attributes["id"],
                                         self_link=attributes["self_link"],
                                         url_map=attributes['url_map'])

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_TARGET_HTTP_PROXY
