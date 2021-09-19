from tests.knowledge.context.aws_context_test import AwsContextTest
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.test_context_annotation import context


class TestElasticSearchDomain(AwsContextTest):

    def get_component(self):
        return 'es'

    @context(module_path="defaults-only")
    def test_defaults_only(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.elastic_search_domains))
        esd = ctx.elastic_search_domains[0]
        self.assertTrue(esd.is_public)
        self.assertFalse(esd.is_in_vpc)
        self.assertEqual(esd.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/es/home?region=us-east-1#domain:resource=test;action=dashboard')
        esd.ports.sort()
        self.assertListEqual([80, 443], esd.ports)
        self.assertFalse(esd.encrypt_at_rest_state)
        self.assertFalse(esd.encrypt_node_to_node_state)
        self.assertFalse(esd.tags)
        self.assertFalse(esd.log_publishing_options)
        self.assertEqual(esd.es_domain_version, '1.5')
        self.assertEqual(esd.es_domain_cluster_instance_type, 'm4.large.elasticsearch')

    @context(module_path="encrypt-at-rest-enabled")
    def test_encrypt_at_rest_enabled(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.elastic_search_domains))
        esd = ctx.elastic_search_domains[0]
        self.assertTrue(esd.is_public)
        self.assertFalse(esd.is_in_vpc)
        esd.ports.sort()
        self.assertListEqual([80, 443], esd.ports)
        self.assertTrue(esd.encrypt_at_rest_state)

    @context(module_path="encrypt-node-to-node-enabled")
    def test_encrypt_node_to_node_enabled(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.elastic_search_domains))
        esd = ctx.elastic_search_domains[0]
        self.assertTrue(esd.is_public)
        self.assertFalse(esd.is_in_vpc)
        esd.ports.sort()
        self.assertListEqual([80, 443], esd.ports)
        self.assertTrue(esd.encrypt_node_to_node_state)
        self.assertEqual(esd.es_domain_version, '6.0')
        self.assertEqual(esd.es_domain_cluster_instance_type, 'i3.large.elasticsearch')

    @context(module_path="vpc-controlled")
    def test_vpc_controlled(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.elastic_search_domains))
        esd = ctx.elastic_search_domains[0]
        self.assertFalse(esd.is_public)
        self.assertTrue(esd.is_in_vpc)
        esd.ports.sort()
        self.assertListEqual([80, 443], esd.ports)
        self.assertEqual(len(esd.network_resource.network_interfaces), 1)
        self.assertEqual(len(esd.network_resource.subnets), 1)
        self.assertEqual(len(esd.network_resource.security_groups), 1)

    @context(module_path="vpc-controlled-enforce-https")
    def test_vpc_controlled_enforce_https(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.elastic_search_domains))
        esd = ctx.elastic_search_domains[0]
        self.assertFalse(esd.is_public)
        self.assertTrue(esd.is_in_vpc)
        self.assertListEqual([443], esd.ports)
        self.assertEqual(len(esd.network_resource.network_interfaces), 2)
        self.assertEqual(len(esd.network_resource.subnets), 2)
        self.assertEqual(len(esd.network_resource.security_groups), 1)
        self.assertFalse(esd.network_resource.security_groups.pop().is_default)

    @context(module_path="vpc-controlled-no-sg")
    def test_vpc_controlled_no_sg(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.elastic_search_domains))
        esd = ctx.elastic_search_domains[0]
        self.assertFalse(esd.is_public)
        self.assertTrue(esd.is_in_vpc)
        esd.ports.sort()
        self.assertListEqual([80, 443], esd.ports)
        self.assertEqual(len(esd.network_resource.network_interfaces), 2)
        self.assertEqual(len(esd.network_resource.subnets), 2)
        self.assertEqual(len(esd.network_resource.security_groups), 1)
        self.assertTrue(esd.network_resource.security_groups.pop().is_default)

    @context(module_path="secure_policy")
    def test_secure_policy(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.elastic_search_domains_policies))
        for policy in ctx.elastic_search_domains_policies:
            self.assertEqual(policy.domain_name, 'es-secure-policy')
            self.assertEqual(policy.statements[0].effect, StatementEffect.ALLOW)
            self.assertEqual(policy.statements[0].actions, ['es:ESHttpGet'])

    @context(module_path="not_secure_policy")
    def test_not_secure_policy(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.elastic_search_domains))
        for es_domain in ctx.elastic_search_domains:
            self.assertEqual(es_domain.policy.domain_name, 'es-not-secure-policy')
            self.assertEqual(es_domain.policy.statements[0].effect, StatementEffect.ALLOW)
            self.assertEqual(es_domain.policy.statements[0].actions, ['es:*'])

    @context(module_path="secure_policy_tf_from_main_resource")
    def test_secure_policy_tf_from_main_resource(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.elastic_search_domains))
        for es_domain in ctx.elastic_search_domains:
            self.assertEqual(es_domain.name, 'es-secure-policy')
            self.assertEqual(es_domain.policy.statements[0].effect, StatementEffect.ALLOW)
            self.assertEqual(es_domain.policy.statements[0].actions, ['es:ESHttpGet'])

    @context(module_path="with_tags")
    def test_with_tags(self, ctx: AwsEnvironmentContext):
        esd = next((esd for esd in ctx.elastic_search_domains if esd.name == 'test'), None)
        self.assertIsNotNone(esd)
        self.assertTrue(esd.tags)

    @context(module_path="with_log_publish_options")
    def test_with_log_publish_options(self, ctx: AwsEnvironmentContext):
        esd = next((esd for esd in ctx.elastic_search_domains if esd.name == 'domain-logging-test'), None)
        self.assertIsNotNone(esd)
        self.assertTrue(esd.log_publishing_options)
        log_index = next((log for log in esd.log_publishing_options if log.log_type == 'INDEX_SLOW_LOGS'), None)
        self.assertIsNotNone(log_index)
        self.assertTrue(log_index.enabled)
        self.assertTrue(log_index.cloudwatch_log_group_arn)
