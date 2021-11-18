from typing import Dict
from cloudrail.knowledge.context.aws.resources.kms.kms_alias import KmsAlias
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationKmsAliasBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.KMS_KEY_ALIAS, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> KmsAlias:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        alias_name = self.get_property(properties, 'AliasName')
        alias_arn = f'arn:aws:kms:{region}:{account}:{alias_name}'
        target_key_id = self.get_property(properties, 'TargetKeyId')
        return KmsAlias(alias_name=alias_name,
                        alias_arn=alias_arn,
                        target_key_id=target_key_id,
                        account=account,
                        region=region)
