from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_ssl_policy import GcpComputeSslPolicy
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder


class ComputeSslPolicyBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeSslPolicy:
        name = attributes["name"]
        policy_id = attributes["id"]
        self_link = attributes["self_link"]
        min_tls_version = self._get_known_value(attributes, "min_tls_version", "TLS_1_0")
        profile = self._get_known_value(attributes, "profile", "COMPATIBLE")
        custom_features = self._get_known_value(attributes, "custom_features")

        return GcpComputeSslPolicy(name, policy_id, self_link, min_tls_version, profile, custom_features)

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_SSL_POLICY
