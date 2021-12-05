import glob
import logging
import os
from abc import abstractmethod
from typing import List, Dict

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.utils.utils import get_account_names
from cloudrail.knowledge.utils.utils import load_as_json
from cloudrail.knowledge.utils.string_utils import StringUtils
from cloudrail.knowledge.context.base_context_builders.base_scanner_builder import BaseScannerBuilder


class BaseAzureScannerBuilder(BaseScannerBuilder):

    def __init__(self, account_data_folder: str, subscription_id: str, tenant_id: str) -> None:
        super().__init__()
        self.account_data_folder: str = account_data_folder
        self.subscription_id: str = subscription_id
        self.tenant_id: str = tenant_id
        self.accounts = get_account_names(self.account_data_folder)

    @abstractmethod
    def do_build(self, attributes: dict) -> AzureResource:
        pass

    def build(self) -> List[AzureResource]:
        try:
            data: List[Dict] = self._load_raw_data()
            resources = []
            for attributes in data:
                build_result = self.do_build(attributes)
                for resource in build_result if isinstance(build_result, list) else [build_result]:
                    if resource:
                        self._set_common_attributes(resource, attributes)
                        resources.append(resource)
            return resources
        except Exception as ex:
            logging.exception(msg='failed while trying to build resource from scanner data', exc_info=ex)
            return []

    def _load_raw_data(self) -> List[Dict]:
        azure_resources_map: Dict[str, Dict] = {}
        for account_name in self.accounts:
            file_path_list: List[str] = glob.glob(os.path.join(self.account_data_folder, account_name, self.get_file_name()))
            for file_path in file_path_list:
                file_content = load_as_json(file_path)
                for azure_resource in file_content['value']:
                    key: str = azure_resource.get('id') or azure_resource.get('name')
                    if key in azure_resources_map:
                        StringUtils.dict_deep_update(azure_resources_map[key], azure_resource)
                    else:
                        azure_resource['FilePath'] = file_path
                        azure_resources_map[key] = azure_resource
        return list(azure_resources_map.values())

    def _set_common_attributes(self, resource: AzureResource, attributes: dict):
        if not isinstance(resource, AzureResource):
            return
        resource.subscription_id = self.subscription_id
        resource.location = attributes.get('location')
        resource.resource_group_name = attributes.get('resourceGroup')
        resource.tenant_id = self.tenant_id
        if resource.is_tagable:
            resource.tags = attributes.get('tags')
        if not resource.get_id() and (_id := attributes.get('id')):
            resource.set_id(_id)
            resource.with_aliases(_id)
