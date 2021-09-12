import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.elasticache.elasticache_replication_group import ElastiCacheReplicationGroup
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_in_transit.ensure_elasticache_replication_groups_encrypted_in_transit_rule import EnsureElasticacheReplicationGroupsEncryptedInTransitRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureElasticacheReplicationGroupsEncryptedInTransitRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureElasticacheReplicationGroupsEncryptedInTransitRule()

    def test_non_car_elasticache_replication_group_encrypt_in_transit_creating_fail(self):
        # Arrange
        elasti_cache_replication_group: ElastiCacheReplicationGroup = create_empty_entity(ElastiCacheReplicationGroup)
        elasti_cache_replication_group.iac_state = IacState(address='address', action=TerraformActionType.CREATE,
                                                            resource_metadata=None, is_new=True)
        elasti_cache_replication_group.encrypted_in_transit = False
        context = AwsEnvironmentContext(elasti_cache_replication_groups=[elasti_cache_replication_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_elasticache_replication_group_encrypt_in_transit_creating_pass(self):
        # Arrange
        elasti_cache_replication_group: ElastiCacheReplicationGroup = create_empty_entity(ElastiCacheReplicationGroup)
        elasti_cache_replication_group.iac_state = IacState(address='address', action=TerraformActionType.CREATE,
                                                            resource_metadata=None, is_new=True)
        elasti_cache_replication_group.encrypted_in_transit = True
        context = AwsEnvironmentContext(elasti_cache_replication_groups=[elasti_cache_replication_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_elasticache_replication_group_encrypt_in_transit_creating__not_new__pass(self):
        # Arrange
        elasti_cache_replication_group: ElastiCacheReplicationGroup = create_empty_entity(ElastiCacheReplicationGroup)
        elasti_cache_replication_group.iac_state = IacState(address='address', action=TerraformActionType.CREATE,
                                                            resource_metadata=None, is_new=False)
        elasti_cache_replication_group.encrypted_in_transit = False
        context = AwsEnvironmentContext(elasti_cache_replication_groups=[elasti_cache_replication_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
