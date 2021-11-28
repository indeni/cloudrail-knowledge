import glob
import logging
import os
from abc import abstractmethod
from typing import Dict, List

from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource
from cloudrail.knowledge.utils.utils import get_account_names, load_as_json
from cloudrail.knowledge.utils.tags_utils import get_gcp_labels

from cloudrail.knowledge.context.base_context_builders.base_scanner_builder import BaseScannerBuilder


class BaseGcpScannerBuilder(BaseScannerBuilder):

    def __init__(self, account_data_folder: str, project_id: str, salt: str):
        super().__init__()
        self.account_data_folder: str = account_data_folder
        self.project_id: str = project_id
        self.salt: str = salt
        self.accounts = get_account_names(self.account_data_folder)

    @abstractmethod
    def do_build(self, attributes: dict) -> GcpResource:
        pass

    def build(self) -> List[GcpResource]:
        try:
            data: List[Dict] = self._load_raw_data()
            resources = []
            for attributes in data:
                resource = self.do_build(attributes)
                if resource:
                    self._set_common_attributes(resource, attributes)
                    resources.append(resource)
            return resources
        except Exception as ex:
            logging.exception(msg='failed while trying to build resource from scanner data', exc_info=ex)
            return []

    def _load_raw_data(self) -> List[Dict]:
        resources = []
        for account_name in self.accounts:
            file_path_list: List[str] = glob.glob(os.path.join(self.account_data_folder, account_name, self.get_file_name()))
            for file_path in file_path_list:
                file_content = load_as_json(file_path)
                for gcp_resource in file_content['value']:
                    gcp_resource['FilePath'] = file_path
                    gcp_resource['salt'] = self.salt
                    resources.append(gcp_resource)
        return resources

    def _set_common_attributes(self, resource: GcpResource, attributes: dict):
        if not isinstance(resource, GcpResource):
            return

        resource.project_id = self.project_id
        resource.tags = attributes.get('tags', {}).get('items')
        if not resource.labels:
            resource.labels = get_gcp_labels(attributes.get('labels'), attributes['salt'])

    @staticmethod
    def get_project_from_url(url: str) -> str:
        if url:
            split_url = url.split('projects')[1]
            return split_url.split('/')[1]
        return None
