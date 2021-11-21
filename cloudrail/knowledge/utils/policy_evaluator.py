import functools
import os
from typing import List, Set, Optional, Dict

from botocore.utils import ArnParser
from cloudrail.knowledge.context.connection import PolicyEvaluation
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect, PolicyStatement
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.utils.action_utils import get_intersected_actions, is_action_fully_defined, attribute_match
from cloudrail.knowledge.utils.arn_utils import is_arn_contained_in_arn, is_valid_arn
from cloudrail.knowledge.utils.utils import load_as_json, flat_list


def copy_policy_evaluation(policy_evaluation: PolicyEvaluation):
    return PolicyEvaluation(policy_evaluation.resource_allowed_actions.copy(),
                            policy_evaluation.resource_denied_actions.copy(),
                            policy_evaluation.identity_allowed_actions.copy(),
                            policy_evaluation.identity_denied_actions.copy(),
                            permission_boundary_applied=policy_evaluation.permission_boundary_applied,
                            permission_boundary_allowed_actions=policy_evaluation.permission_boundary_allowed_actions.copy(),
                            permission_boundary_denied_actions=policy_evaluation.permission_boundary_denied_actions.copy())


def get_allowed_actions(policy_evaluation: PolicyEvaluation) -> Set[str]:
    actions = set()
    allowed_actions = policy_evaluation.resource_allowed_actions.copy()
    if policy_evaluation.permission_boundary_applied:
        intersected_actions = flat_list(
            [get_intersected_actions(policy_evaluation.permission_boundary_allowed_actions, x) for x in policy_evaluation.identity_allowed_actions])
        allowed_actions = allowed_actions.union(intersected_actions)
    else:
        allowed_actions = allowed_actions.union(policy_evaluation.identity_allowed_actions)
    for action in allowed_actions:
        if is_action_subset_allowed(policy_evaluation, action):
            actions.add(action)
    return actions


def is_any_action_allowed(policy_evaluation: PolicyEvaluation):
    for action in policy_evaluation.resource_allowed_actions.union(policy_evaluation.identity_allowed_actions):
        if is_action_subset_allowed(policy_evaluation, action):
            return True
    return False


def is_action_subset_allowed(policy_evaluation: PolicyEvaluation, action: str) -> bool:
    if any(is_action_fully_defined(action, x) for x in policy_evaluation.identity_denied_actions):
        return False
    if any(is_action_fully_defined(action, x) for x in policy_evaluation.resource_denied_actions):
        return False
    if get_intersected_actions(list(policy_evaluation.resource_allowed_actions), action):
        return True
    if intersected_actions := get_intersected_actions(list(policy_evaluation.identity_allowed_actions), action):
        if not policy_evaluation.permission_boundary_applied:
            return True
        for intersected_action in intersected_actions:
            if any(is_action_fully_defined(intersected_action, x) for x in policy_evaluation.permission_boundary_denied_actions):
                return False
            if get_intersected_actions(list(policy_evaluation.permission_boundary_allowed_actions), intersected_action):
                return True
    return False


