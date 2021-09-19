import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.glue.glue_data_catalog_policy import GlueDataCatalogPolicy
from cloudrail.knowledge.context.aws.resources.glue.glue_data_catalog_table import GlueDataCatalogTable
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_glue_data_catalog_policy_not_use_wildcard_rule import \
    EnsureGlueDataCatalogPolicyNotUseWildcard
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureGlueDataCatalogPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureGlueDataCatalogPolicyNotUseWildcard()

    def test_non_car_aws_glue_data_catalog_policy_wildcard_fail(self):
        # Arrange
        gdc = GlueDataCatalogPolicy([PolicyStatement(StatementEffect.ALLOW, ['glue:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                    None,
                                    None,
                                    'us-east-1')
        gdc_table: GlueDataCatalogTable = create_empty_entity(GlueDataCatalogTable)
        gdc_table.region = 'us-east-1'
        context = AwsEnvironmentContext(glue_data_catalog_policy=[gdc], glue_data_catalog_tables=[gdc_table])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `glue:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_glue_data_catalog_policy_wildcard__only_effected_principal__fail(self):
        # Arrange
        gdc = GlueDataCatalogPolicy([PolicyStatement(StatementEffect.ALLOW, ['glue:GetDataCatalogEncryptionSettings'],
                                                     ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                    None,
                                    None,
                                    'us-east-1')
        gdc_table: GlueDataCatalogTable = create_empty_entity(GlueDataCatalogTable)
        gdc_table.region = 'us-east-1'
        context = AwsEnvironmentContext(glue_data_catalog_policy=[gdc], glue_data_catalog_tables=[gdc_table])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("in region `us-east-1` is using principal `AWS: *`" in result.issues[0].evidence)

    def test_non_car_aws_glue_data_catalog_policy_wildcard__only_effected_action__fail(self):
        # Arrange
        gdc = GlueDataCatalogPolicy([PolicyStatement(StatementEffect.ALLOW, ['glue:*'],
                                                     ['*'], Principal(PrincipalType.AWS, ["arn:aws:iam::123456789012:root"]))],
                                    None,
                                    None,
                                    'us-east-1')
        gdc_table: GlueDataCatalogTable = create_empty_entity(GlueDataCatalogTable)
        gdc_table.region = 'us-east-1'
        context = AwsEnvironmentContext(glue_data_catalog_policy=[gdc], glue_data_catalog_tables=[gdc_table])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("in region `us-east-1` is using wildcard action `glue:*`, without" in result.issues[0].evidence)

    def test_non_car_aws_glue_data_catalog_policy_wildcard_pass(self):
        # Arrange
        gdc = GlueDataCatalogPolicy([PolicyStatement(StatementEffect.ALLOW, ['glue:GetDataCatalogEncryptionSettings'],
                                                     ['*'], Principal(PrincipalType.AWS, ["arn:aws:iam::123456789012:root"]))],
                                    None,
                                    None,
                                    'us-east-1')
        gdc_table: GlueDataCatalogTable = create_empty_entity(GlueDataCatalogTable)
        gdc_table.region = 'us-east-1'
        context = AwsEnvironmentContext(glue_data_catalog_policy=[gdc], glue_data_catalog_tables=[gdc_table])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
