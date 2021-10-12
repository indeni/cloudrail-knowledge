import os
from typing import Dict, Optional, List

import yaml
from cloudrail.knowledge.context.iac_type import IacType

from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.rules.rule_metadata import RuleMetadata, RuleSeverity, RuleType, SecurityLayer, ResourceType, BenchmarkType, RemediationSteps

RULE_ID = 'rule_id'
NAME = 'name'
DESCRIPTION = 'description'
LOGIC = 'human_readable_logic'
REMEDIATION_STEPS = 'remediation_steps'
CONSOLE = 'console'
TERRAFORM = 'terraform'
CLOUDFORMATION = 'cloudformation'
SEVERITY = 'severity'
RULE_TYPE = 'rule_type'
SECURITY_LAYER = 'security_layer'
RESOURCE_TYPE = 'resource_type'
CLOUD_PROVIDER = 'cloud_provider'
COMPLIANCE = 'compliance'
RULE_METADATA_NOT_FOUND = 'Rule {} metadata not found'
SUPPORTED_IAC_TYPES = 'supported_iac_types'


class RulesMetadataStore:
    def __init__(self, rules_metadata_dict: dict):
        self.rules_metadata: Dict[str, RuleMetadata] = self._get_rules_metadata_from_dict(rules_metadata_dict)

    def get_by_rule_id(self, rule_id: str) -> Optional[RuleMetadata]:
        return self.rules_metadata.get(rule_id)

    def list_rules_metadata(self) -> List[RuleMetadata]:
        return list(self.rules_metadata.values())

    def add_rules_metadata(self, new_rules_metadata_dict: dict):
        new_rules_metadata = self._get_rules_metadata_from_dict(new_rules_metadata_dict)
        self.rules_metadata = {**self.rules_metadata, **new_rules_metadata}

    def merge(self, rule_metadata_store: 'RulesMetadataStore'):
        self.rules_metadata = {**self.rules_metadata, **rule_metadata_store.rules_metadata}

    @staticmethod
    def _is_template(value):
        if value is not None and isinstance(value, dict):
            return True
        return False

    @staticmethod
    def _fill_template(params_dict, templates):
        template_name = params_dict['template']
        if params_dict.get('params'):
            params = params_dict['params']
            for template in templates:
                for key, value in template.items():
                    if key == template_name:
                        return value.format(*tuple(params))
            return None
        else:
            for template in templates:
                for key, value in template.items():
                    if key == template_name:
                        return value
            return None

    @staticmethod
    def _fill_templates(rules, templates):
        for rule in rules:
            if RulesMetadataStore._is_template(rule.get(NAME)):
                rule[NAME] = RulesMetadataStore._fill_template(rule[NAME], templates)
            if RulesMetadataStore._is_template(rule.get(DESCRIPTION)):
                rule[DESCRIPTION] = RulesMetadataStore._fill_template(rule[DESCRIPTION], templates)
            if RulesMetadataStore._is_template(rule.get(LOGIC)):
                rule[LOGIC] = RulesMetadataStore._fill_template(rule[LOGIC], templates)
            remediation_steps: dict = rule.get(REMEDIATION_STEPS, {})
            if RulesMetadataStore._is_template(remediation_steps.get(TERRAFORM)):
                remediation_steps[TERRAFORM] = RulesMetadataStore._fill_template(remediation_steps[TERRAFORM], templates)
            if RulesMetadataStore._is_template(remediation_steps.get(CONSOLE)):
                remediation_steps[CONSOLE] = RulesMetadataStore._fill_template(remediation_steps[CONSOLE], templates)
            if RulesMetadataStore._is_template(remediation_steps.get(CLOUDFORMATION)):
                remediation_steps[CLOUDFORMATION] = RulesMetadataStore._fill_template(remediation_steps[CLOUDFORMATION], templates)
        return rules

    @staticmethod
    def _verify_all_fields_filled(rules):
        for rule in rules:
            if not rule.get(RULE_ID) \
                    or not rule.get(NAME) \
                    or not rule.get(DESCRIPTION) \
                    or not rule.get(LOGIC) \
                    or not rule.get(SEVERITY) \
                    or not rule.get(RULE_TYPE) \
                    or not rule.get(SECURITY_LAYER) \
                    or not rule.get(RESOURCE_TYPE) \
                    or not rule.get(SUPPORTED_IAC_TYPES):
                raise Exception(f'Invalid rule metadata {rule.get(RULE_ID) or rule}')

    @staticmethod
    def _verify_name_unique(rules):
        names = [rule[NAME] for rule in rules]
        if len(names) > len(set(names)):
            raise Exception('rule_id should be unique, duplicates: {}'.format({x for x in names if names.count(x) > 1}))

    @staticmethod
    def _verify_id_unique(rules):
        rule_ids = [rule[RULE_ID] for rule in rules]
        if len(rule_ids) > len(set(rule_ids)):
            raise Exception('rule_id should be unique, duplicates: {}'.format({x for x in rule_ids if rule_ids.count(x) > 1}))

    @staticmethod
    def _verify_rule_id_not_template(rules):
        if len(list(filter(lambda x: isinstance(x, dict), [rule[RULE_ID] for rule in rules]))) > 0:
            raise Exception('rule id can not be template based')

    @classmethod
    def _verify_rules(cls, rules):
        cls._verify_all_fields_filled(rules)
        cls._verify_name_unique(rules)
        cls._verify_id_unique(rules)
        cls._verify_rule_id_not_template(rules)

    @staticmethod
    def _parse_compliance(compliance_dict: dict) -> Dict[BenchmarkType, Dict[str, str]]:
        result = {}
        for framework, versions in compliance_dict.items():
            result[BenchmarkType(framework)] = {}
            for version, sections in versions.items():
                if not isinstance(sections, list):
                    raise Exception(f'section of benchmark {framework} version {version} is not of type list')
                result[BenchmarkType(framework)][str(version)] = [str(section) for section in sections]
        return result

    def _get_rules_metadata_from_dict(self, raw_data: dict) -> Dict[str, RuleMetadata]:
        rules = self._fill_templates(raw_data.get('rules_metadata', []), raw_data.get('templates', []))
        self._verify_rules(rules)
        return {rule[RULE_ID]: RuleMetadata(
            rule_id=rule[RULE_ID],
            name=rule[NAME],
            description=rule[DESCRIPTION],
            logic=rule[LOGIC],
            severity=RuleSeverity(rule[SEVERITY]),
            rule_type=RuleType(rule[RULE_TYPE]),
            security_layer=SecurityLayer(rule[SECURITY_LAYER]),
            resource_types={ResourceType(resource_type) for resource_type in rule[RESOURCE_TYPE]},
            remediation_steps=RemediationSteps(terraform=rule.get(REMEDIATION_STEPS).get(TERRAFORM, ''),
                                               console=rule.get(REMEDIATION_STEPS).get(CONSOLE, ''),
                                               cloudformation=rule.get(REMEDIATION_STEPS).get(CLOUDFORMATION, '')),
            cloud_provider=CloudProvider(rule[CLOUD_PROVIDER]),
            is_deleted=rule.get('is_deleted', False),
            compliance=self._parse_compliance(rule.get(COMPLIANCE, {})),
            supported_iac_types={IacType(iac_type) for iac_type in rule[SUPPORTED_IAC_TYPES]}
        ) for rule in rules}


def read_metadata_file(file_path: str):
    with open(file_path, 'r') as file:
        return yaml.load(file)


class CloudrailRulesMetadataStore(RulesMetadataStore):
    def __init__(self):
        super().__init__({})
        self.add_rules_metadata(read_metadata_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aws/aws_rules_metadata.yaml')))
        self.add_rules_metadata(read_metadata_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'azure/azure_rules_metadata.yaml')))
        self.add_rules_metadata(read_metadata_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gcp/gcp_rules_metadata.yaml')))
