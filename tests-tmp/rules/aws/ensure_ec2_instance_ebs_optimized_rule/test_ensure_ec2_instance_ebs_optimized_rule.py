from cloudrail.knowledge.rules.aws.non_context_aware.performance_optimization.ensure_ec2_instance_ebs_optimized_rule import \
    EnsureEc2InstanceEbsOptimizedRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureEc2InstanceEbsOptimizedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEc2InstanceEbsOptimizedRule()

    def test_non_optimized_ec2(self):
        self.run_test_case('non_optimized_ec2', True, always_use_cache_on_jenkins=True)

    def test_optimized_ec2(self):
        self.run_test_case('optimized_ec2', False, always_use_cache_on_jenkins=True)