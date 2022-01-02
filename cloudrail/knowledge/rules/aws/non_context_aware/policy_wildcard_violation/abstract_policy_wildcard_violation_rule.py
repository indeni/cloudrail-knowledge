from abc import abstractmethod
from typing import List, Dict, Optional, Tuple, Union

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.aws_policied_resource import PoliciedResource
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AbstractPolicyWildcardViolationRule(AwsBaseRule):
    @abstractmethod
    def _get_violating_actions(self) -> list:
        pass

    @abstractmethod
    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        pass

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        rule_entity = self._get_context_policy_resources(env_context)

        for entity in rule_entity:
            policy = entity.resource_based_policy
            if policy and policy.statements:
                for action, principal in self._find_violating_actions_and_principals(policy, self._get_violating_actions()):
                    if action and principal:
                        issues.append(
                            Issue(
                                f"The policy attached to the {entity.get_type()} `{entity.get_friendly_name()}` is "
                                f"using wildcard action `{action}`, and principal `{self._principal_string(principal)}`, "
                                f"without any condition", entity, policy))
                    elif action and not principal:
                        issues.append(
                            Issue(
                                f"The policy attached to the {entity.get_type()} `{entity.get_friendly_name()}` is "
                                f"using wildcard action `{action}`, without any condition", entity, policy))
                    elif principal and not action:
                        issues.append(
                            Issue(
                                f"The policy attached to the {entity.get_type()} `{entity.get_friendly_name()}` is "
                                f"using principal `{self._principal_string(principal)}`,"
                                f" without any condition", entity, policy))
            else:
                issues.append(
                    Issue(
                        f"There is no resource policy or no statements attached to `{entity.get_friendly_name()}`", entity, entity))
        return issues

    @staticmethod
    def _principal_string(principal: Principal) -> str:
        return f"{principal.principal_type.value.replace('Public', 'AWS')}: *"

    @staticmethod
    def _check_actions(action: str, fault_actions: list) -> Optional[str]:
        if action in ('*') or action in fault_actions:
            return action
        else:
            return None

    @staticmethod
    def _check_principal(policy: PolicyStatement) -> Optional[Principal]:
        if (any(value == '*' for value in policy.principal.principal_values) or not policy.principal.principal_values) \
                and policy.principal.principal_type not in (PrincipalType.IGNORED, PrincipalType.NO_PRINCIPAL):
            return policy.principal
        else:
            return None

    def _find_violating_actions_and_principals(self, item: Policy, actions: list) -> List[Tuple[Optional[str], Optional[Principal]]]:
        actions_list = []
        principals_list = []
        return_list = []
        for policy_statement in item.statements:
            if policy_statement.effect == StatementEffect.ALLOW and not policy_statement.condition_block:
                returned_action = ''
                for action in policy_statement.actions:
                    filtered_action = self._check_actions(action, actions)
                    returned_action = self.return_action_principal(filtered_action, actions_list)
                principal = self._check_principal(policy_statement)
                return_list.append((returned_action, self.return_action_principal(principal, principals_list)))
        return return_list

    @staticmethod
    def return_action_principal(item: Union[Optional[str], Optional[Principal]], item_list: List) -> Union[Optional[str], Optional[Principal]]:
        if item and item not in item_list:
            item_list.append(item)
            return item
        else:
            return None

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(self._get_context_policy_resources(environment_context))
