import unittest

from cloudrail.knowledge.context.aws.resources.docdb.docdb_cluster import DocumentDbCluster
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_docdb_clusters_encrypted_rule import \
    EnsureDocdbClustersEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureDocdbClustersEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureDocdbClustersEncryptedRule()

    def test_not_car_docdb_cluster_encrypted_at_rest_fail(self):
        # Arrange
        document_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        terraform_state = create_empty_entity(IacState)
        document_db_cluster.iac_state = terraform_state
        document_db_cluster.iac_state.is_new = True
        document_db_cluster.storage_encrypted = False

        context = AwsEnvironmentContext(docdb_cluster=[document_db_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest_pass(self):
        # Arrange
        document_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        terraform_state = create_empty_entity(IacState)
        document_db_cluster.iac_state = terraform_state
        document_db_cluster.iac_state.is_new = True
        document_db_cluster.storage_encrypted = True

        context = AwsEnvironmentContext(docdb_cluster=[document_db_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
