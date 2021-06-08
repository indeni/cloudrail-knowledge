from typing import Dict, List
from cloudrail.knowledge.context.aws.iam.iam_password_policy import IamPasswordPolicy
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.iam_account_pass_policy.abstract_iam_account_password_policy import \
    AbstractIamAccountPasswordPolicy
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureIamPasswordExpiration(AbstractIamAccountPasswordPolicy):

    def get_id(self) -> str:
        return "non_car_aws_iam_password_policy_expiry"

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        def policy_condition(policy: IamPasswordPolicy):
            return not policy.max_pass_age or policy.max_pass_age > 90

        issues: List[Issue] = []
        issues_data = self._get_entities_list(env_context, policy_condition)
        for policy in issues_data:
            issues.append(
                Issue(
                    f'~IAM~. The {policy.get_type()} `{policy.get_friendly_name()}`, '
                    'does not enforce password expiry on passwords older than 90 days', policy, policy))

        return issues


class EnsureIamPasswordMinimumLength(AbstractIamAccountPasswordPolicy):

    def get_id(self) -> str:
        return "non_car_aws_iam_password_policy_min_length"

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        def policy_condition(policy: IamPasswordPolicy):
            return not policy.min_pass_length or policy.min_pass_length < 14

        issues: List[Issue] = []
        issues_data = self._get_entities_list(env_context, policy_condition)
        for policy in issues_data:
            issues.append(
                Issue(
                    f'~IAM~. The {policy.get_type()} `{policy.get_friendly_name()}`, '
                    'does not restrict password length to a suitable length (14 characters)', policy, policy))
        return issues


class EnsureIamPasswordLowerCharacters(AbstractIamAccountPasswordPolicy):

    def get_id(self) -> str:
        return "non_car_aws_iam_password_policy_lower_required"

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        def policy_condition(policy: IamPasswordPolicy):
            return not policy.require_low_case_characters

        issues: List[Issue] = []
        issues_data = self._get_entities_list(env_context, policy_condition)
        for policy in issues_data:
            issues.append(
                Issue(
                    f'~IAM~. The {policy.get_type()} `{policy.get_friendly_name()}`, '
                    'does not enforce at least one lower case letter', policy, policy))
        return issues


class EnsureIamPasswordRequiresNumber(AbstractIamAccountPasswordPolicy):

    def get_id(self) -> str:
        return "non_car_aws_iam_password_policy_num_required"

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        def policy_condition(policy: IamPasswordPolicy):
            return not policy.require_numbers

        issues: List[Issue] = []
        issues_data = self._get_entities_list(env_context, policy_condition)
        for policy in issues_data:
            issues.append(
                Issue(
                    f'~IAM~. The {policy.get_type()} `{policy.get_friendly_name()}`, '
                    'does not enforce at least one number', policy, policy))
        return issues


class EnsureIamPasswordNotAllowReuse(AbstractIamAccountPasswordPolicy):

    def get_id(self) -> str:
        return "non_car_aws_iam_password_policy_password_reuse"

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        def policy_condition(policy: IamPasswordPolicy):
            return policy.password_reuse_prevention != 24

        issues: List[Issue] = []
        issues_data = self._get_entities_list(env_context, policy_condition)
        for policy in issues_data:
            issues.append(
                Issue(
                    f'~IAM~. The {policy.get_type()} `{policy.get_friendly_name()}`, '
                    'allows for password re-use', policy, policy))
        return issues


class EnsureIamPasswordRequiresSymbol(AbstractIamAccountPasswordPolicy):

    def get_id(self) -> str:
        return "non_car_aws_iam_password_policy_symbol_required"

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        def policy_condition(policy: IamPasswordPolicy):
            return not policy.require_symbols

        issues: List[Issue] = []
        issues_data = self._get_entities_list(env_context, policy_condition)
        for policy in issues_data:
            issues.append(
                Issue(
                    f'~IAM~. The {policy.get_type()} `{policy.get_friendly_name()}`, '
                    'does not enforce at least one symbol', policy, policy))
        return issues


class EnsureIamPasswordRequiresUpperCase(AbstractIamAccountPasswordPolicy):

    def get_id(self) -> str:
        return "non_car_aws_iam_password_policy_upper_required"

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        def policy_condition(policy: IamPasswordPolicy):
            return not policy.require_upper_case_characters

        issues: List[Issue] = []
        issues_data = self._get_entities_list(env_context, policy_condition)
        for policy in issues_data:
            issues.append(
                Issue(
                    f'~IAM~. The {policy.get_type()} `{policy.get_friendly_name()}`, '
                    'does not enforce at least one upper case letter', policy, policy))
        return issues
