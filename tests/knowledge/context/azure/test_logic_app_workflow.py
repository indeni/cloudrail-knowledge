from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.azure_context_test import AzureContextTest
from tests.knowledge.context.test_context_annotation import context


class TestLogicAppWorkflow(AzureContextTest):

    def get_component(self):
        return "logic_app_workflow"

    @context(module_path="basic")
    def test_basic(self, ctx: AzureEnvironmentContext):
        la_workflow = next((workflow for workflow in ctx.logic_app_workflows if workflow.name == 'cr3686-workflow'), None)
        self.assertIsNotNone(la_workflow)
        self.assertTrue(la_workflow.enabled)
        self.assertEqual(len(la_workflow.access_control_config_list), 1)
        acl = next((acl for acl in la_workflow.access_control_config_list
                    if acl.actions.allowed_caller_ip_address_range == ["10.10.0.2/32"]), None)
        self.assertEqual(acl.triggers.allowed_caller_ip_address_range, ["10.10.0.2/32"])
        self.assertEqual(acl.contents.allowed_caller_ip_address_range, ["10.10.0.2/32"])
        self.assertEqual(acl.workflow_management_list.allowed_caller_ip_address_range, ["10.10.0.2/32"])
        self.assertEqual(la_workflow.workflow_schema,
                         'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#')
        self.assertEqual(la_workflow.workflow_version, '1.0.0.0')
        self.assertEqual(la_workflow.workflow_parameters, {'b': {'type': 'Bool'}})
        self.assertEqual(la_workflow.parameters, {'b': True})
        if la_workflow.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(la_workflow.logic_app_integration_account_id,
                             '/subscriptions/230613d8-3b34-4790-b650-36f31045f19a/resourceGroups/cr3686-RG/providers/Microsoft.Logic/integrationAccounts/cr3686-ia')
        elif la_workflow.origin == EntityOrigin.TERRAFORM:
            self.assertEqual(la_workflow.logic_app_integration_account_id, 'azurerm_logic_app_integration_account.example.id')
