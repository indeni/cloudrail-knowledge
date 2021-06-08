from typing import List, Dict

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext


class S3AclAllowPublicAccessRule(AwsBaseRule):
    # Notice:
    # - this rule don't issue on violation on the bucket object level
    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues_list: List[Issue] = []
        for bucket in env_context.s3_buckets:
            for resource in bucket.publicly_allowing_resources:
                issues_list.append(Issue(f"~The {bucket.get_type()}~. `{bucket.get_friendly_name()}` is publicly exposed through"
                                         f" the `{resource.get_type()}` with identifier `{resource.get_friendly_name()}`.",
                                         bucket, resource))
        return issues_list

    def get_id(self) -> str:
        return "s3_acl_disallow_public_and_cross_account"

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.s3_buckets)
