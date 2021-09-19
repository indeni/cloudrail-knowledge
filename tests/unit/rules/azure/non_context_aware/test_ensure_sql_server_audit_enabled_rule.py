from unittest import TestCase

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.databases.azure_mssql_server_extended_auditing_policy import AzureSqlServerExtendedAuditingPolicy
from cloudrail.knowledge.context.azure.resources.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_sql_server_audit_enabled_rule import EnsureSqlServerAuditEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureSqlServerAuditEnabledRule(TestCase):

    def setUp(self):
        self.rule = EnsureSqlServerAuditEnabledRule()

    def test_non_car_sql_servers_auditing_enabled_fail(self):
        # Arrange
        sql_server: AzureSqlServer = create_empty_entity(AzureSqlServer)
        sql_server.server_name = 'my-sql-server'
        audit_policy: AzureSqlServerExtendedAuditingPolicy = create_empty_entity(AzureSqlServerExtendedAuditingPolicy)
        audit_policy.log_monitoring_enabled = False
        sql_server.extended_auditing_policy = audit_policy
        context = AzureEnvironmentContext(sql_servers=AliasesDict(sql_server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_sql_servers_auditing_enabled__bad_retention__fail(self):
        # Arrange
        sql_server: AzureSqlServer = create_empty_entity(AzureSqlServer)
        sql_server.server_name = 'my-sql-server'
        audit_policy: AzureSqlServerExtendedAuditingPolicy = create_empty_entity(AzureSqlServerExtendedAuditingPolicy)
        audit_policy.log_monitoring_enabled = True
        audit_policy.retention_in_days = 30
        sql_server.extended_auditing_policy = audit_policy
        context = AzureEnvironmentContext(sql_servers=AliasesDict(sql_server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_sql_servers_auditing_enabled_pass(self):
        # Arrange
        sql_server: AzureSqlServer = create_empty_entity(AzureSqlServer)
        sql_server.server_name = 'my-sql-server'
        audit_policy: AzureSqlServerExtendedAuditingPolicy = create_empty_entity(AzureSqlServerExtendedAuditingPolicy)
        audit_policy.log_monitoring_enabled = True
        audit_policy.retention_in_days = 0
        sql_server.extended_auditing_policy = audit_policy
        context = AzureEnvironmentContext(sql_servers=AliasesDict(sql_server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_sql_servers_auditing_enabled_high_retention__pass(self):
        # Arrange
        sql_server: AzureSqlServer = create_empty_entity(AzureSqlServer)
        sql_server.server_name = 'my-sql-server'
        audit_policy: AzureSqlServerExtendedAuditingPolicy = create_empty_entity(AzureSqlServerExtendedAuditingPolicy)
        audit_policy.log_monitoring_enabled = True
        audit_policy.retention_in_days = 100
        sql_server.extended_auditing_policy = audit_policy
        context = AzureEnvironmentContext(sql_servers=AliasesDict(sql_server))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
