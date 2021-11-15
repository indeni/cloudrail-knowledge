from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestProject(GcpContextTest):
    def get_component(self):
        return 'project'

    # Not running drift detection: no permission to create new project.
    @context(module_path="basic", test_options=TestOptions(run_drift_detection=False))
    def test_basic_project(self, ctx: GcpEnvironmentContext):
        project = next((project for project in ctx.projects if project.project_name == 'My Project'), None)
        self.assertIsNotNone(project)
        self.assertEqual(project.gcp_project_id, 'your-project-id')
        self.assertTrue(any(key in ('environment_hashcode', 'Name') for key in project.labels.keys()))
        if not project.is_managed_by_iac:
            self.assertEqual(project.project_number, '556062258574')
        else:
            self.assertIsNone(project.project_number)
