from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_in_transit\
    .ensure_ecs_task_definition_created_with_efs_encrypt_in_transit_rule import \
    EnsureEcsTaskDefinitionCreatedWithEfsEncryptInTransitRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureEcsTaskDefinitionCreatedWithEfsEncryptInTransitRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureEcsTaskDefinitionCreatedWithEfsEncryptInTransitRule()

    def test_task_definition_encrypted_in_transit(self):
        self.run_test_case('task_definition_encrypted_in_transit', False)

    def test_task_definition_not_encrypted_in_transit(self):
        self.run_test_case('task_definition_not_encrypted_in_transit', True)

    def test_task_definition_multiple_volumes(self):
        self.run_test_case('task_definition_multiple_volumes', True)
