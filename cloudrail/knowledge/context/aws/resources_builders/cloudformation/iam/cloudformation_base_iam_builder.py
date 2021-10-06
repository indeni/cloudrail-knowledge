from abc import abstractmethod
from typing import Union, List
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationBaseIamBuilder(BaseCloudformationBuilder):

    @abstractmethod
    def parse_resource(self, cfn_res_attr: dict) -> Union[AwsResource, List[AwsResource]]:
        pass

    def _get_role_arn(self, cfn_res_attr: dict) -> str:
        return build_arn('iam', None, cfn_res_attr['account_id'], 'role', self.get_property(cfn_res_attr['Properties'], 'Path'),
                         self._get_role_name(cfn_res_attr))

    def _get_role_name(self, cfn_res_attr: dict) -> str:
        res_properties: dict = cfn_res_attr['Properties']
        return self.get_property(res_properties, 'RoleName', self.get_resource_id(cfn_res_attr))
