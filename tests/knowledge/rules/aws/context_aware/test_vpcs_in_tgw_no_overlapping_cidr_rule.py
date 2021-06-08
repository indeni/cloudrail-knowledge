
# import unittest
#
# from cloudrail.knowledge.context.environment_context import AwsEnvironmentContext
# from cloudrail.knowledge.rules.base_rule import RuleResultType
# from cloudrail.dev_tools.rule_test_utils import create_empty_entity
#
#
# class TestVpcsInTransitGatewayNoOverlappingCidrRule(unittest.TestCase):
#     def setUp(self):
#         self.rule = VpcsInTransitGatewayNoOverlappingCidrRule()
#
#     def test_vpcs_in_transit_gateway_no_overlapping_cidr_rule_fail(self):
#         # Arrange
#         context = AwsEnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.FAILED, result.status)
#         self.assertEqual(1, len(result.issues))
#
#     def test_vpcs_in_transit_gateway_no_overlapping_cidr_rule_pass(self):
#         # Arrange
#         context = AwsEnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.SUCCESS, result.status)
#         self.assertEqual(0, len(result.issues))
