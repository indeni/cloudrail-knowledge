from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.mergeable import EntityOrigin

from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestComputeInstance(GcpContextTest):
    def get_component(self):
        return 'compute_instance'

    @context(module_path="basic")
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'cloudrail-test-google-compute-instance'), None)
        self.assertIsNotNone(compute)
        self.assertFalse(compute.can_ip_forward)
        self.assertIsNone(compute.hostname)
        self.assertIsNone(compute.service_account)
        self.assertIsNone(compute.shielded_instance_config)
        self.assertEqual(compute.zone, 'us-west1-a')
        self.assertTrue(compute.network_interfaces)
        self.assertTrue(compute.network_interfaces[0].access_config)
        self.assertEqual(compute.network_interfaces[0].access_config[0].network_tier, 'PREMIUM')
        self.assertIsNone(compute.network_interfaces[0].access_config[0].public_ptr_domain_name)
        self.assertFalse(compute.network_interfaces[0].alias_ip_range)
        self.assertEqual(compute.network_interfaces[0].network, 'default')
        self.assertIsNone(compute.network_interfaces[0].nic_type)
        if compute.origin == EntityOrigin.TERRAFORM:
            self.assertIsNone(compute.network_interfaces[0].access_config[0].nat_ip)
            self.assertIsNone(compute.network_interfaces[0].network_ip)
            self.assertIsNone(compute.network_interfaces[0].subnetwork)
            self.assertIsNone(compute.network_interfaces[0].subnetwork_project)
        elif compute.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(compute.network_interfaces[0].access_config[0].nat_ip, '34.127.40.75')
            self.assertEqual(compute.network_interfaces[0].network_ip, '10.138.0.5')
            self.assertEqual(compute.network_interfaces[0].subnetwork, 'default')
            self.assertEqual(compute.network_interfaces[0].subnetwork_project, 'dev-for-tests')

    @context(module_path="serial_ports_one_enabled_one_disabled")
    def test_serial_ports_one_enabled_one_disabled(self, ctx: GcpEnvironmentContext):
        self.assertEqual(len(ctx.compute_instances), 2)
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'gce-5'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.metadata)
        self.assertEqual(compute.metadata, [{'serial-port-enable': 'true'}])
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'gce-6'), None)
        self.assertIsNotNone(compute)
        self.assertFalse(compute.metadata)

    @context(module_path="shielded_vm_config/enable_neither_vptm_nor_integrity")
    def test_shielded_vm_enable_neither_vptm_nor_integrity(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'one-enabled'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.shielded_instance_config)
        self.assertTrue(compute.shielded_instance_config.enable_secure_boot)
        self.assertFalse(compute.shielded_instance_config.enable_integrity_monitoring)
        self.assertFalse(compute.shielded_instance_config.enable_vtpm)

    @context(module_path="shielded_vm_config/enable_vtpm_and_integrity")
    def test_shielded_vm_enable_vtpm_and_integrity(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'one-enabled'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.shielded_instance_config)
        self.assertTrue(compute.shielded_instance_config.enable_secure_boot)
        self.assertTrue(compute.shielded_instance_config.enable_integrity_monitoring)
        self.assertTrue(compute.shielded_instance_config.enable_vtpm)

    @context(module_path="shielded_vm_config/enable_vtpm_not_integrity")
    def test_shielded_vm_enable_vtpm_not_integrity(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'one-enabled'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.shielded_instance_config)
        self.assertTrue(compute.shielded_instance_config.enable_secure_boot)
        self.assertFalse(compute.shielded_instance_config.enable_integrity_monitoring)
        self.assertTrue(compute.shielded_instance_config.enable_vtpm)

    @context(module_path="default_service_account")
    def test_default_service_account(self, ctx: GcpEnvironmentContext):
        self.assertTrue(len(ctx.compute_instances), 2)
        for compute in ctx.compute_instances:
            self.assertTrue(compute.name in ('gce-def-01', 'gce-def-02'))
            self.assertTrue(compute.service_account)
            self.assertEqual(compute.service_account.email, '37924132841-compute@developer.gserviceaccount.com')
            self.assertEqual(compute.service_account.scopes, ['https://www.googleapis.com/auth/cloud-platform'])

    @context(module_path="default_service_account_no_email")
    def test_default_service_account_no_email(self, ctx: GcpEnvironmentContext):
        self.assertTrue(len(ctx.compute_instances), 2)
        for compute in ctx.compute_instances:
            self.assertTrue(compute.name in ('gce-def-01', 'gce-def-02'))
            self.assertTrue(compute.service_account)
            self.assertEqual(compute.service_account.scopes, ['https://www.googleapis.com/auth/cloud-platform'])
            if compute.is_managed_by_iac:
                self.assertFalse(compute.service_account.email)
            else:
                self.assertEqual(compute.service_account.email, '37924132841-compute@developer.gserviceaccount.com')
