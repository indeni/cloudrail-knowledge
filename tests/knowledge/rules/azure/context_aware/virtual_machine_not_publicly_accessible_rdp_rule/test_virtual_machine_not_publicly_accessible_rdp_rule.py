from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.context_aware.not_publicly_accessible_rule import VirtualMachineNotPubliclyAccessibleRdpRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestVirtualMachineNotPubliclyAccessibleRdpRule(AzureBaseRuleTest):

    def get_rule(self):
        return VirtualMachineNotPubliclyAccessibleRdpRule()

    ### SHOULD ALERTT ###

    @rule_test('should_alert/vm_public_rdp_pip_opened_001', should_alert=True)
    def test_vm_public_rdp_pip_opened_001(self, rule_result: RuleResponse):
        """
        pip attached, no nsg - port is exposed
        """
        pass

    @rule_test('should_alert/vm_public_rdp_pip_opened_002', should_alert=True)
    def test_vm_public_rdp_pip_opened_002(self, rule_result: RuleResponse):
        """
        pip attached, nsg attached to nic with Allow rule - port is exposed
        """
        pass

    @rule_test('should_alert/vm_public_rdp_pip_opened_003', should_alert=True)
    def test_vm_public_rdp_pip_opened_003(self, rule_result: RuleResponse):
        """
        pip attached, nsg attached to nic with Allow rule, nsg attached to subnet with Allow rule - port is exposed
        """
        pass

    @rule_test('should_alert/vm_public_rdp_pip_opened_004', should_alert=True)
    def test_vm_public_rdp_pip_opened_004(self, rule_result: RuleResponse):
        """
        pip attached, nsg attached to subnet with Allow rule - port is exposed
        """
        pass

    @rule_test('should_alert/vm_public_rdp_pip_opened_005', should_alert=True)
    def test_vm_public_rdp_pip_opened_005(self, rule_result: RuleResponse):
        """
        pip attached, nsg attached to subnet, 401 rule "Allow", 402 rule "Deny", 401 has higher priority - port is exposed
        """
        pass

    @rule_test('should_alert/vm_public_rdp_pip_opened_006', should_alert=True)
    def test_vm_public_rdp_pip_opened_006(self, rule_result: RuleResponse):
        """
        pip attached, nsg attached to nic, 201 rule "Allow", 202 rule "Deny", 201 has higher priority - port is exposed
        """
        pass

    @rule_test('should_alert/vm_public_rdp_pip_opened_007', should_alert=True)
    def test_vm_public_rdp_pip_opened_007(self, rule_result: RuleResponse):
        """
        pip attached, nsg attached to nic, 201 rule "Allow", 202 rule "Deny", 201 has higher priority ;
        nsg attached to subnet, 401 rule "Allow", 402 rule "Deny", 401 has higher priority - port is exposed
        """
        pass

    @rule_test('should_alert/vm_public_rdp_pip_opened_008', should_alert=True)
    def test_vm_public_rdp_pip_opened_008(self, rule_result: RuleResponse):
        """
        pip attached, nsg attached to nic, 201 rule "Allow"
        nsg attached to subnet, 401 rule "Allow", 402 rule "Deny", 401 has higher priority - port is exposed
        """
        pass

    @rule_test('should_alert/vm_public_rdp_pip_opened_009', should_alert=True)
    def test_vm_public_rdp_pip_opened_009(self, rule_result: RuleResponse):
        """
        pip attached, nsg attached to nic with Allow rule with destination prefix Internet - port is exposed
        """
        pass

    @rule_test('should_alert/vm_public_rdp_pip_opened_020', should_alert=True)
    def test_vm_public_rdp_pip_opened_020(self, rule_result: RuleResponse):
        """
        association rule to nsg
        """
        violating_nsg_rule_address = 'azurerm_network_security_rule.nicnsgrule'
        self.assertIn(violating_nsg_rule_address, rule_result.issues[0].evidence)
        self.assertEqual(violating_nsg_rule_address, rule_result.issues[0].violating.iac_state.address)

    @rule_test('should_alert/vm_public_rdp_pip_opened_030', should_alert=True)
    def test_vm_public_rdp_pip_opened_030(self, rule_result: RuleResponse):
        """
        another azurerm_windows_virtual_machine module to create a vm
        """
        pass

    @rule_test('should_alert/vm_public_rdp_pip_opened_040', should_alert=True)
    def test_vm_public_rdp_pip_opened_040(self, rule_result: RuleResponse):
        """
        using Application security group as a destination
        """
        pass

    ### SHOULD NOT ALERT ###

    @rule_test('should_not_alert/vm_public_rdp_pip_closed_001', should_alert=False)
    def test_vm_public_rdp_pip_closed_001(self, rule_result: RuleResponse):
        """
        NSG on both subnet and NIC. no NSG rules on both
        """
        pass

    @rule_test('should_not_alert/vm_public_rdp_pip_closed_002', should_alert=False)
    def test_vm_public_rdp_pip_closed_002(self, rule_result: RuleResponse):
        """
        NSG on both subnet and NIC. Subnet's NSG allows via allow-all rule, NIC's NSG denies by having no rules
        """
        pass

    @rule_test('should_not_alert/vm_public_rdp_pip_closed_003', should_alert=False)
    def test_vm_public_rdp_pip_closed_003(self, rule_result: RuleResponse):
        """
        NSG on both subnet and NIC. NIC's NSG allows via allow-all rule, Subnet's NSG denies by having no rules
        """
        pass

    @rule_test('should_not_alert/vm_public_rdp_pip_closed_004', should_alert=False)
    def test_vm_public_rdp_pip_closed_004(self, rule_result: RuleResponse):
        """
        NSG on NIC denies all TCP connections. No NSG on subnet
        """
        pass

    @rule_test('should_not_alert/vm_public_rdp_pip_closed_005', should_alert=False)
    def test_vm_public_rdp_pip_closed_005(self, rule_result: RuleResponse):
        """
        NSG on NIC allows all, but NSG on subnet blocks
        """
        pass

    @rule_test('should_not_alert/vm_public_rdp_pip_closed_006', should_alert=False)
    def test_vm_public_rdp_pip_closed_006(self, rule_result: RuleResponse):
        """
        NSG only on subnet, which denies all TCP connections (and not allowing others)
        """
        pass

    @rule_test('should_not_alert/vm_public_rdp_pip_closed_007', should_alert=False)
    def test_vm_public_rdp_pip_closed_007(self, rule_result: RuleResponse):
        """
        NSG only on subnet, with no rules
        """
        pass

    @rule_test('should_not_alert/vm_public_rdp_pip_closed_008', should_alert=False)
    def test_vm_public_rdp_pip_closed_008(self, rule_result: RuleResponse):
        """
        NSG only on NIC, with no rules
        """
        pass
