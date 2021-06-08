
# import unittest
#
# from cloudrail.knowledge.context.environment_context import AwsEnvironmentContext
# from cloudrail.knowledge.rules.base_rule import RuleResultType
# from cloudrail.dev_tools.rule_test_utils import create_empty_entity
#
#
# class TestIndirectPublicAccessDbRedshift(unittest.TestCase):
#     def setUp(self):
#         self.rule = IndirectPublicAccessDbRedshift()
#
#     def test_indirect_public_access_db_redshift_fail(self):
#         # Arrange
#         context = AwsEnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.FAILED, result.status)
#         self.assertEqual(1, len(result.issues))
#
#     def test_indirect_public_access_db_redshift_pass(self):
#         # Arrange
#         context = AwsEnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.SUCCESS, result.status)
#         self.assertEqual(0, len(result.issues))
