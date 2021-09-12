import unittest

from cloudrail.knowledge.context.aws.resources.cloudtrail.cloudtrail import CloudTrail
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.aws.resources.account.account import Account
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudtrail_trail_exists import \
     EnsureCloudtrailTrailExists

class TestEnsureCloudtrailTrailExists(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudtrailTrailExists()

    def test_ensure_cloudtrail_trail_exists_fail(self):
        # Arrange
        context = AwsEnvironmentContext()
        account_test_fail = Account("77465564674","account", False)
        context.accounts.update(account_test_fail)

        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_ensure_cloudtrail_trail_exists_pass(self):
        # Arrange
        context = AwsEnvironmentContext()
        account_test_pass = Account("77465564674","account", False)
        context.accounts.update(account_test_pass)
        cloudtrail_trail = CloudTrail("trail",False,"any",False,"region","account",True)
        context.cloudtrail.append(cloudtrail_trail)


        # Act
        result = self.rule.run(context, {})

        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
  
