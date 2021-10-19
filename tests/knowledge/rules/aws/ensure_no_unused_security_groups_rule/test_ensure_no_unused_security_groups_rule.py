from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.ensure_no_unused_security_groups_rule import EnsureNoUnusedSecurityGroups
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureNoUnusedSecurityGroups(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNoUnusedSecurityGroups()

    # RDS resources #
    @rule_test('rds/used_security_group', False)
    def test_rds_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('rds/unused_security_group_new', False)
    def test_rds_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('rds/unused_security_group_existing', True)
    def test_rds_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # Elasticache resources #
    @rule_test('elasticache/cluster_used_security_group', False)
    def test_elasticache_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('elasticache/cluster_unused_security_group_new', False)
    def test_elasticache_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('elasticache/cluster_unused_security_group_existing', True)
    def test_elasticache_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    @rule_test('elasticache/replication_group_used_security_group', False)
    def test_replication_group_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('elasticache/replication_group_unused_security_group_new', False)
    def test_replication_group_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('elasticache/replication_group_unused_security_group_existing', True)
    def test_replication_group_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # Redshift resources #
    @rule_test('redshift/used_security_group', False)
    def test_redshift_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('redshift/unused_security_group_new', False)
    def test_redshift_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('redshift/unused_security_group_existing', True)
    def test_redshift_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # EC2 resources #
    @rule_test('ec2/used_security_group', False)
    def test_ec2_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('ec2/unused_security_group_new', False)
    def test_ec2_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('ec2/unused_security_group_existing', True)
    def test_ec2_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # EKS resources #
    @rule_test('eks/used_security_group', False)
    def test_eks_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('eks/unused_security_group_new', False)
    def test_eks_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('eks/unused_security_group_existing', True)
    def test_eks_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # launch template resources #
    @rule_test('launch_template/used_security_group', False)
    def test_launch_template_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('launch_template/unused_security_group_new', False)
    def test_launch_template_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('launch_template/unused_security_group_existing', True, 2)
    def test_launch_template_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # Load balancer resources #
    @rule_test('load_balancer/used_security_group', False)
    def test_load_balancer_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('load_balancer/unused_security_group_new', False)
    def test_load_balancer_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('load_balancer/unused_security_group_existing', True)
    def test_load_balancer_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # EFS mount target resources #
    @rule_test('efs_mount_target/used_security_group', False)
    def test_efs_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('efs_mount_target/unused_security_group_new', False)
    def test_efs_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('efs_mount_target/unused_security_group_existing', True)
    def test_efs_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # ECS service resources #
    @rule_test('ecs/used_security_group', False)
    def test_ecs_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('ecs/unused_security_group_new', False)
    def test_ecs_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('ecs/unused_security_group_existing', True)
    def test_ecs_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # launch_configuration resources #
    @rule_test('launch_configuration/used_security_group', False)
    def test_launch_configuration_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('launch_configuration/unused_security_group_new', False)
    def test_launch_configuration_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('launch_configuration/unused_security_group_existing', True)
    def test_launch_configuration_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # lambda function resources #
    @rule_test('lambda_function/used_security_group', False)
    def test_lambda_function_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('lambda_function/unused_security_group_new', False)
    def test_lambda_function_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('lambda_function/unused_security_group_existing', True)
    def test_lambda_function_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # elastic_search_domain resources #
    @rule_test('elastic_search_domain/used_security_group', False)
    def test_elastic_search_domain_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('elastic_search_domain/unused_security_group_new', False)
    def test_elastic_search_domain_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('elastic_search_domain/unused_security_group_existing', True)
    def test_elastic_search_domain_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # codebuild_project resources #
    @rule_test('codebuild_project/used_security_group', False)
    def test_codebuild_project_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('codebuild_project/unused_security_group_new', False)
    def test_codebuild_project_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('codebuild_project/unused_security_group_existing', True)
    def test_codebuild_project_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # Neptune resources #
    @rule_test('neptune/used_security_group', False)
    def test_neptune_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('neptune/unused_security_group_new', False)
    def test_neptune_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('neptune/unused_security_group_existing', True)
    def test_neptune_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # kinesis_firehose resources #
    @rule_test('kinesis_firehose/used_security_group', False)
    def test_kinesis_firehose_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('kinesis_firehose/unused_security_group_new', False)
    def test_kinesis_firehose_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('kinesis_firehose/unused_security_group_existing', True)
    def test_kinesis_firehose_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # DMS resources #
    @rule_test('dms/used_security_group', False)
    def test_dms_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('dms/unused_security_group_new', False)
    def test_dms_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('dms/unused_security_group_existing', True)
    def test_dms_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # workspace_directory resources #
    @rule_test('workspace_directory/used_security_group', False)
    def test_workspace_directory_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('workspace_directory/unused_security_group_new', False)
    def test_workspace_directory_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('workspace_directory/unused_security_group_existing', True, 2)
    def test_workspace_directory_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # batch compute environment resources #
    @rule_test('batch_compute/used_security_group', False)
    def test_batch_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('batch_compute/unused_security_group_new', False)
    def test_batch_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('batch_compute/unused_security_group_existing', True)
    def test_batch_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # MQ Broker resources #
    @rule_test('mq_broker/used_security_group', False)
    def test_mq_broker_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('mq_broker/unused_security_group_new', False)
    def test_mq_broker_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('mq_broker/unused_security_group_existing', True)
    def test_mq_broker_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # Api Gateway V2 resources #
    @rule_test('api_gateway_v2/used_security_group', False)
    def test_api_gateway_v2_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('api_gateway_v2/unused_security_group_new', False)
    def test_api_gateway_v2_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('api_gateway_v2/unused_security_group_existing', True)
    def test_api_gateway_v2_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # EMR cluster resources #
    @rule_test('emr_cluster/used_security_group', False)
    def test_emr_cluster_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('emr_cluster/unused_security_group_new', False)
    def test_emr_cluster_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('emr_cluster/unused_security_group_existing', True)
    def test_emr_cluster_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # Global Accelerator resources #
    @rule_test('global_accelerator/used_security_group', False)
    def test_global_accelerator_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('global_accelerator/unused_security_group_new', False)
    def test_global_accelerator_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('global_accelerator/unused_security_group_existing', True)
    def test_global_accelerator_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # CloudHSMv2 cluster resources #
    @rule_test('cloudhsm_v2_cluster/used_security_group', False)
    def test_cloudhsm_v2_cluster_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('cloudhsm_v2_cluster/unused_security_group_new', False)
    def test_cloudhsm_v2_cluster_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('cloudhsm_v2_cluster/unused_security_group_existing', True)
    def test_cloudhsm_v2_cluster_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # Unable to run rules tests for S3Outpost resource, as not able to fully apply it - needs physical connections and server.

    # WorkLink Fleet resources #
    @rule_test('worklink_fleet/used_security_group', False)
    def test_worklink_fleet_cluster_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('worklink_fleet/unused_security_group_new', False)
    def test_worklink_fleet_cluster_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('worklink_fleet/unused_security_group_existing', True)
    def test_worklink_fleet_cluster_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # Glue Connection resources #
    @rule_test('glue_connection/used_security_group', False)
    def test_glue_connection_cluster_used_security_group(self, rule_result: RuleResponse):
        pass

    @rule_test('glue_connection/unused_security_group_new', False)
    def test_glue_connection_cluster_unused_security_group_new(self, rule_result: RuleResponse):
        pass

    @rule_test('glue_connection/unused_security_group_existing', True)
    def test_glue_connection_cluster_unused_security_group_existing(self, rule_result: RuleResponse):
        pass

    # Simple standalone security group #
    @rule_test('one_sg', True)
    def test_one_sg(self, rule_result: RuleResponse):
        pass
