from typing import List

from cloudrail.knowledge.context.azure.resources.i_monitor_settings import IMonitorSettings
from cloudrail.knowledge.context.azure.resources.monitor.azure_activity_log_alert import AzureMonitorActivityLogAlert
from cloudrail.knowledge.context.azure.resources.network.azure_application_security_group import AzureApplicationSecurityGroup
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface_application_security_group_association import \
    AzureNetworkInterfaceApplicationSecurityGroupAssociation
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group_rule import AzureNetworkSecurityRule
from cloudrail.knowledge.context.azure.resources.network.azure_public_ip import AzurePublicIp
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account import AzureStorageAccount
from cloudrail.knowledge.context.azure.resources.storage.azure_storage_account_network_rules import AzureStorageAccountNetworkRules, \
    BypassTrafficType, NetworkRuleDefaultAction
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_extended_auditing_policy import AzureSqlServerExtendedAuditingPolicy
from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.context.azure.resources.subscription.azure_subscription import AzureSubscription
from cloudrail.knowledge.context.azure.resources.vm.azure_virtual_machine import AzureVirtualMachine
from cloudrail.knowledge.context.azure.resources.monitor.azure_monitor_diagnostic_setting import AzureMonitorDiagnosticSetting
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_config import AzureAppServiceConfig
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.resources.network.azure_security_group_to_subnet_association import AzureSecurityGroupToSubnetAssociation
from cloudrail.knowledge.context.azure.resources.network.azure_subnet import AzureSubnet
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface_security_group_association import AzureNetworkInterfaceSecurityGroupAssociation
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import AzureNetworkInterface
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.pseudo_builder import PseudoBuilder
from cloudrail.knowledge.context.azure.resources.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.context.environment_context.business_logic.dependency_invocation import DependencyInvocation, IterFunctionData
from cloudrail.knowledge.context.environment_context.business_logic.resource_invalidator import ResourceInvalidator


