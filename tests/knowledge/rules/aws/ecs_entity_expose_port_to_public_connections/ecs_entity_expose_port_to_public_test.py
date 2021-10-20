from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_security_groups_port_rule \
    import PublicAccessSecurityGroupsSshPortRule


class EcsEntityExposePortToPublicTest(AwsBaseRuleTest):

    @classmethod
    def get_rule(cls):
        return PublicAccessSecurityGroupsSshPortRule()

    @rule_test('ecs_service_expose_port', True)
    def test_ecs_service_expose_port(self, rule_result: RuleResponse):
        pass

    @rule_test('ecs_service_not_expose_any_port', False)
    def test_ecs_service_not_expose_any_port(self, rule_result: RuleResponse):
        pass

    @rule_test('ecs_schedule_task_expose_port', True)
    def test_ecs_schedule_task_expose_port(self, rule_result: RuleResponse):
        pass

    @rule_test('ecs_schedule_task_not_expose_any_port', False)
    def test_ecs_schedule_task_not_expose_any_port(self, rule_result: RuleResponse):
        pass
