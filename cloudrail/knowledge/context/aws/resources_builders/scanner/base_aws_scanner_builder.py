import glob
import logging
import os
from abc import abstractmethod
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.resourcegroupstaggingapi.resource_tag_mapping_list import ResourceTagMappingList
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.utils.tags_utils import get_aws_tags
from cloudrail.knowledge.utils.utils import load_as_json, get_regions, get_account_names, get_account_id

from cloudrail.knowledge.context.base_context_builders.base_scanner_builder import BaseScannerBuilder


class BaseAwsScannerBuilder(BaseScannerBuilder):

    def __init__(self, working_dir: str, salt: str):
        self.working_dir = working_dir
        self.accounts = get_account_names(self.working_dir)
        self.salt = salt

    def build(self) -> list:
        data = self._load_raw_data(self.get_file_name(), self.get_section_name())
        result = []
        for attributes in data:
            build_result = self._safe_build(attributes)
            for aws_resource in build_result if isinstance(build_result, list) else [build_result]:
                if aws_resource:
                    self._set_common_attributes(aws_resource, attributes)
                    result.append(aws_resource)
        return result

    def _safe_build(self, attributes):
        try:
            build_result = self.do_build(attributes)
            if build_result and isinstance(build_result, Mergeable) \
                    and (build_result.is_tagable or isinstance(build_result, ResourceTagMappingList)):
                build_result.tags = get_aws_tags(attributes) or get_aws_tags(attributes.get('Value') or {})
            return build_result
        except Exception:
            logging.exception('failed while trying to build resource from scanner data: {}'.format(attributes))
            return None

    @abstractmethod
    def get_section_name(self) -> Optional[str]:
        pass

    def _load_raw_data(self, json_filename: str, section_name: Optional[str]) -> List[dict]:
        data = []
        for account in self.accounts:
            account_id = get_account_id(os.path.join(self.working_dir, account))
            for region in self.get_regions(account):
                file_path_list: List[str] = glob.glob(os.path.join(self.working_dir, account, region, json_filename))
                file_path_list = [file_path for file_path in file_path_list if os.path.isfile(file_path)]
                for file_path in file_path_list:
                    if not (file_data := load_as_json(file_path)):
                        continue

                    region_data = file_data[section_name] if section_name else file_data
                    if isinstance(region_data, list):
                        for element in region_data:
                            element['Region'] = region
                            element['Account'] = account_id
                            element['FilePath'] = file_path
                            element['salt'] = self.salt
                        data.extend(region_data)
                    else:
                        element = {'Region': region, 'Account': account_id, 'FilePath': file_path, 'Value': region_data, 'salt': self.salt}
                        data.append(element)
        return data

    def get_regions(self, account: str) -> List[str]:
        return get_regions(self.working_dir, account)

    @staticmethod
    def _set_common_attributes(resource: AwsResource, attributes: dict):
        if not isinstance(resource, AwsResource):
            return
        if not resource.region:
            resource.region = attributes['Region']
        resource.account = attributes['Account']
        resource.with_aliases(resource.get_id())
