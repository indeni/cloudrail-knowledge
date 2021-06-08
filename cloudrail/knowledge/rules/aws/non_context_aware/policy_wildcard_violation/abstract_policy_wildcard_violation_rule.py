import functools
import logging
from abc import abstractmethod
from typing import List, Dict, Optional, Tuple, Union
from cloudrail.knowledge.context.aws.iam.policy import Policy
from cloudrail.knowledge.context.aws.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AbstractPolicyWildcardViolationRule(AwsBaseRule):

    def __init__(self,
                 resource_name: str,
                 resource_entity_name: str,
                 violating_actions: List) -> None:
        self.resource_name: str = resource_name
        self.resource_entity_name: str = resource_entity_name
        self.violating_actions: List = violating_actions

    @abstractmethod
    def get_id(self) -> str:
        pass

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        rule_entity = self._get_rule_entities(env_context)

        for entity in rule_entity:
            policy = self._get_entity_policy(entity)
            if policy and policy.statements:
                for action, principal in self._find_violating_actions_and_principals(policy, self.violating_actions):
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
    def check_actions(action: str, fault_actions: list) -> Optional[str]:
        if action in ('*') or action in fault_actions:
            return action
        else:
            return None

    @staticmethod
    def check_principal(policy: PolicyStatement) -> Optional[Principal]:
        if (any(value == '*' for value in policy.principal.principal_values) or not policy.principal.principal_values)\
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
                    filtered_action = self.check_actions(action, actions)
                    returned_action = self.return_action_principal(filtered_action, actions_list)
                principal = self.check_principal(policy_statement)
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
        return bool(self._get_rule_entities(environment_context))

    @functools.lru_cache(maxsize=None)
    def _get_rule_entities(self, env_context: AwsEnvironmentContext) -> Optional[List[AwsResource]]:
        supported_resource_list = [{'cloudwatch_logs_destinations': env_context.cloudwatch_logs_destinations},
                                   {'ecr_repositories': env_context.ecr_repositories},
                                   {'efs_file_systems': env_context.efs_file_systems},
                                   {'elastic_search_domains': env_context.elastic_search_domains},
                                   {'glacier_vaults': env_context.glacier_vaults},
                                   {'rest_api_gw': env_context.rest_api_gw},
                                   {'s3_buckets': env_context.s3_buckets},
                                   {'secrets_manager_secrets': env_context.secrets_manager_secrets},
                                   {'sqs_queues': env_context.sqs_queues},
                                   {'kms_keys': [kms_key for kms_key in env_context.kms_keys if kms_key.key_manager == KeyManager.CUSTOMER]},
                                   {'lambda_function_list': env_context.lambda_function_list}]
        for line in supported_resource_list:
            if all(key != self.resource_entity_name for key in line.items()):
                logging.info(f'{self.resource_entity_name} is not a supported entity')
            for key, value in line.items():
                if key == self.resource_entity_name:
                    return value
        return None

    @staticmethod
    @abstractmethod
    def _get_entity_policy(entity: AwsResource) -> Policy:
        pass
