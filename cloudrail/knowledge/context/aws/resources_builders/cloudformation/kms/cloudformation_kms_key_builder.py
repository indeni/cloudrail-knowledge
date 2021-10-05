from typing import Dict
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationKmsKeyBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.KMS_KEY, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> KmsKey:
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        key_id = self.get_resource_id(cfn_res_attr)
        return KmsKey(key_id=key_id,
                      arn=build_arn('kms', region, account, 'key', None, key_id),
                      key_manager=KeyManager.CUSTOMER,
                      region=region,
                      account=account)
