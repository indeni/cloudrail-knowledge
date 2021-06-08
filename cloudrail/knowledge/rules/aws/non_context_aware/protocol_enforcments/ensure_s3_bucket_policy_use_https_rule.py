from typing import List, Dict
from cloudrail.knowledge.context.aws.iam.policy import Policy
from cloudrail.knowledge.context.aws.iam.policy_statement import StatementCondition, StatementEffect
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureS3BucketsPolicyUseHttpsRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_s3_bucket_policy_secure_transport'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for s3_bucket in env_context.s3_buckets:
            if not s3_bucket.resource_based_policy or not self._check_secure_policy(s3_bucket.resource_based_policy):
                issues.append(
                    Issue(
                        f'The {s3_bucket.get_type()} `{s3_bucket.get_friendly_name()}` '
                        f'does not have a policy with the aws:SecureTransport condition', s3_bucket, s3_bucket))
        return issues

    @staticmethod
    def _check_conditions(s3_bucket_conditions: List[StatementCondition]) -> List:
        condition_list = []
        for condition in s3_bucket_conditions:
            if condition.operator.lower() == 'bool' \
                    and condition.key == 'aws:SecureTransport' \
                    and condition.values == ['false']:
                condition_list.append(condition)
        return condition_list

    def _check_secure_policy(self, s3_bucket_policy: Policy) -> List:
        secure_statement = []
        for statement in s3_bucket_policy.statements:
            if statement.effect == StatementEffect.DENY and self._check_conditions(statement.condition_block):
                secure_statement.append(statement)
        return secure_statement

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.s3_buckets)
