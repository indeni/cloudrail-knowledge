from typing import Optional
from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_instance import GcpComputeInstance, GcpComputeInstanceServiceAccount
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_do_not_use_default_service_account_full_access_scope_rule import ComputeInstanceDoNotUseDefaultServiceAccountFullAccessScopeRule


class TestComputeInstanceDoNotUseDefaultServiceAccountFullAccessScopeRule(TestCase):
    def setUp(self):
        self.rule = ComputeInstanceDoNotUseDefaultServiceAccountFullAccessScopeRule()

    @parameterized.expand(
        [
            ["default_service_account_used_violating_scope", '37924132841-compute@developer.gserviceaccount.com',
             ["https://www.googleapis.com/auth/cloud-platform"], True],
            ["no_service_account_violating_scope", None, ["cloud-platform"], True],
            ["custom_service_account_no_scope", 'non-default-svc-001@dev-for-tests.iam.gserviceaccount.com', [], False],
        ]
    )

    def test_compute_instance_default_service_account_usage(self, unused_name: str, email: Optional[str], scopes: list, should_alert: bool):
        # Arrange
        compute_instance = create_empty_entity(GcpComputeInstance)
        service_account = create_empty_entity(GcpComputeInstanceServiceAccount)
        service_account.email = email
        service_account.scopes = scopes
        compute_instance.service_account = service_account
        context = GcpEnvironmentContext(compute_instances=[compute_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
