from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.alb_disallow_target_groups_http_rule import AlbDisallowHttpRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestAlbDisallowHttpBaseRule(AwsBaseRuleTest):

    def get_rule(self):
        return AlbDisallowHttpRule()

    def test_alb_use_http(self):
        self.run_test_case('alb_use_http', True, 3)

    def test_alb_not_using_http(self):
        self.run_test_case('alb_not_using_http', False)
