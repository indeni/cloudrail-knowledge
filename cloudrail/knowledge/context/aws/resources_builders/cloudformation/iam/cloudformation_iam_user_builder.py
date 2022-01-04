from typing import Dict
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentityType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_base_iam_builder import CloudformationBaseIamBuilder
from cloudrail.knowledge.context.aws.resources.iam.iam_user import IamUser


class CloudformationIamUserBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_USER, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> IamUser:
        res_properties: dict = cfn_res_attr['Properties']
        iam_user_name: str = self._get_identity_name(cfn_res_attr, IamIdentityType.USER)
        qualified_arn: str = self._get_identity_arn(cfn_res_attr, IamIdentityType.USER)
        return IamUser(account=cfn_res_attr['account_id'],
                       name=iam_user_name,
                       user_id=self.get_resource_id(cfn_res_attr),
                       qualified_arn=qualified_arn,
                       permission_boundary_arn=self.get_property(res_properties, 'PermissionsBoundary'),
                       arn=qualified_arn)
