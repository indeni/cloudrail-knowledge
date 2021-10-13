from cloudrail.knowledge.rules.azure.context_aware.not_publicly_accessible_rule import VirtualMachineNotPubliclyAccessibleRdpRule

from test.knowledge.rules.base_rule_test import AzureBaseRuleTest


class TestVirtualMachineNotPubliclyAccessibleRdpRule(AzureBaseRuleTest):

    def get_rule(self):
        return VirtualMachineNotPubliclyAccessibleRdpRule()

    ### SHOULD ALERTT ###

    def test_vm_public_rdp_pip_opened_001(self):
        """
        pip attached, no nsg - port is exposed
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_001', should_alert=True)

    def test_vm_public_rdp_pip_opened_002(self):
        """
        pip attached, nsg attached to nic with Allow rule - port is exposed
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_002', should_alert=True)

    def test_vm_public_rdp_pip_opened_003(self):
        """
        pip attached, nsg attached to nic with Allow rule, nsg attached to subnet with Allow rule - port is exposed
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_003', should_alert=True)

    def test_vm_public_rdp_pip_opened_004(self):
        """
        pip attached, nsg attached to subnet with Allow rule - port is exposed
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_004', should_alert=True)

    def test_vm_public_rdp_pip_opened_005(self):
        """
        pip attached, nsg attached to subnet, 401 rule "Allow", 402 rule "Deny", 401 has higher priority - port is exposed
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_005', should_alert=True)

    def test_vm_public_rdp_pip_opened_006(self):
        """
        pip attached, nsg attached to nic, 201 rule "Allow", 202 rule "Deny", 201 has higher priority - port is exposed
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_006', should_alert=True)

    def test_vm_public_rdp_pip_opened_007(self):
        """
        pip attached, nsg attached to nic, 201 rule "Allow", 202 rule "Deny", 201 has higher priority ;
        nsg attached to subnet, 401 rule "Allow", 402 rule "Deny", 401 has higher priority - port is exposed
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_007', should_alert=True)

    def test_vm_public_rdp_pip_opened_008(self):
        """
        pip attached, nsg attached to nic, 201 rule "Allow"
        nsg attached to subnet, 401 rule "Allow", 402 rule "Deny", 401 has higher priority - port is exposed
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_008', should_alert=True)

    def test_vm_public_rdp_pip_opened_009(self):
        """
        pip attached, nsg attached to nic with Allow rule with destination prefix Internet - port is exposed
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_009', should_alert=True)

    def test_vm_public_rdp_pip_opened_020(self):
        """
        association rule to nsg
        """
        rule_result = self.run_test_case('should_alert/vm_public_rdp_pip_opened_020', should_alert=True)
        violating_nsg_rule_address = 'azurerm_network_security_rule.nicnsgrule'
        self.assertIn(violating_nsg_rule_address, rule_result.issues[0].evidence)
        self.assertEqual(violating_nsg_rule_address, rule_result.issues[0].violating.iac_state.address)

    def test_vm_public_rdp_pip_opened_030(self):
        """
        another azurerm_windows_virtual_machine module to create a vm
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_030', should_alert=True)

    def test_vm_public_rdp_pip_opened_040(self):
        """
        using Application security group as a destination
        """
        self.run_test_case('should_alert/vm_public_rdp_pip_opened_040', should_alert=True)

    ### SHOULD NOT ALERT ###

    def test_vm_public_rdp_pip_closed_001(self):
        """
        NSG on both subnet and NIC. no NSG rules on both
        """
        self.run_test_case('should_not_alert/vm_public_rdp_pip_closed_001', should_alert=False)

    def test_vm_public_rdp_pip_closed_002(self):
        """
        NSG on both subnet and NIC. Subnet's NSG allows via allow-all rule, NIC's NSG denies by having no rules
        """
        self.run_test_case('should_not_alert/vm_public_rdp_pip_closed_002', should_alert=False)

    def test_vm_public_rdp_pip_closed_003(self):
        """
        NSG on both subnet and NIC. NIC's NSG allows via allow-all rule, Subnet's NSG denies by having no rules
        """
        self.run_test_case('should_not_alert/vm_public_rdp_pip_closed_003', should_alert=False)

    def test_vm_public_rdp_pip_closed_004(self):
        """
        NSG on NIC denies all TCP connections. No NSG on subnet
        """
        self.run_test_case('should_not_alert/vm_public_rdp_pip_closed_004', should_alert=False)

    def test_vm_public_rdp_pip_closed_005(self):
        """
        NSG on NIC allows all, but NSG on subnet blocks
        """
        self.run_test_case('should_not_alert/vm_public_rdp_pip_closed_005', should_alert=False)

    def test_vm_public_rdp_pip_closed_006(self):
        """
        NSG only on subnet, which denies all TCP connections (and not allowing others)
        """
        self.run_test_case('should_not_alert/vm_public_rdp_pip_closed_006', should_alert=False)

    def test_vm_public_rdp_pip_closed_007(self):
        """
        NSG only on subnet, with no rules
        """
        self.run_test_case('should_not_alert/vm_public_rdp_pip_closed_007', should_alert=False)

    def test_vm_public_rdp_pip_closed_008(self):
        """
        NSG only on NIC, with no rules
        """
        self.run_test_case('should_not_alert/vm_public_rdp_pip_closed_008', should_alert=False)
