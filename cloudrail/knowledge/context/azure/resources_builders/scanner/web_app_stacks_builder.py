import re
from typing import List
from pkg_resources import parse_version
from cloudrail.knowledge.context.azure.resources.webapp.web_app_stack import WebAppStack
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class WebAppStacksBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'get-web-app-stacks.json'

    def do_build(self, attributes: dict) -> List[WebAppStack]:
        web_app_stacks: List[WebAppStack] = []
        properties: dict = attributes['properties']
        preferred_os = properties.get('preferredOs')
        if preferred_os:
            for stack in properties['majorVersions']:
                if ver_val := re.search(r'\d+', stack['value']):
                    major_version: int = int(ver_val.group())
                    web_app_stacks.append(WebAppStack(name=stack['displayText'],
                                                      preferred_os=preferred_os,
                                                      major_version=major_version,
                                                      minor_versions=[parse_version(ver['value']) for ver in stack['minorVersions']]))
        return web_app_stacks
