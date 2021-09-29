import unittest

from cloudrail.dev_tools.aws_rule_test_utils import create_empty_network_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.dms.dms_replication_instance import DmsReplicationInstance
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_dms_replication_instance_rule import \
    PublicAccessDmsReplicationInstanceRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestPublicAccessDmsReplicationInstanceRule(unittest.TestCase):
    def setUp(self):
        self.rule = PublicAccessDmsReplicationInstanceRule()

    def test_public_access_dms_replication_instance_fail(self):
        # Arrange
        dms = create_empty_network_entity(DmsReplicationInstance)
        security_group = create_empty_entity(SecurityGroup)
        dms.security_group_allowing_public_access = security_group
        context = AwsEnvironmentContext(dms_replication_instances=[dms], security_groups=AliasesDict(security_group))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_public_access_dms_replication_instance_pass(self):
        # Arrange
        dms = create_empty_network_entity(DmsReplicationInstance)
        context = AwsEnvironmentContext(dms_replication_instances=[dms])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
