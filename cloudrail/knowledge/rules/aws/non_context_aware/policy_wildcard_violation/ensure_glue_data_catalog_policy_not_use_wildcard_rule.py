from typing import Dict, List, Optional, Union

from cloudrail.knowledge.context.aws.resources.glue.glue_data_catalog_policy import GlueDataCatalogPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureGlueDataCatalogPolicyNotUseWildcard(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_aws_glue_data_catalog_policy_wildcard'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for gdc_policy in env_context.glue_data_catalog_policy:
            glue_resources = self._get_glue_resources(env_context, gdc_policy.region)
            for action, principal in self._find_violating_actions_and_principals(gdc_policy, ['glue:*']):
                for glue_resource in glue_resources:
                    if action and principal:
                        issues.append(
                            Issue(
                                f"The {gdc_policy.get_type()} in region `{gdc_policy.region}` is "
                                f"using wildcard action `{action}`, and principal `{self._principal_string(principal)}`, "
                                f"without any condition", glue_resource, gdc_policy))
                    elif action and not principal:
                        issues.append(
                            Issue(
                                f"The {gdc_policy.get_type()} in region `{gdc_policy.region}` is "
                                f"using wildcard action `{action}`, without any condition", glue_resource, gdc_policy))
                    elif principal and not action:
                        issues.append(
                            Issue(
                                f"The {gdc_policy.get_type()} in region `{gdc_policy.region}` is "
                                f"using principal `{self._principal_string(principal)}`,"
                                f" without any condition", glue_resource, gdc_policy))
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

    def _find_violating_actions_and_principals(self, item: GlueDataCatalogPolicy, actions: list) -> list:
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
    def check_principal(policy: PolicyStatement) -> Optional[Principal]:
        if (any(value == '*' for value in policy.principal.principal_values) or not policy.principal.principal_values)\
                or policy.principal.principal_type == PrincipalType.PUBLIC:
            return policy.principal
        else:
            return None

    @staticmethod
    def return_action_principal(item: Union[Optional[str], Optional[Principal]], item_list: List) -> Union[Optional[str], Optional[Principal]]:
        if item and item not in item_list:
            item_list.append(item)
            return item
        else:
            return None

    @staticmethod
    def _get_glue_resources(env_context: AwsEnvironmentContext, region: str):
        return [x for x in env_context.glue_data_catalog_tables if x.region == region] \
               + [x for x in env_context.glue_data_catalog_crawlers if x.region == region]

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.glue_data_catalog_policy)
