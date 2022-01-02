import functools
from typing import Union, List, Dict, Tuple, Set

from cloudrail.knowledge.context.parallel.process.abstract_async_tasks_executor import AbstractAsyncTasksExecutor
from cloudrail.knowledge.utils.policy_evaluator import PolicyEvaluator, is_any_action_allowed, PolicyEvaluation
from cloudrail.knowledge.context.aws.resources.aws_client import AwsClient
from cloudrail.knowledge.context.connection import PolicyConnectionProperty
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.resources.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class AssignInboundPermissionsConnectionsTask(AbstractAsyncTasksExecutor):

    def __init__(self, aws_instances: List[Union[AwsResource, AwsClient]], iam_entities: List[IamIdentity]) -> None:
        super().__init__(self._create_inbound_permissions_connections_map)
        self.aws_instances: List[Union[AwsResource, AwsClient]] = aws_instances
        self.id_to_aws_instances_map: Dict[str, Union[AwsResource, AwsClient]] = dict()
        self.iam_entities: List[IamIdentity] = iam_entities
        self.arn_to_iam_entities_map: Dict[str, IamIdentity] = dict()
        self.arn_to_iam_entities_map_copy: Dict[str, IamIdentity] = dict()
        self.services: Set[str] = set()

    def init_args(self) -> None:

        for aws_instance in self.aws_instances:
            self.args.append(aws_instance)
            self.id_to_aws_instances_map[aws_instance.get_id()] = aws_instance
            if aws_instance.get_aws_service_type():
                self.services.add(aws_instance.get_aws_service_type())
        self.arn_to_iam_entities_map: Dict[str, IamIdentity] = {iam_entity.qualified_arn: iam_entity for iam_entity in self.iam_entities
                                                                if self.is_action_match_to_resource(iam_entity)}
        self.arn_to_iam_entities_map_copy = self._create_iam_entities_modified_copy()

    def handle_results(self, results: list) -> None:
        self.arn_to_iam_entities_map_copy.clear()
        for aws_instance_id, iam_entity_policy_eval_list in results:
            for iam_entity_and_policy_eval in iam_entity_policy_eval_list:
                iam_entity: IamIdentity = self.arn_to_iam_entities_map[iam_entity_and_policy_eval[1]]
                aws_instance: Union[AwsResource, AwsClient] = self.id_to_aws_instances_map[aws_instance_id]
                aws_instance.add_private_inbound_conn(PolicyConnectionProperty([iam_entity_and_policy_eval[0]]), iam_entity)

    def _create_inbound_permissions_connections_map(self, aws_instances: List[Union[AwsResource, AwsClient]]) \
            -> List[Tuple[str, List[Tuple[PolicyEvaluation, str]]]]:
        aws_instance_to_connections_map: Dict[str, List[Tuple[PolicyEvaluation, str]]] = {}
        for aws_instance in aws_instances:
            for iam_entity in self.arn_to_iam_entities_map_copy.values():
                policy_evaluation_result = PolicyEvaluator.evaluate_actions(iam_entity,
                                                                            aws_instance,
                                                                            [],
                                                                            iam_entity.get_policies(),
                                                                            iam_entity.permission_boundary if isinstance(iam_entity, (Role, IamUser))
                                                                            else None)

                if is_any_action_allowed(policy_evaluation_result) and \
                        (aws_instance.iam_role is None or aws_instance.iam_role != iam_entity):
                    aws_instance_id: str = aws_instance.get_id()
                    if aws_instance_id not in aws_instance_to_connections_map:
                        aws_instance_to_connections_map[aws_instance_id] = []
                    aws_instance_to_connections_map[aws_instance_id].append((policy_evaluation_result, iam_entity.qualified_arn))
        return list(aws_instance_to_connections_map.items())

    def _create_iam_entities_modified_copy(self) -> Dict[str, IamIdentity]:
        arn_to_iam_entities_map: Dict[str, IamIdentity] = dict()
        for qualified_arn, iam_entity in self.arn_to_iam_entities_map.items():
            iam_entity_copy = iam_entity.deep_copy()
            filtered_policies: List[Policy] = []
            for policy in iam_entity_copy.permissions_policies:
                filtered_statements: List[PolicyStatement] = []
                for stat in policy.statements:
                    stat.actions = self._create_filtered_actions(stat)
                    if stat.actions:
                        filtered_statements.append(stat)
                if filtered_statements:
                    policy.reset_statements()
                    policy.add_all_statements(filtered_statements)
                    filtered_policies.append(policy)
            if filtered_policies:
                iam_entity_copy.permissions_policies = filtered_policies
                arn_to_iam_entities_map[qualified_arn] = iam_entity_copy
        return arn_to_iam_entities_map

    def is_action_match_to_resource(self, iam_entity: IamIdentity) -> bool:
        for policy in iam_entity.permissions_policies:
            for stat in policy.statements:
                if self._any_statement_match(stat):
                    return True
        return False

    def _any_statement_match(self, stat: PolicyStatement) -> bool:
        for action in stat.actions:
            if self._is_action_contains_service_name(action):
                return True
        return False

    def _create_filtered_actions(self, stat: PolicyStatement) -> List[str]:
        return [action for action in stat.actions if self._is_action_contains_service_name(action)]

    @functools.lru_cache(maxsize=None)
    def _is_action_contains_service_name(self, action: str) -> bool:
        return any(self.is_action_match(action, service) for service in self.services)

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def is_action_match(action: str, service_name: str) -> bool:
        return action == "*" or f"{service_name}:" in action

    @classmethod
    def clear_cache(cls):
        cls._is_action_contains_service_name.cache_clear()
        cls.is_action_match.cache_clear()
