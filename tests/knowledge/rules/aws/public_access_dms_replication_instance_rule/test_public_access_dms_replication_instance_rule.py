from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_dms_replication_instance_rule import \
    PublicAccessDmsReplicationInstanceRule


class TestPublicAccessDmsReplicationInstanceRule(AwsBaseRuleTest):

    def get_rule(self):
        return PublicAccessDmsReplicationInstanceRule()

    @rule_test('no_public_access', False)
    def test_no_public_access(self, rule_result: RuleResponse):
        pass

    @rule_test('public_accessed_using_default_sg', False)
    def test_public_accessed_using_default_sg(self, rule_result: RuleResponse):
        pass

    @rule_test('default_vpc_public_access', False)
    def test_default_vpc_public_access(self, rule_result: RuleResponse):
        pass

    @rule_test('public_access_violating_sg', True)
    def test_public_access_violating_sg(self, rule_result: RuleResponse):
        self.assertTrue("is reachable from the internet due to subnet(s) and route table(s)" in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'DMS replication instance')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')
