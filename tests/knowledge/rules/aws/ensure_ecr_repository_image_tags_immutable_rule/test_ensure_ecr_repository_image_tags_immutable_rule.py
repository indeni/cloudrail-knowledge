from cloudrail.knowledge.rules.aws.non_context_aware.ensure_ecr_repository_image_tags_immutable_rule import EnsureEcrRepositoryImageTagsImmutableRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureEcrRepositoryImageTagsImmutableRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcrRepositoryImageTagsImmutableRule()

    def test_image_tag_immutable(self):
        self.run_test_case('image_tag_immutable', False)

    def test_image_tag_mutable(self):
        self.run_test_case('image_tag_mutable', True)
