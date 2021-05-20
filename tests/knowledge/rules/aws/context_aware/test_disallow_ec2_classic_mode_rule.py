import unittest

from cloudrail.knowledge.context.aws.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.context_aware.disallow_ec2_classic_mode_rule import DisallowEc2ClassicModeRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestDisallowEc2ClassicModeRule(unittest.TestCase):
    def setUp(self):
        self.rule = DisallowEc2ClassicModeRule()

    def test_disallow_ec2_classic_mode_rule_fail(self):
        # Arrange
        redshift_cluster = create_empty_entity(RedshiftCluster)
        redshift_cluster.subnet_group_name = None
        context = EnvironmentContext(redshift_clusters=[redshift_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(redshift_cluster, result.issues[0].exposed)
        self.assertEqual(redshift_cluster, result.issues[0].violating)

    def test_disallow_ec2_classic_mode_rule_pass(self):
        # Arrange
        redshift_cluster = create_empty_entity(RedshiftCluster)
        redshift_cluster.subnet_group_name = 'my-group'
        context = EnvironmentContext(redshift_clusters=[redshift_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
