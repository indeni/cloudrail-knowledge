from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_ec2_instance_detailed_monitoring_enabled_rule import \
    EnsureEc2InstanceDetailedMonitoringEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureEc2InstanceDetailedMonitoringEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEc2InstanceDetailedMonitoringEnabledRule()

    @rule_test('monitoring_disabled', True)
    def test_monitoring_disabled(self, rule_result: RuleResponse):
        pass

    @rule_test('monitoring_enabled', False)
    def test_monitoring_enabled(self, rule_result: RuleResponse):
        pass
