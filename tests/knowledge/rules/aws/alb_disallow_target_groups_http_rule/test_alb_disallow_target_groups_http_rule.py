from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.alb_disallow_target_groups_http_rule import AlbDisallowHttpRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestAlbDisallowHttpBaseRule(AwsBaseRuleTest):

    def get_rule(self):
        return AlbDisallowHttpRule()

    @rule_test('alb_use_http', True, 3)
    def test_alb_use_http(self, rule_result: RuleResponse):
        pass

    @rule_test('alb_not_using_http', False)
    def test_alb_not_using_http(self, rule_result: RuleResponse):
        pass
