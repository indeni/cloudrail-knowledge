from typing import List, Dict
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import PrincipalType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class IamRoleAssumeRolePrincipalTooWide(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_iam_role_assume_role_principal_too_wide'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for role in env_context.roles:
            for statement in role.assume_role_policy.statements:
                if statement.effect == StatementEffect.ALLOW and \
                    not statement.condition_block and \
                        (statement.principal.principal_type == PrincipalType.PUBLIC or
                         (statement.principal.principal_type == PrincipalType.AWS and
                          any(value == "*" for value in statement.principal.principal_values))):
                    issues.append(Issue(f'The IAM role `{role.get_friendly_name()}` has a trust policy that allows `\'*\'` '
                                        f'principal to assume it', role, role))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.roles)
