from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestCodeBuildProjects(AwsContextTest):

    def get_component(self):
        return "codebuild"

    @context(module_path="default_encryption")
    def test_default_encryption(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.codebuild_projects), 1)
        project = ctx.codebuild_projects[0]
        self.assertEqual(project.project_name, 'project-cloudrail-test')
        self.assertTrue(project.encryption_key)
        self.assertTrue(project.arn)
        self.assertFalse(project.tags)
        self.assertFalse(project.vpc_config)
        self.assertFalse(project.get_all_network_configurations())
        if not project.is_managed_by_iac:
            self.assertEqual(project.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/codesuite/codebuild/115553109071/projects/project-cloudrail-test/')

    @context(module_path="with_tags")
    def test_default_encryption_with_tags(self, ctx: AwsEnvironmentContext):
        project = next((project for project in ctx.codebuild_projects if project.project_name == 'project-cloudrail-test'), None)
        self.assertIsNotNone(project)
        self.assertTrue(project.tags)

    @context(module_path="codebuild_project_with_networking")
    def test_codebuild_project_with_networking(self, ctx: AwsEnvironmentContext):
        project = next((project for project in ctx.codebuild_projects if project.project_name == 'project-cloudrail-test'), None)
        self.assertIsNotNone(project)
        self.assertTrue(project.vpc_config)
        self.assertTrue(project.vpc_config.subnet_list_ids)
        self.assertTrue(project.vpc_config.security_groups_ids)
        self.assertTrue(project.network_resource.network_interfaces)
