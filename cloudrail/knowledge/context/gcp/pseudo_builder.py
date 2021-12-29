import os
from typing import List, Optional

from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources_builders.scanner.compute_firewall_builder import ComputeFirewallBuilder
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket_iam_policy import GcpStorageBucketIamPolicy
from cloudrail.knowledge.context.gcp.resources_builders.scanner.iam_policy_builder import StorageBucketIamPolicyBuilder
from cloudrail.knowledge.context.mergeable import EntityOrigin
from cloudrail.knowledge.utils.file_utils import file_to_json


class PseudoBuilder:
    def __init__(self, merged_ctx: GcpEnvironmentContext):
        self.ctx = merged_ctx

    def create_default_firewalls(self):
        if len(self.ctx.compute_firewalls) > 0 \
            and not any(firewall.origin == EntityOrigin.LIVE_ENV for firewall in self.ctx.compute_firewalls):
            firewalls = self._get_firewalls_from_file('default_firewalls.json')
            project_id = self.ctx.compute_firewalls[0].project_id
            for firewall in firewalls:
                firewall.network.replace('dev-for-tests', project_id)
            self.ctx.compute_firewalls.extend(firewalls)

    def get_implied_firewalls(self):
        firewalls = self._get_firewalls_from_file('implied_firewalls.json')
        for firewall in firewalls:
            firewall.is_implied_rule = True
        return firewalls

    @staticmethod
    def _get_firewalls_from_file(file_name: str) -> List[GcpComputeFirewall]:
        current_path = os.path.dirname(os.path.abspath(__file__))
        firewalls = file_to_json(os.path.join(current_path, 'pseudo_docs', file_name))
        firewalls_list: Optional[List[GcpComputeFirewall]] = [ComputeFirewallBuilder.do_build(ComputeFirewallBuilder, firewall)
                                                              for firewall in firewalls['value']]
        return firewalls_list

    @staticmethod
    def create_default_storage_bucket_iam_policy(project_id: str) -> GcpStorageBucketIamPolicy:
        current_path = os.path.dirname(os.path.abspath(__file__))
        raw_data_policy = file_to_json(os.path.join(current_path, 'pseudo_docs', 'default_storage_bucket_iam_policies.json'))
        policy: GcpStorageBucketIamPolicy = StorageBucketIamPolicyBuilder.do_build(StorageBucketIamPolicyBuilder, raw_data_policy['value'][0])
        policy.is_default = True
        policy.is_pseudo = True
        for binding in policy.bindings:
            for member in binding.members:
                member.replace('dev-for-tests', project_id)
        return policy
