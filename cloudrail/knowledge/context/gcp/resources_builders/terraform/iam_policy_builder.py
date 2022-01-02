import json
from typing import Callable, List, Optional
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket_iam_policy import GcpStorageBucketIamPolicy
from cloudrail.knowledge.context.gcp.resources.iam.iam_access_policy import GcpIamPolicyCondition, GcpIamPolicyType, IamAccessPolicy, GcpIamPolicyBinding
from cloudrail.knowledge.exceptions import UnknownResultOfTerraformApply
from cloudrail.knowledge.utils.utils import flat_list, is_iterable_with_values
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder

class IamPolicyBuilder:

    def build_iam_policy(self, attributes: dict, resource_name: str, policy_type: GcpIamPolicyType, get_known_value_func: Callable) -> IamAccessPolicy:
        bindings: List[GcpIamPolicyBinding] = []
        if policy_type == GcpIamPolicyType.AUTHORITATIVE:
            bindings_data = json.loads(attributes['policy_data'])['bindings']
            for binding in bindings_data:
                condition = self._get_condition_data(binding, get_known_value_func)
                bindings.append(GcpIamPolicyBinding(members=binding['members'],
                                                     role=binding['role'],
                                                     condition=condition))
        else:
            raw_member = [get_known_value_func(attributes, 'member')]
            raw_members = get_known_value_func(attributes, 'members')
            members = raw_member if is_iterable_with_values(raw_member) else raw_members
            condition = self._get_condition_data(attributes, get_known_value_func)
            bindings = [GcpIamPolicyBinding(members=members,
                                             role=attributes['role'],
                                             condition=condition)]
        return IamAccessPolicy(resource_name=resource_name,
                               bindings=bindings,
                               policy_type=policy_type)

    @staticmethod
    def _get_condition_data(binding_dict: dict, get_known_value_func: Callable) -> GcpIamPolicyCondition:
        condition = None
        if condition_data := binding_dict.get('condition'):
            condition = GcpIamPolicyCondition(expression=condition_data[0]['expression'],
                                            title=condition_data[0]['title'],
                                            description=get_known_value_func(condition_data[0], 'description'))
        return condition

    @staticmethod
    def validate_iam_policies_config(iam_policies: List[IamAccessPolicy]):
        policies_types = {policy.policy_type for policy in iam_policies}
        if len(policies_types) > 1 and GcpIamPolicyType.AUTHORITATIVE in policies_types:
            raise UnknownResultOfTerraformApply(f'The Terraform content provided uses both "google_*_iam_policy" and'
                                                f' one of the unique policy bindings (google_*_iam_member, google_*_iam_binding),'
                                                f' for the same resource ({iam_policies[0].resource_name}). '
                                                f'This creates an unknown end-result and is not supported by Cloudrail.')


class StorageBucketIamPolicyBuilder(IamPolicyBuilder):

    def get_iam_policies(self, resources: dict) -> Optional[List[GcpStorageBucketIamPolicy]]:
        storage_bucket_iam_authoritative_policies = StorageBucketIamAuthoritativePolicyBuilder(resources).build()
        storage_bucket_iam_binding_policies = StorageBucketIamPolicyBindingBuilder(resources).build()
        storage_bucket_iam_member_policies = StorageBucketIamPolicyMemberBuilder(resources).build()
        storage_bucket_iam_policies = flat_list(storage_bucket_iam_authoritative_policies + storage_bucket_iam_binding_policies + storage_bucket_iam_member_policies)
        self.validate_iam_policies_config(storage_bucket_iam_policies)
        return storage_bucket_iam_policies


class StorageBucketIamAuthoritativePolicyBuilder(BaseGcpTerraformBuilder):

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_STORAGE_BUCKET_IAM_POLICY

    def do_build(self, attributes: dict) -> GcpStorageBucketIamPolicy:
        iam_policy: IamAccessPolicy = IamPolicyBuilder.build_iam_policy(IamPolicyBuilder, attributes, attributes['bucket'].replace('b/', ''),
                                                                        GcpIamPolicyType.AUTHORITATIVE, self._get_known_value)
        return GcpStorageBucketIamPolicy(iam_policy.resource_name, iam_policy.bindings, iam_policy.policy_type)

class StorageBucketIamPolicyBindingBuilder(BaseGcpTerraformBuilder):

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_STORAGE_BUCKET_IAM_BINDING

    def do_build(self, attributes: dict) -> GcpStorageBucketIamPolicy:
        iam_policy: IamAccessPolicy = IamPolicyBuilder.build_iam_policy(IamPolicyBuilder, attributes, attributes['bucket'].replace('b/', ''),
                                                                        GcpIamPolicyType.ROLEAUTHORITATIVE, self._get_known_value)
        return GcpStorageBucketIamPolicy(iam_policy.resource_name, iam_policy.bindings, iam_policy.policy_type)

class StorageBucketIamPolicyMemberBuilder(BaseGcpTerraformBuilder):

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_STORAGE_BUCKET_IAM_MEMBER

    def do_build(self, attributes: dict) -> GcpStorageBucketIamPolicy:
        iam_policy: IamAccessPolicy = IamPolicyBuilder.build_iam_policy(IamPolicyBuilder, attributes, attributes['bucket'].replace('b/', ''),
                                                                        GcpIamPolicyType.NONAUTHORITATIVE, self._get_known_value)
        return GcpStorageBucketIamPolicy(iam_policy.resource_name, iam_policy.bindings, iam_policy.policy_type)
