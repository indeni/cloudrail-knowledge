import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_elasticache_replication_groups_encrypted_at_rest_rule import EnsureElasticacheReplicationGroupsEncryptedAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_replication_group import ElastiCacheReplicationGroup


class TestEnsureElasticacheReplicationGroupsEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureElasticacheReplicationGroupsEncryptedAtRestRule()

    def test_non_car_elasticache_replication_group_encrypt_at_rest_creating_fail(self):
        # Arrange
        ec_rep_group: ElastiCacheReplicationGroup = create_empty_entity(ElastiCacheReplicationGroup)
        ec_rep_group.iac_state = IacState(address='address',
                                          action=TerraformActionType.CREATE,
                                          resource_metadata=None,
                                          is_new=True)
        ec_rep_group.encrypted_at_rest = False
        context = AwsEnvironmentContext(elasti_cache_replication_groups=[ec_rep_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_elasticache_replication_group_encrypt_at_rest_creating_pass(self):
        # Arrange
        ec_rep_group: ElastiCacheReplicationGroup = create_empty_entity(ElastiCacheReplicationGroup)
        ec_rep_group.iac_state = IacState(address='address',
                                          action=TerraformActionType.CREATE,
                                          resource_metadata=None,
                                          is_new=True)
        ec_rep_group.encrypted_at_rest = True
        context = AwsEnvironmentContext(elasti_cache_replication_groups=[ec_rep_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_elasticache_replication_group_encrypt_at_rest_creating__not_new__pass(self):
        # Arrange
        ec_rep_group: ElastiCacheReplicationGroup = create_empty_entity(ElastiCacheReplicationGroup)
        ec_rep_group.iac_state = IacState(address='address',
                                          action=TerraformActionType.CREATE,
                                          resource_metadata=None,
                                          is_new=False)
        ec_rep_group.encrypted_at_rest = False
        context = AwsEnvironmentContext(elasti_cache_replication_groups=[ec_rep_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
