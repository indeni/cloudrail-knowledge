from dataclasses import dataclass
from enum import Enum
from typing import List

from cloudrail.knowledge.context.cloneable import Cloneable
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal


class StatementEffect(Enum):
    ALLOW = "Allow"
    DENY = "Deny"


@dataclass
class StatementCondition:
    operator: str
    key: str
    values: List[str]


class PolicyStatement(Cloneable):
    """
        Attributes:
            effect: The effect of the statement (Allow / Deny).
            actions: The actions covered by the statements.
            resources: The resources covered by the statement.
            principal: The principal(s) included.
            statement_id: The id of the statement.
            condition_block: List of conditions included in the statement,
                or None if there aren't any.
            policy: The policy the statement belong to, if it does.
    """
    def __init__(self,
                 effect: StatementEffect,
                 actions: List[str],
                 resources: List[str],
                 principal: Principal,  # todo - need to support: NotPrincipal, NotAction
                 statement_id: str = '',
                 condition_block: List[StatementCondition] = None,
                 policy: 'Policy' = None):
        self.effect = effect
        self.actions = actions
        self.resources = resources
        self.principal = principal  # todo - need to support: NotPrincipal, NotAction
        self.statement_id = statement_id
        self.condition_block = condition_block or []
        self.policy = policy

    def clone(self):
        return policy_statement_clone(self)

    def to_dict(self):
        return {'effect': self.effect.value,
                'actions': self.actions,
                'resources': self.resources,
                'principal': self.principal.to_dict(),
                'statement_id': self.statement_id,
                'condition_block': self.condition_block}


def policy_statement_clone(statement: PolicyStatement) -> PolicyStatement:
    return PolicyStatement(effect=statement.effect,
                           actions=list(statement.actions),
                           resources=statement.resources,
                           principal=statement.principal,
                           statement_id=statement.statement_id,
                           condition_block=statement.condition_block,
                           policy=statement.policy)
