import datetime
from typing import Dict
from cloudrail.knowledge.context.aws.resources.kms.kms_key_policy import KmsKeyPolicy
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.environment_context.common_component_builder import build_policy_statement


class CloudformationKmsKeyPolicyBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.KMS_KEY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> KmsKeyPolicy:
        properties: dict = cfn_res_attr['Properties']
        account = cfn_res_attr['account_id']
        key_id = self.get_resource_id(cfn_res_attr)
        kms_policy: dict = self.get_property(properties, 'KeyPolicy')
        if kms_policy and isinstance(kms_policy.get('Version'), datetime.date):
            policy_date: datetime.date = kms_policy['Version']
            kms_policy['Version'] = f'{policy_date.year}-{policy_date.month}-{policy_date.day}'
        return KmsKeyPolicy(account=account,
                            key_id=key_id,
                            policy_statements=[build_policy_statement(statement) for statement in kms_policy.get('Statement', [])] if kms_policy else [],
                            raw_document=kms_policy)
