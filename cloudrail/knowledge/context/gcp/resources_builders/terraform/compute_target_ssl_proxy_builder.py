from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_ssl_proxy import GcpComputeTargetSslProxy
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder


class ComputeTargetSslProxyBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeTargetSslProxy:
        name = attributes["name"]
        target_id = attributes["id"]
        self_link = attributes["self_link"]
        backend_service = attributes["backend_service"]
        ssl_certificates = attributes["ssl_certificates"]
        ssl_policy_identifier = self._get_known_value(attributes, "ssl_policy")
        return GcpComputeTargetSslProxy(name, target_id, self_link, backend_service, ssl_certificates, ssl_policy_identifier)

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_TARGET_SSL_PROXY
