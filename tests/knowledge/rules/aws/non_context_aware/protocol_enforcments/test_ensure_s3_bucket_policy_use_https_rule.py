import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.iam.policy import S3Policy
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement, StatementCondition, StatementEffect
from cloudrail.knowledge.context.aws.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_s3_bucket_policy_use_https_rule import \
    EnsureS3BucketsPolicyUseHttpsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureS3BucketsPolicyUseHttpsRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureS3BucketsPolicyUseHttpsRule()

    def test_non_car_s3_bucket_policy_secure_transport_fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.iac_state = IacState('dummy_path', TerraformActionType.CREATE, None, True)
        policy_condition = [StatementCondition(operator='BOOL', key='aws:NotSecureTransport', values=['false'])]
        s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.DENY, ['s3:*'],
                                                                                              ['*'], Principal(PrincipalType.PUBLIC, ['*']),
                                                                                              'statement_id', policy_condition)],
                                                   'raw_doc')
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_s3_bucket_policy_secure_transport_pass(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        policy_condition = [StatementCondition(operator='BOOL', key='aws:SecureTransport', values=['false'])]
        s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.DENY, ['s3:*'],
                                                                                              ['*'], Principal(PrincipalType.PUBLIC, ['*']),
                                                                                              'statement_id', policy_condition)],
                                                   'raw_doc')
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
