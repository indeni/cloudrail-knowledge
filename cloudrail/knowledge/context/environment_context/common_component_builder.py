import json
import logging
import os
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementCondition, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType

ALL_SERVICES_PUBLIC_FULL_ACCESS: PolicyStatement = PolicyStatement(StatementEffect.ALLOW,
                                                                   ['*'],
                                                                   ['*'],
                                                                   Principal(PrincipalType.PUBLIC, []),
                                                                   'AllServicesPublicFullAccess')


def build_policy_statements_from_str(statement_list: str) -> List[PolicyStatement]:
    if not statement_list or statement_list == '':
        return []
    try:
        policy = json.loads(statement_list)
        return [build_policy_statement(statement) for statement in policy['Statement']]
    except ValueError:
        logging.warning(f"failed to parse statements list={str(statement_list)} as string to object")
        return []


def build_condition(statement_dict: dict) -> List[StatementCondition]:
    if condition_dict := statement_dict.get('Condition'):
        condition_list: List[StatementCondition] = []
        for operator, key_values in condition_dict.items():
            for cond_key, cond_value in key_values.items():
                if isinstance(cond_value, str):
                    values_list = [cond_value]
                elif isinstance(cond_value, bool):
                    values_list = ['false'] if not cond_value else ['true']
                else:
                    values_list = cond_value
                condition_list.append(StatementCondition(operator, cond_key, values_list))
        return condition_list
    else:
        return []


def build_policy_statement(raw_data: dict) -> PolicyStatement:
    effect = StatementEffect(raw_data['Effect'])
    actions = raw_data.get('Action', [])
    if isinstance(actions, str):
        actions = [actions]

    resource = raw_data.get('Resource')
    if resource is None:
        resources = []
    else:
        if isinstance(resource, list):
            resources = resource
        else:
            resources = [resource]

    principal = _build_principal(raw_data.get('Principal'))
    condition_block = build_condition(raw_data)
    statement_id = raw_data.get('Sid', '')
    return PolicyStatement(effect, actions, resources, principal, statement_id, condition_block)


def _build_principal(raw_data: str or dict) -> Principal:
    principal_values = []
    if isinstance(raw_data, str):
        principal_type = PrincipalType.PUBLIC
    elif isinstance(raw_data, dict):
        key = next(iter(raw_data))
        if key not in set(item.value for item in PrincipalType):
            principal_type = PrincipalType.IGNORED
        else:
            principal_type = PrincipalType(key)
            value = raw_data[key]
            if isinstance(value, str):
                principal_values.append(value)
            else:  # the value is a list
                for item in value:
                    principal_values.append(item)
    else:
        principal_type = PrincipalType.NO_PRINCIPAL
    return Principal(principal_type, principal_values)


def get_dict_value(dict_ref: dict, key: str, default):
    return default if (key not in dict_ref or dict_ref[key] is None or (not isinstance(dict_ref[key], bool) and not dict_ref[key])) else dict_ref[key]


def extract_attribute_from_file_path(path: str, strings_to_remove: list):
    attribute = os.path.basename(path)
    for string in strings_to_remove:
        attribute = attribute.replace(string, '')
    return attribute.replace('.json', '')


def extract_name_from_gcp_link(gcp_link: str, default=None) -> Optional[str]:
    return gcp_link.split('/')[-1] if gcp_link else default
