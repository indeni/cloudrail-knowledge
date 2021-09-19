import unittest

from cloudrail.knowledge.context.aws.resources.athena.athena_database import AthenaDatabase
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_athena_database_encrypted_at_rest_rule import \
    EnsureAthenaDatabaseEncryptedAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureAthenaDatabaseEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureAthenaDatabaseEncryptedAtRestRule()

    def test_non_car_athena_database_encrypted_at_rest_fail(self):
        # Arrange
        athena_database: AthenaDatabase = create_empty_entity(AthenaDatabase)
        context = AwsEnvironmentContext(athena_databases=[athena_database])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_athena_database_encrypted_at_rest_pass(self):
        # Arrange
        athena_database: AthenaDatabase = create_empty_entity(AthenaDatabase)
        athena_database.encryption_option = 'SSE_S3'
        context = AwsEnvironmentContext(athena_databases=[athena_database])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
