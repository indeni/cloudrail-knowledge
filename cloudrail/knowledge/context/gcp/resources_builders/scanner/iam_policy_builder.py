from typing import List
from cloudrail.knowledge.context.gcp.resources.iam.iam_access_policy import IamAccessPolicy, GcpIamPolicyBinding, GcpIamPolicyCondition
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket_iam_policy import GcpStorageBucketIamPolicy
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class StorageBucketIamPolicyBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'storage-v1-buckets-getIamPolicy.json'

    def do_build(self, attributes: dict) -> GcpStorageBucketIamPolicy:
        iam_policy: IamAccessPolicy = _build_iam_policy(attributes, attributes['resourceId'].split('/')[-1])
        return GcpStorageBucketIamPolicy(iam_policy.resource_name, iam_policy.bindings)

def _build_iam_policy(attributes: dict, resource_name: str) -> IamAccessPolicy:
    bindings: List[GcpIamPolicyBinding] = []
    for binding in attributes['bindings']:
        condition = None
        if condition_data := binding.get('condition'):
            condition = GcpIamPolicyCondition(expression=condition_data['expression'],
                                              title=condition_data['title'],
                                              description=condition_data.get('description'))
        bindings.append(GcpIamPolicyBinding(members=binding['members'],
                                             role=binding['role'],
                                             condition=condition))
    return IamAccessPolicy(resource_name=resource_name,
                           bindings=bindings)
