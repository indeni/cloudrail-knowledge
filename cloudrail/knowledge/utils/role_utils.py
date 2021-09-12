from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import PrincipalType


def is_policy_allowing_external_assume(policy: AssumeRolePolicy):
    if policy.account:
        valid_principal_values = [policy.account, 'amazonaws.com']
    else:
        valid_principal_values = ['amazonaws.com']
    for statement in policy.statements:
        is_allowing_external_policy = \
            statement.principal.principal_values and \
            statement.principal.principal_type != PrincipalType.SERVICE and \
            any(all(valid_string not in value for valid_string in valid_principal_values) for value in statement.principal.principal_values) and \
            statement.effect == StatementEffect.ALLOW and \
            any('AssumeRole' in action for action in statement.actions)

        if is_allowing_external_policy:
            return True

    return False
