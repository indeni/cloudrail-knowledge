import uuid
from typing import Dict

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.resources.cloudtrail.cloudtrail import CloudTrail


class CloudformationCloudtrailBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CLOUDTRAIL, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> CloudTrail:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        pseudo_name = str(uuid.uuid4())
        name = self.get_property(properties, 'TrailName', f'pseudo_cloudtrail_{pseudo_name}')
        return CloudTrail(name=name,
                          kms_encryption=bool(self.get_property(properties, 'KMSKeyId')),
                          arn=self.get_property(properties, 'Arn', f'arn:aws:cloudtrail:{region}:{account}:trail/{name}'),
                          log_file_validation=self.get_property(properties, 'EnableLogFileValidation', False),
                          region=region,
                          account=account,
                          is_multi_region_trail=self.get_property(properties, 'IsMultiRegionTrail', False))
