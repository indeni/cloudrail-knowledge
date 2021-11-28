from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_https_proxy import GcpComputeTargetHttpsProxy
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class ComputeTargetHttpsProxyBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeTargetHttpsProxy:
        return GcpComputeTargetHttpsProxy(name=attributes['name'],
                                          url_map=attributes['url_map'],
                                          ssl_certificates=attributes['ssl_certificates'],
                                          ssl_policy=self._get_known_value(attributes, 'ssl_policy'))

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_TARGET_HTTPS_PROXY
