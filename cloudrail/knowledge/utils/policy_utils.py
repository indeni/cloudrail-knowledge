from typing import List, Set

from cloudrail.knowledge.context.connection import PolicyEvaluation
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementCondition, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import PrincipalType
from cloudrail.knowledge.utils.action_utils import is_action_fully_defined
from cloudrail.knowledge.utils.arn_utils import are_arns_intersected


def build_condition(statement_dict: dict) -> List[StatementCondition]:
    condition_dict: dict = statement_dict.get('Condition')
    if condition_dict:
        condition_list: List[StatementCondition] = []
        for operator, key_values in condition_dict.items():
            for cond_key, cond_value in key_values.items():
                values_list = [cond_value] if isinstance(cond_value, str) else cond_value
                condition_list.append(StatementCondition(operator, cond_key, values_list))
        return condition_list
    else:
        return []


def is_any_resource_based_action_allowed(policy_evaluation: PolicyEvaluation) -> bool:
    resource_allowed_actions_copy = policy_evaluation.resource_allowed_actions.copy()
    resource_denied_actions_copy = policy_evaluation.resource_denied_actions.copy()
    remove_allowed_from_denied(resource_allowed_actions_copy, resource_denied_actions_copy)
    return len(resource_allowed_actions_copy) > 0


def remove_allowed_from_denied(allowed_actions: Set[str], denied_actions: Set[str]):
    allows_to_remove = set()
    denieds_to_remove = set()
    for allow_action_a in allowed_actions:
        for allow_action_b in allowed_actions:
            if allow_action_a != allow_action_b and is_action_fully_defined(allow_action_a, allow_action_b):
                allows_to_remove.add(allow_action_a)

    for denied_action_a in denied_actions:
        for denied_action_b in denied_actions:
            if denied_action_a != denied_action_b and is_action_fully_defined(denied_action_a, denied_action_b):
                denieds_to_remove.add(denied_action_a)

    for allow_action in allowed_actions:
        for deny_action in denied_actions:
            if is_action_fully_defined(allow_action, deny_action):
                allows_to_remove.add(allow_action)

    for allow_to_remove in allows_to_remove:
        allowed_actions.remove(allow_to_remove)

    for denied_to_remove in denieds_to_remove:
        denied_actions.remove(denied_to_remove)


def is_policy_block_public_access(policy: Policy, aws_resource_arn: str = '*') -> bool:
    for statement in policy.statements:
        if len(statement.condition_block) == 0:
            if statement.principal.principal_type == PrincipalType.PUBLIC or \
                    (statement.principal.principal_type == PrincipalType.AWS and
                     any(value == "*" for value in statement.principal.principal_values)) and \
                    any(are_arns_intersected(res, aws_resource_arn) for res in statement.resources):
                return statement.effect == StatementEffect.DENY
        else:
            return True
    return False
