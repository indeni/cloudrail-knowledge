from typing import Dict
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_base_iam_builder import CloudformationBaseIamBuilder
from cloudrail.knowledge.context.aws.resources.iam.iam_instance_profile import IamInstanceProfile


class CloudformationIamInstanceProfileBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_INSTANCE_PROFILE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> IamInstanceProfile:
        res_properties: dict = cfn_res_attr['Properties']
        instance_profile_name = self.get_property(res_properties, 'InstanceProfileName', self.get_resource_id(cfn_res_attr))
        role_names = self.get_property(res_properties, 'Roles')
        return IamInstanceProfile(iam_instance_profile_name=instance_profile_name,
                                  account=cfn_res_attr['account_id'],
                                  region=cfn_res_attr['region'],
                                  role_name=role_names[0] if role_names else None)
