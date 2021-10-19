from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_vms_and_vmss_use_managed_disks_rule import EnsureVmAndVmssUseManagedDisksRule
from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestEnsureVmAndVmssUseManagedDisksRule(AzureBaseRuleTest):
    def get_rule(self):
        return EnsureVmAndVmssUseManagedDisksRule()

    @rule_test('linux_vmss_with_data_disk', False)
    def test_linux_vmss_with_data_disk(self, rule_result: RuleResponse):
        pass

    @rule_test('no_os_managed_disk', False)
    def test_no_os_vmss_managed_disk(self, rule_result: RuleResponse):
        pass

    @rule_test('no_os_unmanaged_disk', True, 2)
    def test_no_os_vmss_unmanaged_disk(self, rule_result: RuleResponse):
        pass

    @rule_test('no_os_vm_unmanaged_disk', True)
    def test_no_os_vm_unmanaged_disk(self, rule_result: RuleResponse):
        pass


    @rule_test('no_os_vm_with_data_disks', False)
    def test_no_os_vm_with_data_disks(self, rule_result: RuleResponse):
        pass

    @rule_test('windows_vmss_data_disk', False)
    def test_windows_vmss_data_disk(self, rule_result: RuleResponse):
        pass