# TODO: Add Organizations SCP support
# TODO: Add Session Policies support (or figure out if it is even needed)
class PolicyEvaluator:
    @staticmethod
    def evaluate_actions(source: Optional[AwsResource],
                         destination: AwsResource,
                         resource_based_policies: List[Policy],
                         identity_based_policies: List[Policy],
                         permission_boundary: Optional[Policy]) -> PolicyEvaluation:
        """
        Evaluates what actions the `source` can perform on the `destination` by assessing the policies, according to
        `AWS Policy Evaluation Logic user-guide <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html>`_
        """

        resource_based_policies_statements = flat_list([x.statements for x in resource_based_policies if x])
        identity_based_policies_statements = flat_list([x.statements for x in identity_based_policies if x])

        evaluation_result: PolicyEvaluation = PolicyEvaluation()

        for action in PolicyEvaluator.get_resource_actions(destination.get_aws_service_type()):

            evaluation_result.resource_denied_actions.update(
                PolicyEvaluator._get_applicable_actions_by_effect(
                    action, resource_based_policies_statements, source, destination, StatementEffect.DENY)
            )

            evaluation_result.resource_allowed_actions.update(
                PolicyEvaluator._get_applicable_actions_by_effect(
                    action, resource_based_policies_statements, source, destination, StatementEffect.ALLOW)
            )

            evaluation_result.identity_denied_actions.update(
                PolicyEvaluator._get_applicable_actions_by_effect(
                    action, identity_based_policies_statements, source, destination, StatementEffect.DENY)
            )

            evaluation_result.identity_allowed_actions.update(
                PolicyEvaluator._get_applicable_actions_by_effect(
                    action, identity_based_policies_statements, source, destination, StatementEffect.ALLOW)
            )

            if permission_boundary:
                permission_boundary_policies_statements = permission_boundary.statements
                evaluation_result.permission_boundary_applied = True

                evaluation_result.permission_boundary_denied_actions.update(
                    PolicyEvaluator._get_applicable_actions_by_effect(
                        action, permission_boundary_policies_statements, source, destination, StatementEffect.DENY)
                )

                evaluation_result.permission_boundary_allowed_actions.update(
                    PolicyEvaluator._get_applicable_actions_by_effect(
                        action, permission_boundary_policies_statements, source, destination, StatementEffect.ALLOW)
                )

        return evaluation_result

    @staticmethod
    def with_additional_policies(source: AwsResource,
                                 destination: AwsResource,
                                 evaluation_result: PolicyEvaluation,
                                 resource_based_policies: List[Policy]) -> PolicyEvaluation:
        """
        Use this function to evaluate policies over an existing evaluation.
        """
        new_evaluation_result = copy_policy_evaluation(evaluation_result)
        statements = flat_list([x.statements for x in resource_based_policies if x])

        for action in PolicyEvaluator.get_resource_actions(destination.get_aws_service_type()):
            new_evaluation_result.resource_denied_actions.update(
                PolicyEvaluator._get_applicable_actions_by_effect(
                    action, statements, source, destination, StatementEffect.DENY)
            )

            new_evaluation_result.resource_allowed_actions.update(
                PolicyEvaluator._get_applicable_actions_by_effect(
                    action, statements, source, destination, StatementEffect.ALLOW)
            )

        return new_evaluation_result

    @staticmethod
    def get_resource_actions(aws_service_type: str) -> List[str]:
        json = load_as_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'actions.json'))
        return json[aws_service_type]

    @classmethod
    def _get_applicable_actions_by_effect(cls, action: str,
                                          statements: List[PolicyStatement],
                                          source: AwsResource,
                                          destination: AwsResource,
                                          effect: StatementEffect) -> List[str]:
        filtered_statements = [x for x in statements if x.effect == effect]
        actions = [cls._get_applicable_actions(action, statement, source, destination) for statement in filtered_statements]
        return flat_list(actions)

    @classmethod
    def _get_applicable_actions(cls, action: str, statement: PolicyStatement, source: AwsResource, destination: AwsResource) -> List[str]:
        if cls._is_resource_defined(statement.resources, destination):
            if cls._is_principal_allowed(statement.principal, source):
                return cls._get_action_defined(statement.actions, action)
        return []

    @classmethod
    def _is_principal_allowed(cls, principal: Principal, source: AwsResource):
        return principal.principal_type == PrincipalType.PUBLIC or \
               principal.principal_type == PrincipalType.NO_PRINCIPAL or \
               cls._is_principal_match(principal, source) or \
               cls._is_service_domain_name_match(principal, source)

    @classmethod
    def _is_principal_match(cls, principal: Principal, source: Mergeable) -> bool:
        cls._convert_principal_to_account_owner_arn(principal)
        return principal.principal_type == PrincipalType.AWS and source and source.get_arn() and \
               any(is_arn_contained_in_arn(source.get_arn(), x) for x in principal.principal_values)  # todo - need to support arn tf address

    @staticmethod
    def _convert_principal_to_account_owner_arn(principal: Principal):
        if principal.principal_type == PrincipalType.AWS:
            for index, principal_value in enumerate(principal.principal_values):
                if principal_value.isnumeric():
                    principal.principal_values[index] = f"arn:aws:iam::{principal_value}:root"

    @staticmethod
    def _is_service_domain_name_match(principal: Principal, source: AwsResource):
        return principal.principal_type == PrincipalType.SERVICE and \
               source and \
               any(source.get_aws_service_attributes() and source.get_aws_service_attributes().get_qualified_service_name() == service
                   for service in principal.principal_values)

    @classmethod
    def _get_action_defined(cls, statement_actions: List[str], action: str) -> List[str]:
        return get_intersected_actions(statement_actions, action)

    @classmethod
    def _is_resource_defined(cls, resources: List[str], destination: AwsResource) -> bool:
        for resource in resources:
            try:
                if destination.is_arn_match(resource):
                    return True
            except Exception:
                if destination.iac_state and destination.iac_state.address in resource:
                    return True
        return False

    @staticmethod
    def evaluate_and_get_all_allow_statements(statements_by_effect_map: Dict[StatementEffect, List[PolicyStatement]]) -> List[PolicyStatement]:
        for allow_statement in statements_by_effect_map[StatementEffect.ALLOW]:
            for deny_statement in statements_by_effect_map[StatementEffect.DENY]:
                PolicyEvaluator.remove_denied_actions(allow_statement, deny_statement)
                if not allow_statement.actions:
                    statements_by_effect_map[StatementEffect.ALLOW].remove(allow_statement)
                    break
        return statements_by_effect_map[StatementEffect.ALLOW]

    @classmethod
    def remove_denied_actions(cls, allow_statement: PolicyStatement, deny_statement: PolicyStatement):
        if cls.all_resources_match(deny_statement, allow_statement):
            for allow_action in allow_statement.actions:
                for deny_action in deny_statement.actions:
                    if attribute_match(deny_action, allow_action):
                        allow_statement.actions.remove(allow_action)

    @classmethod
    def all_resources_match(cls, src_statement: PolicyStatement, target_statement: PolicyStatement):
        countdown: int = len(target_statement.resources)
        for target_resource in target_statement.resources:
            for src_resource in src_statement.resources:
                if attribute_match(src_resource, target_resource):
                    countdown -= 1
                    break
        return countdown == 0

    @staticmethod
    @functools.lru_cache(maxsize=100)
    def equals_resources(resource1: str, resource2: str) -> bool:
        if is_valid_arn(resource1) and is_valid_arn(resource2):
            parser: ArnParser = ArnParser()
            resource_arn1: dict = parser.parse_arn(resource1)
            resource_arn2: dict = parser.parse_arn(resource2)
            return resource_arn1["account"] == resource_arn2["account"] and resource_arn1["resource"] == resource_arn2["resource"]
        else:
            return resource1 == resource2
