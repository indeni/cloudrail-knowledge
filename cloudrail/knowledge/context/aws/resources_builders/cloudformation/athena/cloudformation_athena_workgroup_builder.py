from typing import Dict
from cloudrail.knowledge.context.aws.resources.athena.athena_workgroup import AthenaWorkgroup
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import is_valid_arn


class CloudformationAthenaWorkgroupBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.ATHENA_WORKGROUP, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> AthenaWorkgroup:
        properties: dict = cfn_res_attr['Properties']
        workgroup_configuration = properties.get('WorkGroupConfiguration', {})
        result_configuration = workgroup_configuration.get('ResultConfiguration', {})
        encryption_config = result_configuration.get('EncryptionConfiguration', {})
        encryption_option = self.get_property(encryption_config, 'EncryptionOption')
        kms_key_id: str = self.get_property(encryption_config, 'KmsKey')
        if is_valid_arn(kms_key_id):
            kms_key_id = kms_key_id.split('/')[1]

        return AthenaWorkgroup(self.get_property(properties, 'Name'),
                               self.get_property(properties, 'State', 'ENABLED'),
                               bool(encryption_config),
                               self.get_property(workgroup_configuration, 'EnforceWorkGroupConfiguration', False),
                               encryption_option,
                               kms_key_id,
                               cfn_res_attr['region'],
                               cfn_res_attr['account_id'])
