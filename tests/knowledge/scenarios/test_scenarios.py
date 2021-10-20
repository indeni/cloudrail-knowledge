import unittest

from tests.knowledge.scenarios.base_test_scenarios import BaseTestScenarios


class TestScenarios(BaseTestScenarios):

    def test_terraform_aws_vpc_examples_complete_vpc(self):
        self.run_test_case('terraform-aws-vpc/examples/complete-vpc',
                           failed_rule_ids=['non_car_cw_log_group_no_retention'])

    def test_terraform_aws_vpc_examples_simple_vpc(self):
        self.run_test_case('terraform-aws-vpc/examples/simple-vpc',
                           failed_rule_ids=[])

    def test_terraform_ecs(self):
        self.run_test_case('terraform-ecs',
                           failed_rule_ids=['non_car_ensure_imdsv2'])

    def test_covid_alert_server_staging_terraform(self):
        self.run_test_case('covid-alert-server-staging-terraform/server/aws',
                           failed_rule_ids=['non_car_s3_bucket_policy_secure_transport',
                                            's3_bucket_policy_vpce'])

    def test_tack(self):
        self.run_test_case('tack')

    def test_detectionlab(self):
        self.run_test_case('DetectionLab/AWS/Terraform',
                           failed_rule_ids=['non_car_ensure_imdsv2'])

    def test_terragoat(self):
        self.run_test_case('terragoat/terraform/aws',
                           failed_rule_ids=[
                               'public_access_elasticsearch_rule',
                               'non_car_iam_no_permissions_directly_to_user',
                               'non_car_ensure_imdsv2',
                               'non_car_s3_bucket_policy_secure_transport'])

    # only support tf 12/13
    def test_consoleme(self):
        self.run_test_case('consoleme/terraform/central-account',
                           failed_rule_ids=['non_car_s3_bucket_policy_secure_transport',
                                            'non_car_alb_target_group_no_http'])

    def test_terraform_aws_iam_examples_iam_account(self):
        self.run_test_case('terraform-aws-iam/examples/iam-account',
                           failed_rule_ids=[])

    def test_terraform_aws_iam_examples_iam_assumable_role_with_oidc(self):
        self.run_test_case('terraform-aws-iam/examples/iam-assumable-role-with-oidc',
                           failed_rule_ids=[])

    def test_terraform_aws_iam_examples_iam_assumable_role(self):
        self.run_test_case('terraform-aws-iam/examples/iam-assumable-role',
                           failed_rule_ids=[])

    def test_terraform_aws_iam_examples_iam_group_complete(self):
        self.run_test_case('terraform-aws-iam/examples/iam-group-complete',
                           failed_rule_ids=[])

    def test_terraform_aws_iam_examples_iam_group_with_policies(self):
        self.run_test_case('terraform-aws-iam/examples/iam-group-with-policies',
                           failed_rule_ids=[])

    def test_terraform_aws_iam_examples_iam_policy(self):
        self.run_test_case('terraform-aws-iam/examples/iam-policy',
                           failed_rule_ids=[])

    def test_terraform_aws_iam_examples_iam_user(self):
        self.run_test_case('terraform-aws-iam/examples/iam-user',
                           failed_rule_ids=['non_car_iam_no_human_users'])

    def test_vault_on_aws(self):
        self.run_test_case('vault-on-aws',
                           failed_rule_ids=[])

    # show failed on jenkins
    def test_terraform_aws_gitlab_runner_examples_runner_public(self):
        self.run_test_case('terraform-aws-gitlab-runner/examples/runner-public',
                           failed_rule_ids=[])

    # show failed on jenkins
    def test_terraform_aws_gitlab_runner_examples_runner_default(self):
        self.run_test_case('terraform-aws-gitlab-runner/examples/runner-default',
                           failed_rule_ids=[])

    # show failed on jenkins
    def test_terraform_aws_gitlab_runner_examples_runner_docker(self):
        self.run_test_case('terraform-aws-gitlab-runner/examples/runner-docker',
                           failed_rule_ids=[])

    # show failed on jenkins
    def test_terraform_aws_gitlab_runner_examples_runner_pre_registered(self):
        self.run_test_case('terraform-aws-gitlab-runner/examples/runner-pre-registered',
                           failed_rule_ids=[])

    @unittest.skip('Need the ability to run specific versions of TF (TF 0.12 not supported by this scenario)')
    def test_sadcloud(self):
        self.run_test_case('sadcloud/sadcloud',
                           failed_rule_ids=[
                               'non_car_s3_bucket_policy_secure_transport',
                               's3_acl_disallow_public_and_cross_account',
                               'not_car_rds_instances_encrypted_at_rest',
                               'not_car_elasticsearch_domains_encrypted_note_to_node',
                               'public_access_elasticsearch_rule',
                               'ensure_all_used_default_security_groups_restrict_all_traffic_rule'])

    def test_lots_of_ec2s(self):
        self.run_test_case('lot-of-ec2s')

    def test_lots_of_roles(self):
        self.run_test_case('lot-of-roles')

    # only support tf 14
    def test_performance_eni_100(self):
        self.run_test_case('performance-eni-100')

    def test_serverless_jenkins_on_aws_fargate(self):
        self.run_test_case('serverless-jenkins-on-aws-fargate/modules/jenkins_platform',
                           failed_rule_ids=[
                               'non_car_alb_target_group_no_http',
                               'not_car_cloudwatch_log_group_encrypted_at_rest_using_kms_cmk'
                           ])

    @unittest.skip('Need the ability to run specific versions of TF (TF 0.12 not supported by this scenario)')
    def test_serverless_tf_playground(self):
        self.run_test_case('serverless.tf-playground/terraform')

    # only support tf 14
    def test_performance_eni_1000(self):
        self.run_test_case('performance-eni-1000')

    def test_performance_eni_10000(self):
        self.run_test_case('performance-eni-10000')
