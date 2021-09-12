import functools
from typing import Dict, Optional

from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.exceptions import UnsupportedCloudProviderException
from cloudrail.knowledge.rules.base_rule import BaseRule

from cloudrail.knowledge.rules.aws_rules_loader import AwsRulesLoader
from cloudrail.knowledge.rules.azure_rules_loader import AzureRulesLoader
from cloudrail.knowledge.rules.gcp_rules_loader import GcpRulesLoader


class RulesLoader:

    @classmethod
    def load(cls, cloud_provider: Optional[CloudProvider] = None) -> Dict[str, BaseRule]:
        if not cloud_provider:
            return {**AwsRulesLoader().load(), **AzureRulesLoader().load(), **GcpRulesLoader().load()}
        if cloud_provider == CloudProvider.AMAZON_WEB_SERVICES:
            return AwsRulesLoader().load()
        if cloud_provider == CloudProvider.AZURE:
            return AzureRulesLoader().load()
        if cloud_provider == CloudProvider.GCP:
            return GcpRulesLoader().load()
        raise UnsupportedCloudProviderException(cloud_provider)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def get_rules_source_control_links(cls) -> Dict[str, str]:
        rules = cls.load()
        source_control_links = {}
        for rule_id, rule in rules.items():
            rule_module = rule.__module__
            if not rule_module.startswith('cloudrail.knowledge'):
                continue
            rule_path = rule_module.replace('.', '/')
            source_control_link = f'https://github.com/indeni/cloudrail-knowledge/blob/main/{rule_path}.py'
            source_control_links[rule_id] = source_control_link
        return source_control_links
