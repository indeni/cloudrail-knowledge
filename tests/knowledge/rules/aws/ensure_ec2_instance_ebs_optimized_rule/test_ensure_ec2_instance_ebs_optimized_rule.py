from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.performance_optimization.ensure_ec2_instance_ebs_optimized_rule import \
    EnsureEc2InstanceEbsOptimizedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureEc2InstanceEbsOptimizedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEc2InstanceEbsOptimizedRule()

    @rule_test('non_optimized_ec2', True)
    def test_non_optimized_ec2(self, rule_result: RuleResponse):
        pass

    @rule_test('optimized_ec2', False)
    def test_optimized_ec2(self, rule_result: RuleResponse):
        pass
