from typing import Dict
from cloudrail.knowledge.context.aws.resources.codebuild.codebuild_project import CodeBuildProject
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn

class CloudformationCodeBuildProjectBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CODEBUILD_PROJECT, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> CodeBuildProject:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        region = cfn_res_attr['region']
        project_name = self.get_property(properties, 'Name', self.get_resource_id(cfn_res_attr))
        encryption_key = self.get_encryption_key_arn(self.get_property(properties, 'EncryptionKey'), account, region, CodeBuildProject)
        arn = build_arn('codebuild', region, account, 'project', None, project_name)
        vpc_config: NetworkConfiguration = None
        if vpc_config_data := self.get_property(properties, 'VpcConfig'):
            vpc_config = NetworkConfiguration(assign_public_ip=False,
                                              security_groups_ids=self.get_property(vpc_config_data, 'SecurityGroupIds', []),
                                              subnet_list_ids=self.get_property(vpc_config_data, 'Subnets', []))
        return CodeBuildProject(account=account,
                                region=region,
                                project_name=project_name,
                                encryption_key=encryption_key,
                                arn=arn,
                                vpc_config=vpc_config)
