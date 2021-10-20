from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecr_repository_image_tags_immutable_rule import EnsureEcrRepositoryImageTagsImmutableRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureEcrRepositoryImageTagsImmutableRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcrRepositoryImageTagsImmutableRule()

    @rule_test('image_tag_immutable', False)
    def test_image_tag_immutable(self, rule_result: RuleResponse):
        pass

    @rule_test('image_tag_mutable', True)
    def test_image_tag_mutable(self, rule_result: RuleResponse):
        pass
