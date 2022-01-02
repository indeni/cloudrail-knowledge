from typing import List, Dict, Optional
from cloudrail.knowledge.context.gcp.resources.iam.iam_access_policy import IamAccessPolicy, GcpIamPolicyBinding
from cloudrail.knowledge.utils.utils import flat_list

class IamActions:

    @classmethod
    def merge_iam_policies(cls, iam_policies: List[IamAccessPolicy]) -> List[IamAccessPolicy]:
        updated_iam_policies: List[IamAccessPolicy] = []
        policies_by_name: Dict[str, List[GcpIamPolicyBinding]] = {}
        for policy in iam_policies:
            if policy.resource_name not in policies_by_name:
                policies_by_name[policy.resource_name] = policy.bindings
            else:
                policies_by_name[policy.resource_name].extend(policy.bindings)
        for key, value in policies_by_name.items():
            policies_by_name[key] = cls.merge_bindings(value)
        for policy in iam_policies:
            if policy.resource_name in policies_by_name and not any(policy.resource_name == updated_policy.resource_name
                                                                    for updated_policy in updated_iam_policies):
                policy.bindings = policies_by_name[policy.resource_name]
                updated_iam_policies.append(policy)
        return updated_iam_policies

    @staticmethod
    def merge_bindings(bindings: List[GcpIamPolicyBinding]) -> List[Optional[GcpIamPolicyBinding]]:
        merged_bindings = [binding for binding in bindings if binding.condition]
        roles = {binding.role for binding in bindings if not binding.condition}
        role_members_map = {}
        for role in roles:
            role_members = flat_list([binding.members for binding in bindings if role == binding.role])
            role_members_map[role] = role_members
        for key, value in role_members_map.items():
            merged_bindings.append(GcpIamPolicyBinding(role=key, members=value, condition=None))
        return merged_bindings
