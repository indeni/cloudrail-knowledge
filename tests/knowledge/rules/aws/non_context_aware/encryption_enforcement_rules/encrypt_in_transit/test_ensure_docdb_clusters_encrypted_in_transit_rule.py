import unittest
from typing import List

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.docdb.docdb_cluster import DocumentDbCluster
from cloudrail.knowledge.context.aws.docdb.docdb_cluster_parameter import DocDbClusterParameter
from cloudrail.knowledge.context.aws.docdb.docdb_cluster_parameter_group import DocDbClusterParameterGroup
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_in_transit.ensure_docdb_clusters_encrypted_in_transit_rule import EnsureDocdbClustersEncryptedInTransitRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureDocdbClustersEncryptedInTransitRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureDocdbClustersEncryptedInTransitRule()

    def test_not_car_docdb_cluster_encrypted_in_transit_fail(self):
        # Arrange
        doc_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        doc_db_cluster.terraform_state = TerraformState(address='address',
                                                        action=TerraformActionType.CREATE,
                                                        resource_metadata=None,
                                                        is_new=True)
        docdb_cluster_parameter_group: DocDbClusterParameterGroup = create_empty_entity(DocDbClusterParameterGroup)
        docdb_cluster_parameter_group_params: List[DocDbClusterParameter] = [create_empty_entity(DocDbClusterParameter)]
        docdb_cluster_parameter_group.parameters = docdb_cluster_parameter_group_params
        doc_db_cluster.parameter_group_name = 'param_group_name'
        docdb_cluster_parameter_group.group_name = 'param_group_name'
        docdb_cluster_parameter_group.parameters[0].parameter_name = 'tls'
        docdb_cluster_parameter_group.parameters[0].parameter_value = 'disabled'
        context = EnvironmentContext(docdb_cluster=[doc_db_cluster], docdb_cluster_parameter_groups=[docdb_cluster_parameter_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_in_transit_pass(self):
        # Arrange
        doc_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        doc_db_cluster.terraform_state = TerraformState(address='address',
                                                        action=TerraformActionType.CREATE,
                                                        resource_metadata=None,
                                                        is_new=True)
        docdb_cluster_parameter_group: DocDbClusterParameterGroup = create_empty_entity(DocDbClusterParameterGroup)
        docdb_cluster_parameter_group_params: List[DocDbClusterParameter] = [create_empty_entity(DocDbClusterParameter)]
        docdb_cluster_parameter_group.parameters = docdb_cluster_parameter_group_params
        doc_db_cluster.parameter_group_name = 'param_group_name'
        docdb_cluster_parameter_group.group_name = 'param_group_name'
        docdb_cluster_parameter_group.parameters[0].parameter_name = 'tls'
        docdb_cluster_parameter_group.parameters[0].parameter_value = 'enabled'
        context = EnvironmentContext(docdb_cluster=[doc_db_cluster], docdb_cluster_parameter_groups=[docdb_cluster_parameter_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_in_transit__not_new__pass(self):
        # Arrange
        doc_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        doc_db_cluster.terraform_state = TerraformState(address='address',
                                                        action=TerraformActionType.CREATE,
                                                        resource_metadata=None,
                                                        is_new=False)
        docdb_cluster_parameter_group: DocDbClusterParameterGroup = create_empty_entity(DocDbClusterParameterGroup)
        docdb_cluster_parameter_group_params: List[DocDbClusterParameter] = [create_empty_entity(DocDbClusterParameter)]
        docdb_cluster_parameter_group.parameters = docdb_cluster_parameter_group_params
        doc_db_cluster.parameter_group_name = 'param_group_name'
        docdb_cluster_parameter_group.group_name = 'param_group_name'
        docdb_cluster_parameter_group.parameters[0].parameter_name = 'tls'
        docdb_cluster_parameter_group.parameters[0].parameter_value = 'disabled'
        context = EnvironmentContext(docdb_cluster=[doc_db_cluster], docdb_cluster_parameter_groups=[docdb_cluster_parameter_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_in_transit__not_tls__pass(self):
        # Arrange
        doc_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        doc_db_cluster.terraform_state = TerraformState(address='address',
                                                        action=TerraformActionType.CREATE,
                                                        resource_metadata=None,
                                                        is_new=True)
        docdb_cluster_parameter_group: DocDbClusterParameterGroup = create_empty_entity(DocDbClusterParameterGroup)
        docdb_cluster_parameter_group_params: List[DocDbClusterParameter] = [create_empty_entity(DocDbClusterParameter)]
        docdb_cluster_parameter_group.parameters = docdb_cluster_parameter_group_params
        doc_db_cluster.parameter_group_name = 'param_group_name'
        docdb_cluster_parameter_group.group_name = 'param_group_name'
        docdb_cluster_parameter_group.parameters[0].parameter_name = 'SSL'
        docdb_cluster_parameter_group.parameters[0].parameter_value = 'disabled'
        context = EnvironmentContext(docdb_cluster=[doc_db_cluster], docdb_cluster_parameter_groups=[docdb_cluster_parameter_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_in_transit__not_same_name__pass(self):
        # Arrange
        doc_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        doc_db_cluster.terraform_state = TerraformState(address='address',
                                                        action=TerraformActionType.CREATE,
                                                        resource_metadata=None,
                                                        is_new=True)
        docdb_cluster_parameter_group: DocDbClusterParameterGroup = create_empty_entity(DocDbClusterParameterGroup)
        docdb_cluster_parameter_group_params: List[DocDbClusterParameter] = [create_empty_entity(DocDbClusterParameter)]
        docdb_cluster_parameter_group.parameters = docdb_cluster_parameter_group_params
        doc_db_cluster.parameter_group_name = 'param_group_name'
        docdb_cluster_parameter_group.group_name = 'param_group_name_2'
        docdb_cluster_parameter_group.parameters[0].parameter_name = 'tls'
        docdb_cluster_parameter_group.parameters[0].parameter_value = 'disabled'
        context = EnvironmentContext(docdb_cluster=[doc_db_cluster], docdb_cluster_parameter_groups=[docdb_cluster_parameter_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
