from abc import abstractmethod
from typing import List, Dict, Union, Optional
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.iac_resource_metadata import IacResourceMetadata
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_utils import ELEMENT_POSITION_KEY
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.cloudformation.intrinsic_functions.cloudformation_intrinsic_functions import CloudformationFunction
from cloudrail.knowledge.utils.string_utils import generate_random_string
from cloudrail.knowledge.utils.tags_utils import get_aws_tags


class BaseCloudformationBuilder:

    CFN_PSEUDO_PREFIX: str = 'cfn-pseudo'

    def __init__(self, cfn_resource_type: CloudformationResourceType, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__()
        self._resources: Dict[str, Dict] = cfn_by_type_map.get(cfn_resource_type, {})

    def build(self) -> list:
        aws_resources_list: List[AwsResource] = []
        for cfn_resource in self._resources.values():
            if 'Properties' not in cfn_resource:
                cfn_resource['Properties'] = {}

            build_result = self.parse_resource(cfn_resource)
            for aws_resource in build_result if isinstance(build_result, list) else [build_result]:
                if aws_resource:
                    self._set_common_attributes(aws_resource, cfn_resource)
                    aws_resources_list.append(aws_resource)
        return aws_resources_list

    @abstractmethod
    def parse_resource(self, cfn_res_attr: dict) -> Union[AwsResource, List[AwsResource]]:
        pass

    @staticmethod
    def get_resource_id(cfn_resource: dict) -> str:  # could be name/id...or some other defined field
        return cfn_resource['physical_id'] if 'physical_id' in cfn_resource else cfn_resource['logical_id']

    @staticmethod
    def is_physical_id_exist(cfn_resource: dict) -> bool:
        return 'physical_id' in cfn_resource

    @staticmethod
    def get_property(properties: dict, property_name: str, default=None):
        prop_value = properties.get(property_name, default)
        if not CloudformationFunction.is_all_values_valid(prop_value):
            return default
        else:
            return prop_value

    @classmethod
    def get_name_tag(cls, properties: dict) -> str:
        return cls.get_tag(properties, 'Name')

    @staticmethod
    def get_tag(properties: dict, tag_name: str) -> str:
        return next(iter(key_val_pair['Value'] for key_val_pair in properties.get('Tags', []) if key_val_pair['Key'] == tag_name), None)

    @staticmethod
    def get_tags(properties: dict) -> Dict[str, str]:
        return {key_val_pair['Key']: key_val_pair['Value'] for key_val_pair in properties.get('Tags', [])}

    @staticmethod
    def _set_common_attributes(resource: AwsResource, cfn_resource: dict):
        if not isinstance(resource, AwsResource):
            return
        metadata: Optional[IacResourceMetadata] = None
        if cfn_resource.get('iac_action') != IacActionType.DELETE:
            start_line, end_line = cfn_resource[ELEMENT_POSITION_KEY]
            metadata = IacResourceMetadata(iac_entity_id=cfn_resource['logical_id'],
                                           file_name=cfn_resource['cfn_template_file_name'],
                                           start_line=start_line,
                                           end_line=end_line)
        resource.iac_state = IacState(address=cfn_resource['logical_id'],
                                      action=cfn_resource['iac_action'],
                                      is_new=cfn_resource['iac_action'] == IacActionType.CREATE,
                                      resource_metadata=metadata)
        resource.iac_state.iac_resource_url = metadata and metadata.get_iac_resource_url(cfn_resource.get('iac_url_template'))
        attributes = cfn_resource.get('Properties')
        resource.tags = get_aws_tags(attributes)

    def create_random_pseudo_identifier(self) -> str:
        return f'{self.CFN_PSEUDO_PREFIX}-{generate_random_string()}'
