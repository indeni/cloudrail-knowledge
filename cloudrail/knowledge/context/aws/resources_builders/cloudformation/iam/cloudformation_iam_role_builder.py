from typing import Dict
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.iam.cloudformation_base_iam_builder import CloudformationBaseIamBuilder
from cloudrail.knowledge.context.aws.resources.iam.role import Role


class CloudformationIamRoleBuilder(CloudformationBaseIamBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.IAM_ROLE, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> Role:
        res_properties: dict = cfn_res_attr['Properties']
        role_name: str = self._get_role_name(cfn_res_attr)
        qualified_arn: str = self._get_role_arn(cfn_res_attr)
        return Role(account=cfn_res_attr['account_id'],
                    qualified_arn=qualified_arn,
                    role_name=role_name,
                    role_id=self.create_random_pseudo_identifier(),
                    permission_boundary_arn=self.get_property(res_properties, 'PermissionsBoundary'),
                    creation_date=None)
