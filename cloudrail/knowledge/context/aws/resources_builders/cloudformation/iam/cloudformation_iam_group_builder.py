from typing import Dict
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentityType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_base_iam_builder import CloudformationBaseIamBuilder
from cloudrail.knowledge.context.aws.resources.iam.iam_group import IamGroup


class CloudformationIamGroupBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_GROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> IamGroup:
        iam_group_name: str = self._get_identity_name(cfn_res_attr, IamIdentityType.GROUP)
        qualified_arn: str = self._get_identity_arn(cfn_res_attr, IamIdentityType.GROUP)
        return IamGroup(account=cfn_res_attr['account_id'],
                        name=iam_group_name,
                        group_id=self.get_resource_id(cfn_res_attr),
                        qualified_arn=qualified_arn,
                        arn=qualified_arn)
