import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Set, Dict

import yaml
from cloudrail.knowledge.context.cloud_provider import CloudProvider


class RuleSeverity(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    MAJOR = 'major'

    def as_int(self) -> int:
        if self == RuleSeverity.LOW:
            return 0
        if self == RuleSeverity.MEDIUM:
            return 1
        if self == RuleSeverity.MAJOR:
            return 2
        else:
            return -1


class RuleType(str, Enum):
    NON_CONTEXT_AWARE = 'non_context_aware'
    CONTEXT_AWARE = 'context_aware'


class SecurityLayer(str, Enum):
    IAM = 'iam'
    ENCRYPTION = 'encryption'
    NETWORKING = 'networking'
    LOGGING = 'logging'
    CODE = 'code'
    DISASTER_RECOVERY = 'disaster_recovery'
    STORAGE = 'storage'
    TAGGING = 'tagging'


class ResourceType(str, Enum):
    ALL = 'all'
    KUBERNETES = 'kubernetes'
    COMPUTE = 'compute'
    IAM = 'iam'
    FIREWALL = 'firewall'
    STORAGE = 'storage'
    KEY_MGMT = 'key_mgmt'
    NETWORK = 'network'
    DATABASE = 'database'
    CLOUDFRONT = 'cloudfront'
    CONTENT_DELIVERY = 'content_delivery'
    SERVICE_ENDPOINT = 'service_endpoint'
    CODE = 'code'
    LOGGING = 'logging'
    QUEUING = 'queuing'
    NOTIFICATION = 'notification'
    STREAMING = 'streaming'
    SECURITY_SERVICES = 'security_services'


class BenchmarkType(str, Enum):
    PCI_DSS = "PCI DSS"
    CIS = "CIS"


@dataclass
class RemediationSteps:
    console: str
    terraform: Optional[str] = None
    cloudformation: Optional[str] = None


@dataclass
class RuleMetadata:
    rule_id: str
    name: str
    description: str
    logic: str
    severity: RuleSeverity
    remediation_steps: RemediationSteps
    rule_type: RuleType
    security_layer: SecurityLayer
    resource_types: Set[ResourceType]
    cloud_provider: CloudProvider = field(default=CloudProvider.AMAZON_WEB_SERVICES)
    is_deleted: bool = False
    compliance: Dict[BenchmarkType, Dict[str, str]] = field(default_factory=dict)


def rule_matches_query(rule_id: str, rule_name: str, query: Optional[str]) -> bool:
    if not query:
        return True
    return query.lower() in rule_id.lower() or query.lower() in rule_name.lower()


def get_rule_metadata_content(provider: CloudProvider) -> dict:
    provider_name = provider.to_shorthand_string()

    current_path = os.path.dirname(os.path.abspath(__file__))
    rules_metadata_path = os.path.join(current_path, f'{provider_name}/{provider_name}_rules_metadata.yaml')
    with open(rules_metadata_path, 'r') as file:
        return yaml.load(file)
