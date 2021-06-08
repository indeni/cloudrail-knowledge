from typing import Dict, List, Set

from cloudrail.knowledge.context.aws.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.iam.policy import Policy
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils.action_utils import is_combo_escalation_permissions_match, attribute_match, LAMBDA_UPDATE_ACTION, EC2_RUN_INSTANCE_ACTION, \
    LAMBDA_INVOKE_FUNCTION_ACTION, LAMBDA_CREATE_EVENT_ACTION


class IamPrivilegeEscalationPolicyRule(AwsBaseRule):
    EVIDENCE_TEMPLATE: str = "~`{}`~. is applied to `{}`. {}{}"

    def __init__(self) -> None:
        super().__init__()
        self.issues_list: List[Issue] = []

    def get_id(self) -> str:
        return "iam_priv_escalation_policy"

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        for iam_entity in env_context.get_all_iam_entities():
            self._add_issues_by_iam_entity(iam_entity)
        return self.issues_list

    def _add_issues_by_iam_entity(self, iam_entity: IamIdentity):
        if iam_entity.policy_to_escalation_actions_map:
            all_policies_esc_actions: Set[str] = {esc_action for esc_actions in iam_entity.policy_to_escalation_actions_map.values()
                                                  for esc_action in esc_actions}
            uuid_to_policy_map: Dict[str, Policy] = {policy.uuid: policy for policy in iam_entity.permissions_policies}
            if is_combo_escalation_permissions_match(all_policies_esc_actions):
                policies: List[Policy] = [uuid_to_policy_map[policy_uuid] for policy_uuid in iam_entity.policy_to_escalation_actions_map.keys()]
                self._handle_issues(iam_entity, policies, all_policies_esc_actions)

    def _handle_issues(self, iam_entity: IamIdentity, policies: List[Policy], esc_action_list: Set[str]):
        specific_evidence: str = self._get_evidence_str(esc_action_list)
        multiple_policies_section: str = self._get_multiple_policies_evidence_section(policies)
        policy: Policy = policies[0]
        if multiple_policies_section:
            specific_evidence = ' ' + specific_evidence
        evidence: str = self.EVIDENCE_TEMPLATE.format(
            policy.get_friendly_name(), iam_entity.get_arn(), multiple_policies_section, specific_evidence)
        if policy.is_managed_by_iac:
            self.issues_list.append(Issue(evidence, policy, policy))
        else:
            self.issues_list.append(Issue(evidence, iam_entity, iam_entity))

    @staticmethod
    def _get_multiple_policies_evidence_section(policies: List[Policy]) -> str:
        multiple_policies_section: str = ""
        if len(policies) > 1:
            multiple_policies_section = "in conjunction with " + \
                                        ', '.join([f"`{policy.get_friendly_name()}`" for policy in policies])
        return multiple_policies_section

    @classmethod
    def _get_evidence_str(cls, esc_action_list: Set[str]):
        if cls._is_specific_evidence(esc_action_list, LAMBDA_UPDATE_ACTION):
            return "`lambda:UpdateFunctionCode` allows a hacker to run their code under the lambda permission"
        elif cls._is_specific_evidence(esc_action_list, EC2_RUN_INSTANCE_ACTION):
            return "`iam:PassRole` and `ec2:RunInstances` allows a hacker to run an EC2 instance with a role they choose"
        elif cls._is_specific_evidence(esc_action_list, LAMBDA_INVOKE_FUNCTION_ACTION) or \
                cls._is_specific_evidence(esc_action_list, LAMBDA_CREATE_EVENT_ACTION):
            return f"{str(esc_action_list)} allows a hacker to trigger a Lambda function with a role they choose"
        else:
            return f"granting the problematic permissions `{str(esc_action_list)}` which can allow for privilege escalation"

    @staticmethod
    def _is_specific_evidence(esc_action_list: Set[str], action: str):
        return "*" not in esc_action_list and any(attribute_match(esc_action, action)
                                                  for esc_action in esc_action_list)

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.get_all_iam_entities())
