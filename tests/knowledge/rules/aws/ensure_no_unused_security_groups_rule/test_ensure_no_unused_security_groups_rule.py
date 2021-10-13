from cloudrail.knowledge.rules.aws.context_aware.ensure_no_unused_security_groups_rule import EnsureNoUnusedSecurityGroups
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureNoUnusedSecurityGroups(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureNoUnusedSecurityGroups()

    # RDS resources #
    def test_rds_used_security_group(self):
        self.run_test_case('rds/used_security_group', False)

    def test_rds_unused_security_group_new(self):
        self.run_test_case('rds/unused_security_group_new', False)

    def test_rds_unused_security_group_existing(self):
        self.run_test_case('rds/unused_security_group_existing', True)

    # Elasticache resources #
    def test_elasticache_used_security_group(self):
        self.run_test_case('elasticache/cluster_used_security_group', False)

    def test_elasticache_unused_security_group_new(self):
        self.run_test_case('elasticache/cluster_unused_security_group_new', False)

    def test_elasticache_unused_security_group_existing(self):
        self.run_test_case('elasticache/cluster_unused_security_group_existing', True)

    def test_replication_group_used_security_group(self):
        self.run_test_case('elasticache/replication_group_used_security_group', False)

    def test_replication_group_unused_security_group_new(self):
        self.run_test_case('elasticache/replication_group_unused_security_group_new', False)

    def test_replication_group_unused_security_group_existing(self):
        self.run_test_case('elasticache/replication_group_unused_security_group_existing', True)

    # Redshift resources #
    def test_redshift_used_security_group(self):
        self.run_test_case('redshift/used_security_group', False)

    def test_redshift_unused_security_group_new(self):
        self.run_test_case('redshift/unused_security_group_new', False)

    def test_redshift_unused_security_group_existing(self):
        self.run_test_case('redshift/unused_security_group_existing', True)

    # EC2 resources #
    def test_ec2_used_security_group(self):
        self.run_test_case('ec2/used_security_group', False)

    def test_ec2_unused_security_group_new(self):
        self.run_test_case('ec2/unused_security_group_new', False)

    def test_ec2_unused_security_group_existing(self):
        self.run_test_case('ec2/unused_security_group_existing', True)

    # EKS resources #
    def test_eks_used_security_group(self):
        self.run_test_case('eks/used_security_group', False)

    def test_eks_unused_security_group_new(self):
        self.run_test_case('eks/unused_security_group_new', False)

    def test_eks_unused_security_group_existing(self):
        self.run_test_case('eks/unused_security_group_existing', True)

    # launch template resources #
    def test_launch_template_used_security_group(self):
        self.run_test_case('launch_template/used_security_group', False)

    def test_launch_template_unused_security_group_new(self):
        self.run_test_case('launch_template/unused_security_group_new', False)

    def test_launch_template_unused_security_group_existing(self):
        self.run_test_case('launch_template/unused_security_group_existing', True, 2)

    # Load balancer resources #
    def test_load_balancer_used_security_group(self):
        self.run_test_case('load_balancer/used_security_group', False)

    def test_load_balancer_unused_security_group_new(self):
        self.run_test_case('load_balancer/unused_security_group_new', False)

    def test_load_balancer_unused_security_group_existing(self):
        self.run_test_case('load_balancer/unused_security_group_existing', True)

    # EFS mount target resources #
    def test_efs_used_security_group(self):
        self.run_test_case('efs_mount_target/used_security_group', False)

    def test_efs_unused_security_group_new(self):
        self.run_test_case('efs_mount_target/unused_security_group_new', False)

    def test_efs_unused_security_group_existing(self):
        self.run_test_case('efs_mount_target/unused_security_group_existing', True)

    # ECS service resources #
    def test_ecs_used_security_group(self):
        self.run_test_case('ecs/used_security_group', False)

    def test_ecs_unused_security_group_new(self):
        self.run_test_case('ecs/unused_security_group_new', False)

    def test_ecs_unused_security_group_existing(self):
        self.run_test_case('ecs/unused_security_group_existing', True)

    # launch_configuration resources #
    def test_launch_configuration_used_security_group(self):
        self.run_test_case('launch_configuration/used_security_group', False)

    def test_launch_configuration_unused_security_group_new(self):
        self.run_test_case('launch_configuration/unused_security_group_new', False)

    def test_launch_configuration_unused_security_group_existing(self):
        self.run_test_case('launch_configuration/unused_security_group_existing', True)

    # lambda function resources #
    def test_lambda_function_used_security_group(self):
        self.run_test_case('lambda_function/used_security_group', False)

    def test_lambda_function_unused_security_group_new(self):
        self.run_test_case('lambda_function/unused_security_group_new', False)

    def test_lambda_function_unused_security_group_existing(self):
        self.run_test_case('lambda_function/unused_security_group_existing', True)

    # elastic_search_domain resources #
    def test_elastic_search_domain_used_security_group(self):
        self.run_test_case('elastic_search_domain/used_security_group', False)

    def test_elastic_search_domain_unused_security_group_new(self):
        self.run_test_case('elastic_search_domain/unused_security_group_new', False)

    def test_elastic_search_domain_unused_security_group_existing(self):
        self.run_test_case('elastic_search_domain/unused_security_group_existing', True)

    # codebuild_project resources #
    def test_codebuild_project_used_security_group(self):
        self.run_test_case('codebuild_project/used_security_group', False)

    def test_codebuild_project_unused_security_group_new(self):
        self.run_test_case('codebuild_project/unused_security_group_new', False)

    def test_codebuild_project_unused_security_group_existing(self):
        self.run_test_case('codebuild_project/unused_security_group_existing', True)

    # Neptune resources #
    def test_neptune_used_security_group(self):
        self.run_test_case('neptune/used_security_group', False)

    def test_neptune_unused_security_group_new(self):
        self.run_test_case('neptune/unused_security_group_new', False)

    def test_neptune_unused_security_group_existing(self):
        self.run_test_case('neptune/unused_security_group_existing', True)

    # kinesis_firehose resources #
    def test_kinesis_firehose_used_security_group(self):
        self.run_test_case('kinesis_firehose/used_security_group', False)

    def test_kinesis_firehose_unused_security_group_new(self):
        self.run_test_case('kinesis_firehose/unused_security_group_new', False)

    def test_kinesis_firehose_unused_security_group_existing(self):
        self.run_test_case('kinesis_firehose/unused_security_group_existing', True)

    # DMS resources #
    def test_dms_used_security_group(self):
        self.run_test_case('dms/used_security_group', False)

    def test_dms_unused_security_group_new(self):
        self.run_test_case('dms/unused_security_group_new', False)

    def test_dms_unused_security_group_existing(self):
        self.run_test_case('dms/unused_security_group_existing', True)

    # workspace_directory resources #
    def test_workspace_directory_used_security_group(self):
        self.run_test_case('workspace_directory/used_security_group', False)

    def test_workspace_directory_unused_security_group_new(self):
        self.run_test_case('workspace_directory/unused_security_group_new', False)

    def test_workspace_directory_unused_security_group_existing(self):
        self.run_test_case('workspace_directory/unused_security_group_existing', True, 2)

    # batch compute environment resources #
    def test_batch_used_security_group(self):
        self.run_test_case('batch_compute/used_security_group', False)

    def test_batch_unused_security_group_new(self):
        self.run_test_case('batch_compute/unused_security_group_new', False)

    def test_batch_unused_security_group_existing(self):
        self.run_test_case('batch_compute/unused_security_group_existing', True)

    # MQ Broker resources #
    def test_mq_broker_used_security_group(self):
        self.run_test_case('mq_broker/used_security_group', False)

    def test_mq_broker_unused_security_group_new(self):
        self.run_test_case('mq_broker/unused_security_group_new', False)

    def test_mq_broker_unused_security_group_existing(self):
        self.run_test_case('mq_broker/unused_security_group_existing', True)

    # Api Gateway V2 resources #
    def test_api_gateway_v2_used_security_group(self):
        self.run_test_case('api_gateway_v2/used_security_group', False)

    def test_api_gateway_v2_unused_security_group_new(self):
        self.run_test_case('api_gateway_v2/unused_security_group_new', False)

    def test_api_gateway_v2_unused_security_group_existing(self):
        self.run_test_case('api_gateway_v2/unused_security_group_existing', True)

    # EMR cluster resources #
    def test_emr_cluster_used_security_group(self):
        self.run_test_case('emr_cluster/used_security_group', False)

    def test_emr_cluster_unused_security_group_new(self):
        self.run_test_case('emr_cluster/unused_security_group_new', False)

    def test_emr_cluster_unused_security_group_existing(self):
        self.run_test_case('emr_cluster/unused_security_group_existing', True)

    # Global Accelerator resources #
    def test_global_accelerator_used_security_group(self):
        self.run_test_case('global_accelerator/used_security_group', False)

    def test_global_accelerator_unused_security_group_new(self):
        self.run_test_case('global_accelerator/unused_security_group_new', False)

    def test_global_accelerator_unused_security_group_existing(self):
        self.run_test_case('global_accelerator/unused_security_group_existing', True)

    # CloudHSMv2 cluster resources #
    def test_cloudhsm_v2_cluster_used_security_group(self):
        self.run_test_case('cloudhsm_v2_cluster/used_security_group', False)

    def test_cloudhsm_v2_cluster_unused_security_group_new(self):
        self.run_test_case('cloudhsm_v2_cluster/unused_security_group_new', False)

    def test_cloudhsm_v2_cluster_unused_security_group_existing(self):
        self.run_test_case('cloudhsm_v2_cluster/unused_security_group_existing', True)

    # Unable to run rules tests for S3Outpost resource, as not able to fully apply it - needs physical connections and server.

    # WorkLink Fleet resources #
    def test_worklink_fleet_cluster_used_security_group(self):
        self.run_test_case('worklink_fleet/used_security_group', False)

    def test_worklink_fleet_cluster_unused_security_group_new(self):
        self.run_test_case('worklink_fleet/unused_security_group_new', False)

    def test_worklink_fleet_cluster_unused_security_group_existing(self):
        self.run_test_case('worklink_fleet/unused_security_group_existing', True)

    # Glue Connection resources #
    def test_glue_connection_cluster_used_security_group(self):
        self.run_test_case('glue_connection/used_security_group', False)

    def test_glue_connection_cluster_unused_security_group_new(self):
        self.run_test_case('glue_connection/unused_security_group_new', False)

    def test_glue_connection_cluster_unused_security_group_existing(self):
        self.run_test_case('glue_connection/unused_security_group_existing', True)

    # Simple standalone security group #
    def test_one_sg(self):
        self.run_test_case('one_sg', True)
