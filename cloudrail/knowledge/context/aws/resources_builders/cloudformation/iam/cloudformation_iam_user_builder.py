from typing import Dict
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_base_iam_builder import CloudformationBaseIamBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationIamUserBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_USER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> IamUser:
        properties = cfn_res_attr['Properties']
        name = self.get_property(properties, "UserName")
        account = cfn_res_attr['account_id']
        user_id = self.get_resource_id(cfn_res_attr)
        qualified_arn = build_arn('iam', None, account, 'user', self.get_property(cfn_res_attr, "Path", "/"), name)
        permission_boundary_arn = self.get_property(properties, 'PermissionsBoundary')
        return IamUser(account=account,
                       name=name,
                       user_id=user_id + "unique_id",
                       qualified_arn=qualified_arn,
                       permission_boundary_arn=permission_boundary_arn,
                       arn=user_id + "arn")
