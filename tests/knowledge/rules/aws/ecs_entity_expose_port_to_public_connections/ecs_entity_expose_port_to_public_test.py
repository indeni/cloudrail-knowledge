from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_security_groups_port_rule \
    import PublicAccessSecurityGroupsSshPortRule


class EcsEntityExposePortToPublicTest(AwsBaseRuleTest):

    @classmethod
    def get_rule(cls):
        return PublicAccessSecurityGroupsSshPortRule()

    def test_ecs_service_expose_port(self):
        tf_use_case_folder_name = 'ecs_service_expose_port'
        self.run_test_case(tf_use_case_folder_name, True)

    def test_ecs_service_not_expose_any_port(self):
        tf_use_case_folder_name = 'ecs_service_not_expose_any_port'
        self.run_test_case(tf_use_case_folder_name, False)

    def test_ecs_schedule_task_expose_port(self):
        tf_use_case_folder_name = 'ecs_schedule_task_expose_port'
        self.run_test_case(tf_use_case_folder_name, True)

    def test_ecs_schedule_task_not_expose_any_port(self):
        tf_use_case_folder_name = 'ecs_schedule_task_not_expose_any_port'
        self.run_test_case(tf_use_case_folder_name, False)
