from dataclasses import dataclass, field
from typing import Dict, Set
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.utils.action_utils import is_action_fully_defined
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import PrincipalType, Principal
from cloudrail.knowledge.context.aws.resources.s3.s3_acl import GranteeTypes, S3PredefinedGroups
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket


@dataclass
class PublicAccessResults:
    principal: Principal
    resources: Set[str]
    allowed_actions: Set[str] = field(default_factory=set)
    denied_actions: Set[str] = field(default_factory=set)


class S3PublicAccessEvaluator:

    # Notice: this evaluation don't take in account bucket object acl
    ALL_AUTHENTICATED_USERS: Principal = Principal(PrincipalType.AWS, ['*'])
    PUBLIC_USERS: Principal = Principal(PrincipalType.PUBLIC, [])

    def __init__(self, s3_bucket: S3Bucket, ignore_policy_condition_block: bool = False) -> None:
        self._s3_bucket: S3Bucket = s3_bucket
        self.ignore_policy_condition_block: bool = ignore_policy_condition_block
        self._results_map: Dict[AwsResource, PublicAccessResults] = {}
        self._evaluated: bool = False

    def evaluate(self) -> Dict[AwsResource, PublicAccessResults]:
        if not (self._evaluated or self._s3_bucket.public_access_block_settings.is_restrict_public_buckets()):
            self._set_bucket_policy_results()
            self._set_acl_policy_results()
            all_denied_actions: Set[str] = set()
            for results in self._results_map.values():
                all_denied_actions.update(results.denied_actions)
            for results in self._results_map.values():
                self._filter_allowed_actions(results, all_denied_actions)
        self._evaluated = True
        return self._results_map

    def _set_acl_policy_results(self):
        if not self._s3_bucket.public_access_block_settings.is_ignore_public_acls():
            for acl in self._s3_bucket.acls:
                if acl.type == GranteeTypes.GROUP:
                    if acl.type_value == S3PredefinedGroups.AUTHENTICATED_USERS.value or \
                            acl.type_value == S3PredefinedGroups.ALL_USERS.value:
                        self._results_map[acl] = PublicAccessResults(principal=self.ALL_AUTHENTICATED_USERS,
                                                                     allowed_actions=set(acl.actions),
                                                                     resources={self._s3_bucket.get_arn()})
                else:
                    # canned acls and names: ac2 instance read: za-team, ec2 instance read/write: ec2-bundled-images
                    # TF don't support "user display name" attribute could lead to false positive
                    if not (acl.is_grantee_owner() or (acl.type == GranteeTypes.CANONICAL_USER and (acl.type_value == "za-team" or
                                                                                                    acl.type_value == "ec2-bundled-images"))):
                        self._results_map[acl] = PublicAccessResults(principal=Principal(PrincipalType.CANONICAL_USER, [acl.type_value]),
                                                                     allowed_actions=set(acl.actions),
                                                                     resources={self._s3_bucket.get_arn()})

    def _set_bucket_policy_results(self):
        if self._s3_bucket.resource_based_policy:
            for statement in self._s3_bucket.resource_based_policy.statements:
                if not self.ignore_policy_condition_block or len(statement.condition_block) == 0:
                    if statement.principal.principal_type == PrincipalType.PUBLIC or \
                            (statement.principal.principal_type == PrincipalType.AWS and
                             any(value == "*" for value in statement.principal.principal_values)) and \
                            any(res == self._s3_bucket.get_arn() for res in statement.resources):
                        principal: Principal = self.PUBLIC_USERS if statement.principal.principal_type == PrincipalType.PUBLIC \
                            else self.ALL_AUTHENTICATED_USERS
                        if statement.effect == StatementEffect.ALLOW:
                            self._results_map[self._s3_bucket.resource_based_policy] = \
                                PublicAccessResults(principal=principal,
                                                    allowed_actions=set(statement.actions),
                                                    resources={self._s3_bucket.get_arn()})
                        else:
                            self._results_map[self._s3_bucket.resource_based_policy] = \
                                PublicAccessResults(principal=principal,
                                                    denied_actions=set(statement.actions),
                                                    resources={self._s3_bucket.get_arn()})

    @staticmethod
    def _filter_allowed_actions(results: PublicAccessResults, all_denied_actions: Set[str]):
        filtered_allowed_actions: Set[str] = set()
        for allowed in results.allowed_actions:
            if not any(is_action_fully_defined(allowed, denied) for denied in all_denied_actions):
                filtered_allowed_actions.add(allowed)
        results.allowed_actions = filtered_allowed_actions

    def is_bucket_publicly_accessible(self):
        return len(self.get_all_publicly_allowed_actions()) > 0

    def get_all_publicly_allowed_actions(self,) -> Set[str]:
        self.evaluate()
        return set(action for result in self.evaluate().values() for action in result.allowed_actions
                   if result.principal.principal_type != PrincipalType.CANONICAL_USER)