class AzureRelationsAssigner(DependencyInvocation):

    def __init__(self, ctx: AzureEnvironmentContext = None):
        self.pseudo_builder = PseudoBuilder(ctx)
        self.pseudo_builder.create_vm_from_vmss(ctx.virtual_machines_scale_sets)
        function_pool = [
            ### Security Group
            IterFunctionData(self._assign_network_security_group_to_subnet, ctx.subnets,
                             (ctx.net_security_groups, ctx.subnet_network_security_group_association)),
            IterFunctionData(self._assign_network_security_group_to_network_interface, ctx.network_interfaces,
                             (ctx.net_security_groups, ctx.network_interface_network_security_group_association)),
            IterFunctionData(self._assign_monitor_diagnostic_settings, ctx.monitor_diagnostic_settings, (AliasesDict(*ctx.get_all_monitored_resources()), )),
            IterFunctionData(self._assign_network_security_group_rule_to_network_security_group, ctx.network_security_group_rules, (ctx.net_security_groups,)),
            IterFunctionData(self._assign_application_security_group_to_ip_config, ctx.network_interfaces, (ctx.app_security_groups, ctx.network_interface_application_security_group_association)),
            ### App Service
            IterFunctionData(self._assign_config_to_app_service, ctx.app_services, (ctx.app_service_configs,)),
            ### Function App
            IterFunctionData(self._assign_config_to_function_app, ctx.function_apps, (ctx.function_app_configs,)),
            ### MSQL server
            IterFunctionData(self._assign_audit_policy_to_mssql_server, ctx.sql_servers, (ctx.sql_server_extended_audit_policies,)),
            ### Storage Account
            IterFunctionData(self._assign_network_rules_to_storage_account, ctx.storage_accounts, (ctx.storage_account_network_rules,)),
            ### Virtual Machine
            IterFunctionData(self._assign_network_interface_to_virtual_machine, [vm for vm in ctx.virtual_machines if not vm.is_pseudo],
                             (ctx.network_interfaces,)),
            ### Network Interface
            IterFunctionData(self._assign_public_ip_to_ip_config, ctx.network_interfaces, (ctx.public_ips,)),
            IterFunctionData(self._assign_subnet_to_ip_config, ctx.network_interfaces, (ctx.subnets,)),
            ### Monitor Activity Log Alert
            IterFunctionData(self._assign_monitor_activity_log_alert_to_subscription, ctx.subscriptions, (ctx.monitor_activity_log_alert,)),
        ]

        super().__init__(function_pool, context=ctx)

    @staticmethod
    def _assign_network_security_group_to_subnet(subnet: AzureSubnet,
                                                 security_groups: AliasesDict[AzureNetworkSecurityGroup],
                                                 subnet_network_security_group_association: List[AzureSecurityGroupToSubnetAssociation]):
        if nsg_id := next((ast.network_security_group_id for ast in subnet_network_security_group_association if ast.subnet_id == subnet.get_id()), None):
            subnet.network_security_group = ResourceInvalidator.get_by_id(security_groups, nsg_id, True, subnet)
            subnet.network_security_group.subnets.append(subnet)

    @staticmethod
    def _assign_network_security_group_to_network_interface(network_interface: AzureNetworkInterface,
                                                            security_groups: AliasesDict[AzureNetworkSecurityGroup],
                                                            network_interface_network_security_group_association: List[AzureNetworkInterfaceSecurityGroupAssociation]):
        if nsg_id := next((ast.network_security_group_id for ast in network_interface_network_security_group_association
                        if ast.network_interface_id == network_interface.get_id()), network_interface.network_security_group_id):
            network_interface.network_security_group = ResourceInvalidator.get_by_id(security_groups, nsg_id, True, network_interface)
            network_interface.network_security_group.network_interfaces.append(network_interface)

    @staticmethod
    def _assign_config_to_app_service(app_service: AzureAppService, app_service_configs: AliasesDict[AzureAppServiceConfig]):
        app_service_config = ResourceInvalidator.get_by_logic(
            lambda: next((app_service_config for app_service_config in app_service_configs if app_service.name == app_service_config.name), None),
            False
        )
        app_service.app_service_config = app_service_config

    @staticmethod
    def _assign_config_to_function_app(function_app: AzureFunctionApp, app_service_configs: AliasesDict[AzureAppServiceConfig]):
        app_service_config = ResourceInvalidator.get_by_logic(
            lambda: next((app_service_config for app_service_config in app_service_configs if function_app.name == app_service_config.name), None),
            False
        )
        function_app.app_service_config = app_service_config

    @staticmethod
    def _assign_network_rules_to_storage_account(storage_account: AzureStorageAccount, storage_account_network_rules: AliasesDict[AzureStorageAccountNetworkRules]):
        def get_network_rules():
            network_rules = next((rules for rules in storage_account_network_rules if rules.storage_name == storage_account.storage_name), None)
            if network_rules is None:
                network_rules = AzureStorageAccountNetworkRules(storage_account.storage_name, NetworkRuleDefaultAction.ALLOW, [], [BypassTrafficType.AZURESERVICES])
            return network_rules
        if storage_account.network_rules is None:
            storage_account.network_rules = ResourceInvalidator.get_by_logic(get_network_rules, False)

    @staticmethod
    def _assign_audit_policy_to_mssql_server(mssql_server: AzureSqlServer, audit_policies: AliasesDict[AzureSqlServerExtendedAuditingPolicy]):
        if mssql_server.extended_auditing_policy is None:
            def get_audit_policy():
                audit_policy = next((audit_policy for audit_policy in audit_policies if audit_policy.server_id == mssql_server.get_id()), None)
                if audit_policy is None:
                    audit_policy = AzureSqlServerExtendedAuditingPolicy(mssql_server.get_id(), 0, False)
                return audit_policy
            mssql_server.extended_auditing_policy = ResourceInvalidator.get_by_logic(get_audit_policy, False)

    @staticmethod
    def _assign_monitor_diagnostic_settings(monitor_diagnostic_setting: AzureMonitorDiagnosticSetting,
                                            target_resources_map: AliasesDict[IMonitorSettings]):
        if target_resource := ResourceInvalidator.get_by_id(target_resources_map, monitor_diagnostic_setting.target_resource_id, False, case_sensitive=False):
            target_resource.get_monitor_settings().append(monitor_diagnostic_setting)

    @staticmethod
    def _assign_network_interface_to_virtual_machine(virtual_machine: AzureVirtualMachine, network_interfaces: AliasesDict[AzureNetworkInterface]):
        for nic_id in virtual_machine.network_interface_ids:
            virtual_machine.network_interfaces.append(ResourceInvalidator.get_by_id(network_interfaces, nic_id, True, virtual_machine))

    @staticmethod
    def _assign_public_ip_to_ip_config(network_interface: AzureNetworkInterface, public_ips: AliasesDict[AzurePublicIp]):
        for ip_config in network_interface.ip_configurations:
            if ip_config.public_ip_id:
                ip_config.public_ip = ResourceInvalidator.get_by_id(public_ips, ip_config.public_ip_id, True, network_interface)

    @staticmethod
    def _assign_subnet_to_ip_config(network_interface: AzureNetworkInterface, subnets: AliasesDict[AzureSubnet]):
        for ip_config in network_interface.ip_configurations:
            ip_config.subnet = ResourceInvalidator.get_by_id(subnets, ip_config.subnet_id, True, network_interface)

    @staticmethod
    def _assign_network_security_group_rule_to_network_security_group(nsg_rule: AzureNetworkSecurityRule, nsgs: AliasesDict[AzureNetworkSecurityGroup]):
        nsg = ResourceInvalidator.get_by_logic(
            lambda: next((nsg for nsg in nsgs if nsg.resource_group_name == nsg_rule.resource_group_name and nsg.name == nsg_rule.network_security_group_name), None),
            True,
            nsg_rule,
            'Could not associate rule to Network Security Group')

        nsg.network_security_rules.append(nsg_rule)

    @staticmethod
    def _assign_application_security_group_to_ip_config(network_interface: AzureNetworkInterface, asgs: AliasesDict[AzureApplicationSecurityGroup],
                                                        asg_to_nic_associations: AliasesDict[AzureNetworkInterfaceApplicationSecurityGroupAssociation]):
        asgs_to_attach = []

        associations = [ast for ast in asg_to_nic_associations if ast.network_interface_id == network_interface.get_id()]

        for association in associations:
            asg = ResourceInvalidator.get_by_id(asgs, association.application_security_group_id, True, network_interface)
            asgs_to_attach.append(asg)

        for ip_config in network_interface.ip_configurations:
            ip_config.application_security_groups.extend(asgs_to_attach)
            for asg_id in ip_config.application_security_groups_ids:
                asg = ResourceInvalidator.get_by_id(asgs, asg_id, True, network_interface)
                ip_config.application_security_groups.append(asg)

    @staticmethod
    def _assign_monitor_activity_log_alert_to_subscription(subscription: AzureSubscription, monitor_activity_log_alert: AliasesDict[AzureMonitorActivityLogAlert]):
        subscription.monitor_activity_alert_log_list = ResourceInvalidator.get_by_logic(
            lambda: [monitor for monitor in monitor_activity_log_alert if subscription.get_id() in monitor.scopes],
            False)
