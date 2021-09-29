import functools
from typing import List, Dict, Set, Tuple
from cloudrail.knowledge.context.parallel.process.abstract_async_tasks_executor import AbstractAsyncTasksExecutor
from cloudrail.knowledge.utils.policy_evaluator import PolicyEvaluator
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.utils.action_utils import parse_service_name, SERVICE_TO_ESC_ACTIONS_LIST, ACTIONS_EXCLUDE_LIST, LAMBDA_UPDATE_ACTION, attribute_match


class CreateIamEntityToEscActionsMapTask(AbstractAsyncTasksExecutor):
    def __init__(self, iam_entities: List[IamIdentity]) -> None:
        super().__init__(function=self.create_iam_entity_to_actions_map)
        self._iam_entities: List[IamIdentity] = iam_entities
        self.iam_entity_to_actions_map: Dict[str, Dict[str, Set[str]]] = dict()

    def init_args(self) -> None:
        self.args.extend(self._iam_entities)

    def handle_results(self, results) -> None:
        iam_entity_to_actions_map: Dict[str, Dict[str, Set[str]]] = dict()
        for iam_entity_qualified_arn, actions_tuple in results:
            if iam_entity_qualified_arn not in iam_entity_to_actions_map:
                iam_entity_to_actions_map[iam_entity_qualified_arn] = {actions_tuple[0]: actions_tuple[1]}
            else:
                iam_entity_to_actions_map[iam_entity_qualified_arn].update({actions_tuple[0]: actions_tuple[1]})
        self.iam_entity_to_actions_map.update(iam_entity_to_actions_map)

    @classmethod
    def create_iam_entity_to_actions_map(cls, iam_entities: List[IamIdentity]) -> List[Tuple[str, Tuple[str, Set[str]]]]:
        iam_entity_to_actions_map: Dict[str, Dict[str, Set[str]]] = dict()
        for iam_entity in iam_entities:
            iam_entity_to_actions_map[iam_entity.qualified_arn] = dict()
            allowed_statements: List[PolicyStatement] = cls.evaluate_and_get_all_allow_statements(iam_entity)
            for statement, esc_actions in cls._search_for_escalation_permissions(iam_entity, allowed_statements).items():
                if statement.policy.uuid not in iam_entity_to_actions_map[iam_entity.qualified_arn]:
                    iam_entity_to_actions_map[iam_entity.qualified_arn][statement.policy.uuid] = set()
                iam_entity_to_actions_map[iam_entity.qualified_arn][statement.policy.uuid].update(esc_actions)
            if not iam_entity_to_actions_map[iam_entity.qualified_arn]:
                del iam_entity_to_actions_map[iam_entity.qualified_arn]
        result = []
        for iam_entity_arn, dict1 in iam_entity_to_actions_map.items():
            for policy_uuid, actions in dict1.items():
                result.append((iam_entity_arn, (policy_uuid, actions)))
        return result

    @classmethod
    def evaluate_and_get_all_allow_statements(cls, iam_identity: IamIdentity) -> List[PolicyStatement]:
        all_statements_by_effect_map: Dict[StatementEffect, List[PolicyStatement]] = cls.get_all_policies_statements_by_effect(iam_identity)
        return PolicyEvaluator.evaluate_and_get_all_allow_statements(all_statements_by_effect_map)

    @classmethod
    def get_all_policies_statements_by_effect(cls, iam_identity: IamIdentity) -> Dict[StatementEffect, List[PolicyStatement]]:
        statements_by_effect_map: Dict[StatementEffect, List[PolicyStatement]] = {StatementEffect.ALLOW: [], StatementEffect.DENY: []}
        for policy in iam_identity.permissions_policies:
            stat_map: Dict[StatementEffect, List[PolicyStatement]] = policy.get_statements_by_effect()
            statements_by_effect_map[StatementEffect.ALLOW].extend(stat_map[StatementEffect.ALLOW])
            statements_by_effect_map[StatementEffect.DENY].extend(stat_map[StatementEffect.DENY])
        return statements_by_effect_map

    @classmethod
    def _search_for_escalation_permissions(cls, iam_entity: IamIdentity, statements_list: List[PolicyStatement]) \
            -> Dict[PolicyStatement, Set[str]]:
        escalation_permissions_map: Dict[PolicyStatement, Set[str]] = {}
        for statement in statements_list:
            escalation_permissions_map[statement] = set()
            for action in statement.actions:
                for action_esc in cls.get_esc_actions(action):
                    if attribute_match(action, action_esc):
                        if not cls.is_action_excluded(iam_entity, statement, action):
                            escalation_permissions_map[statement].add(action)
                            break
            if not escalation_permissions_map[statement]:
                del escalation_permissions_map[statement]
        return escalation_permissions_map

    @classmethod
    @functools.lru_cache(maxsize=None)
    def get_esc_actions(cls, action: str) -> List[str]:
        action_prefix: str = parse_service_name(action)
        return SERVICE_TO_ESC_ACTIONS_LIST.get(action_prefix, [])

    @classmethod
    def is_action_excluded(cls, iam_entity: IamIdentity, statement: PolicyStatement, action: str) -> bool:
        if action != "*" and any(attribute_match(action, exclude_action)
                                 for exclude_action in ACTIONS_EXCLUDE_LIST) and \
                len(statement.resources) == 1:
            if attribute_match(action, LAMBDA_UPDATE_ACTION):
                return statement.resources[0] == "*"  # todo - compare lambda vs role permissions will do after CR-1014
            else:
                return PolicyEvaluator.equals_resources(statement.resources[0], iam_entity.get_arn())
        return False
