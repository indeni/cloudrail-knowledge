import functools
from typing import List, Dict


from cloudrail.knowledge.context.environment_context.business_logic.connection_builder_data_holders import PrivateConnectionData
from cloudrail.knowledge.context.aws.parallel.assign_inbound_permissions_connections_task import AssignInboundPermissionsConnectionsTask
from cloudrail.knowledge.context.parallel.process.abstract_async_tasks_executor import AbstractAsyncTasksExecutor
from cloudrail.knowledge.utils.policy_evaluator import PolicyEvaluator, is_any_action_allowed, PolicyEvaluation
from cloudrail.knowledge.context.connection import PolicyConnectionProperty
from cloudrail.knowledge.context.aws.resources.iam.role import Role
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aliases_dict import AliasesDict


class AssignRolesToBucketTask(AbstractAsyncTasksExecutor):

    def __init__(self, roles: List[Role], s3_buckets: AliasesDict[S3Bucket]) -> None:
        super().__init__(self._assign_role_to_s3_connections)
        self.roles: List[Role] = roles
        self.s3_buckets: AliasesDict[S3Bucket] = s3_buckets
        self.roles_dict: Dict[str, Role] = dict()
        self.bucket_dict: Dict[str, S3Bucket] = dict()

    def init_args(self) -> None:
        filtered_roles: List[Role] = self._filter_roles_by_resource(self.roles)
        self.roles_dict = {role.qualified_arn: role for role in filtered_roles}
        self.bucket_dict = {bucket.arn: bucket for bucket in self.s3_buckets}
        if filtered_roles and self.s3_buckets:
            self.args.extend(self.s3_buckets)
        self.extra_args.append(self.roles_dict)

    def handle_results(self, results: list) -> None:
        for private_conn in results:
            role_arn: str = private_conn.source
            bucket_arn: str = private_conn.destination
            eval_results: PolicyEvaluation = private_conn.value
            origin_role: Role = self.roles_dict[role_arn]
            origin_bucket: S3Bucket = self.bucket_dict[bucket_arn]
            origin_role.policy_evaluation_result_map[bucket_arn] = eval_results
            origin_bucket.add_private_inbound_conn(PolicyConnectionProperty([eval_results]), origin_role)

    @staticmethod
    def _assign_role_to_s3_connections(s3_buckets: List[S3Bucket], roles_dict) -> List[PrivateConnectionData]:
        policy_evaluation_results: List[PrivateConnectionData] = []
        for s3_bucket in s3_buckets:
            for role in roles_dict.values():
                connection_data = _get_role_to_s3_connections(role, s3_bucket)
                if is_any_action_allowed(connection_data.value):
                    policy_evaluation_results.append(connection_data)
        return policy_evaluation_results

    @classmethod
    def _filter_roles_by_resource(cls, roles: List[Role]) -> List[Role]:
        filtered_roles: List[Role] = []
        for role in roles:
            if cls.is_action_match_to_resource(role):
                filtered_roles.append(role)
        return filtered_roles

    @classmethod
    def is_action_match_to_resource(cls, iam_entity) -> bool:
        for policy in iam_entity.permissions_policies:
            for stat in policy.statements:
                if cls._any_statement_match(stat):
                    return True
        return False

    @classmethod
    def _any_statement_match(cls, stat) -> bool:
        for action in stat.actions:
            if cls._is_action_contains_service_name(action):
                return True
        return False

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _is_action_contains_service_name(cls, action: str) -> bool:
        return cls.is_action_match(action)

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def is_action_match(action: str) -> bool:
        return action == "*" or 's3:' in action

    @staticmethod
    def _is_action_match_to_resource(role: Role, service_name: str):
        for policy in role.permissions_policies:
            for stat in policy.statements:
                for action in stat.actions:
                    if AssignInboundPermissionsConnectionsTask.is_action_match(action, service_name):
                        return True
        return False

    @classmethod
    def clear_cache(cls):
        cls.is_action_match.cache_clear()
        cls._is_action_contains_service_name.cache_clear()


def _get_role_to_s3_connections(role: Role, bucket: S3Bucket) -> PrivateConnectionData:
    policy_evaluation_result: PolicyEvaluation
    if bucket.get_arn() in role.policy_evaluation_result_map:
        policy_evaluation_result = role.policy_evaluation_result_map[bucket.get_arn()]
    else:
        policy_evaluation_result = PolicyEvaluator.evaluate_actions(role,
                                                                    bucket,
                                                                    [bucket.resource_based_policy],
                                                                    role.get_policies(),
                                                                    role.permission_boundary)

    return PrivateConnectionData(role.qualified_arn, bucket.arn, policy_evaluation_result)
