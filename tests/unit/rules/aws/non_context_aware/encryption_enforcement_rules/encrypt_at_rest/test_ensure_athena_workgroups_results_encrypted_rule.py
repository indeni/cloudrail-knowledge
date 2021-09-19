
import unittest

from cloudrail.knowledge.context.aws.resources.athena.athena_workgroup import AthenaWorkgroup
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_athena_workgroups_results_encrypted_rule import EnsureAthenaWorkGroupsResultsEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureAthenaWorkGroupsResultsEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureAthenaWorkGroupsResultsEncryptedRule()

    def test_non_car_athena_workgroup_query_results_encrypt_at_rest__encryption_config__missing__fail(self):
        # Arrange
        athena_workgroup: AthenaWorkgroup = create_empty_entity(AthenaWorkgroup)
        athena_workgroup.name = 'testing_workgroup'
        athena_workgroup.enforce_workgroup_config = True
        athena_workgroup.encryption_config = None

        context = AwsEnvironmentContext(athena_workgroups=[athena_workgroup])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_athena_workgroup_query_results_encrypt_at_rest__encryption_config__no_enforce_config__fail(self):
        # Arrange
        athena_workgroup: AthenaWorkgroup = create_empty_entity(AthenaWorkgroup)
        athena_workgroup.name = 'testing_workgroup'
        athena_workgroup.enforce_workgroup_config = False
        athena_workgroup.encryption_config = True

        context = AwsEnvironmentContext(athena_workgroups=[athena_workgroup])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_athena_workgroup_query_results_encrypt_at_rest_pass(self):
        # Arrange
        athena_workgroup: AthenaWorkgroup = create_empty_entity(AthenaWorkgroup)
        athena_workgroup.name = 'testing_workgroup'
        athena_workgroup.enforce_workgroup_config = True
        athena_workgroup.encryption_config = 'kms_key_arn'

        context = AwsEnvironmentContext(athena_workgroups=[athena_workgroup])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
