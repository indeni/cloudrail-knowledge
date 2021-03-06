from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.context.mergeable import EntityOrigin
from cloudrail.knowledge.context.connection import PortConnectionProperty
from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import context


class TestComputeInstance(GcpContextTest):
    def get_component(self):
        return 'compute_instance'

    @context(module_path="basic_1", base_scanner_data_for_iac='account-data-gcp-default-vpc-network.zip')
    def test_basic(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'cloudrail-test-google-compute-instance'), None)
        self.assertIsNotNone(compute)
        self.assertFalse(compute.can_ip_forward)
        self.assertIsNone(compute.hostname)
        self.assertIsNone(compute.service_account)
        self.assertIsNone(compute.shielded_instance_config)
        self.assertEqual(compute.zone, 'us-west1-a')
        self.assertTrue(compute.compute_network_interfaces)
        self.assertTrue(compute.compute_network_interfaces[0].access_config)
        self.assertEqual(compute.compute_network_interfaces[0].access_config[0].network_tier, 'PREMIUM')
        self.assertIsNone(compute.compute_network_interfaces[0].access_config[0].public_ptr_domain_name)
        self.assertFalse(compute.compute_network_interfaces[0].alias_ip_range)
        self.assertIsNone(compute.compute_network_interfaces[0].nic_type)
        if compute.origin == EntityOrigin.TERRAFORM:
            self.assertIsNone(compute.compute_network_interfaces[0].access_config[0].nat_ip)
            self.assertIsNone(compute.compute_network_interfaces[0].network_ip)
            self.assertIsNone(compute.compute_network_interfaces[0].subnetwork)
            self.assertIsNone(compute.compute_network_interfaces[0].subnetwork_project)
            self.assertEqual(compute.compute_network_interfaces[0].network, 'default')
        elif compute.origin == EntityOrigin.LIVE_ENV:
            self.assertEqual(compute.compute_network_interfaces[0].access_config[0].nat_ip, '35.185.227.55')
            self.assertEqual(compute.compute_network_interfaces[0].network_ip, '10.138.0.49')
            self.assertEqual(compute.compute_network_interfaces[0].network,
                             'https://www.googleapis.com/compute/v1/projects/dev-for-tests/global/networks/default')
            self.assertEqual(compute.compute_network_interfaces[0].subnetwork,
                             'https://www.googleapis.com/compute/v1/projects/dev-for-tests/regions/us-west1/subnetworks/default')
            self.assertEqual(compute.compute_network_interfaces[0].subnetwork_project, 'dev-for-tests')

    @context(module_path="serial_ports_one_enabled_one_disabled_1", base_scanner_data_for_iac='account-data-gcp-default-vpc-network.zip')
    def test_serial_ports_one_enabled_one_disabled(self, ctx: GcpEnvironmentContext):
        self.assertEqual(len(ctx.compute_instances), 2)
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'gce-5'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.metadata)
        self.assertEqual(compute.metadata, {'serial-port-enable': 'true'})
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'gce-6'), None)
        self.assertIsNotNone(compute)
        self.assertFalse(compute.metadata)

    @context(module_path="shielded_vm_config/enable_neither_vptm_nor_integrity_1", base_scanner_data_for_iac='account-data-gcp-default-vpc-network.zip')
    def test_shielded_vm_enable_neither_vptm_nor_integrity(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'one-enabled'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.shielded_instance_config)
        self.assertTrue(compute.shielded_instance_config.enable_secure_boot)
        self.assertFalse(compute.shielded_instance_config.enable_integrity_monitoring)
        self.assertFalse(compute.shielded_instance_config.enable_vtpm)

    @context(module_path="shielded_vm_config/enable_vtpm_and_integrity_1", base_scanner_data_for_iac='account-data-gcp-default-vpc-network.zip')
    def test_shielded_vm_enable_vtpm_and_integrity(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'one-enabled'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.shielded_instance_config)
        self.assertTrue(compute.shielded_instance_config.enable_secure_boot)
        self.assertTrue(compute.shielded_instance_config.enable_integrity_monitoring)
        self.assertTrue(compute.shielded_instance_config.enable_vtpm)

    @context(module_path="shielded_vm_config/enable_vtpm_not_integrity_1", base_scanner_data_for_iac='account-data-gcp-default-vpc-network.zip')
    def test_shielded_vm_enable_vtpm_not_integrity(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'one-enabled'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(compute.shielded_instance_config)
        self.assertTrue(compute.shielded_instance_config.enable_secure_boot)
        self.assertFalse(compute.shielded_instance_config.enable_integrity_monitoring)
        self.assertTrue(compute.shielded_instance_config.enable_vtpm)

    @context(module_path="default_service_account_1", base_scanner_data_for_iac='account-data-gcp-default-vpc-network.zip')
    def test_default_service_account(self, ctx: GcpEnvironmentContext):
        self.assertTrue(len(ctx.compute_instances), 2)
        for compute in ctx.compute_instances:
            self.assertTrue(compute.name in ('gce-def-01', 'gce-def-02'))
            self.assertTrue(compute.service_account)
            self.assertEqual(compute.service_account.email, '37924132841-compute@developer.gserviceaccount.com')
            self.assertEqual(compute.service_account.scopes, ['https://www.googleapis.com/auth/cloud-platform'])

    @context(module_path="default_service_account_no_email_1", base_scanner_data_for_iac='account-data-gcp-default-vpc-network.zip')
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

    @context(module_path="default_service_with_labels", base_scanner_data_for_iac='account-data-gcp-default-vpc-network.zip')
    def test_default_service_account_with_labels(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances if compute.name == 'gce-def-01'), None)
        self.assertIsNotNone(compute)
        self.assertTrue(key in ('Test_hashcode', 'Name') for key in compute.labels.keys())

    @context(module_path="unrestricted_and_pub_ip", base_scanner_data_for_iac='account-data-gcp-default-vpc-network.zip')
    def test_unrestricted_and_pub_ip(self, ctx: GcpEnvironmentContext):
        compute = next((compute for compute in ctx.compute_instances
                        if compute.name == 'unrestricted-gce'), None)
        self.assertIsNotNone(compute)
        self.assertEqual(len(compute.inbound_connections), 7)
        self.assertTrue(any(conn_prop.connection_property == PortConnectionProperty([(22, 22)], '0.0.0.0/0', IpProtocol('TCP'))
                            for conn_prop in compute.inbound_connections))
