from typing import Dict, Optional
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentityType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_base_iam_builder import CloudformationBaseIamBuilder
from cloudrail.knowledge.context.aws.resources.iam.iam_users_login_profile import IamUsersLoginProfile


class CloudformationIamUsersLoginProfileBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_USER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Optional[IamUsersLoginProfile]:
        res_properties: dict = cfn_res_attr['Properties']
        if 'LoginProfile' in res_properties:
            iam_user_name: str = self._get_identity_name(cfn_res_attr, IamIdentityType.USER)
            return IamUsersLoginProfile(account=cfn_res_attr['account_id'],
                                        name=iam_user_name)
        return None
