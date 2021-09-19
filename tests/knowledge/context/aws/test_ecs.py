from unittest import skip

from cloudrail.knowledge.context.connection import ConnectionDetail, PortConnectionProperty, ConnectionType, PrivateConnectionDetail, \
    PolicyConnectionProperty, PolicyEvaluation
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_event_target import CloudWatchEventTarget
from cloudrail.knowledge.context.aws.resources.ecs.ecs_constants import LaunchType, NetworkMode
from cloudrail.knowledge.context.aws.resources.ecs.ecs_service import EcsService
from cloudrail.knowledge.context.aws.resources.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.resources.ecs.ecs_task_definition import EcsTaskDefinition, ContainerDefinition, PortMappings
from cloudrail.knowledge.context.aws.resources.networking_config.inetwork_configuration import INetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.policy_evaluator import is_any_action_allowed
from cloudrail.knowledge.utils.utils import is_subset

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestEcs(AwsContextTest):

    def get_component(self):
        return "ecs"

    @context(module_path="fargate/ecs-service-network-configuration")
    def test_ecs_service_network_configuration(self, ctx: AwsEnvironmentContext):
        cluster = next(cluster for cluster in ctx.ecs_cluster_list if cluster.cluster_name == 'ecs-cluster')
        self.assertFalse(cluster.is_container_insights_enabled)
        self.assertEqual(1, len(cluster.service_list), "empty services list")
        self.assertEqual(cluster.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/ecs-cluster/services')
        service = cluster.service_list[0]
        self.assertEqual(service.name, "web-server-service")
        self.assertIsNotNone(service.cluster_arn, cluster.cluster_arn)
        self.assertEqual(service.launch_type, LaunchType.FARGATE)
        self.assertEqual(1, len(service.elb_list), "empty elb list")
        elb_conf = service.elb_list[0]
        self.assertIsNotNone(elb_conf.target_group_arn)
        self.assertEqual(elb_conf.container_name, "apache-web-server")
        self.assertEqual(80, elb_conf.container_port)
        self._assert_network_configuration_list(service)
        self._assert_network_connections(service)
        self.assertIsNotNone(service.cluster_arn, cluster.cluster_arn)
        self.assertFalse(service.tags)

    @context(module_path="fargate/ecs-event-target-network-configuration")
    def test_ecs_event_target_network_configuration(self, ctx: AwsEnvironmentContext):
        cluster = next(cluster for cluster in ctx.ecs_cluster_list if cluster.cluster_name == 'ecs-cluster')
        self.assertEqual(1, len(cluster.event_target_list), "empty event target list")
        event_target = cluster.event_target_list[0]
        self.assertEqual(event_target.rule_name, "web-server-schedule-every-1d-rule")
        self.assertEqual(event_target.cluster_arn, cluster.cluster_arn)
        target = event_target.ecs_target_list[0]
        self.assertIsNotNone(target.name)
        self.assertIsNotNone(target.target_id)
        self.assertEqual(target.launch_type, LaunchType.FARGATE)
        self.assertIsNotNone(target.cluster_arn)
        self.assertIsNotNone(target.role_arn)
        self._assert_network_configuration_list(target)
        self._assert_network_connections(target)
        if not target.is_managed_by_iac:
            self.assertEqual(target.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/ecs-cluster/tasks')

    @skip('Pending CR-458')
    @context(module_path="ec2/service")
    def test_ec2_capacity_type(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.ecs_cluster_list))
        self.assertEqual(1, len(ctx.ecs_service_list))
        self.assertEqual(1, len(ctx.auto_scaling_groups))
        self.assertEqual(1, len(ctx.load_balancers))
        self.assertEqual(1, len(ctx.load_balancer_target_groups))
        service = ctx.ecs_service_list[0]
        lb = ctx.load_balancers[0]
        target_group = lb.target_groups[0]
        acg = ctx.auto_scaling_groups[0]
        ec2 = ctx.ec2s[0]
        self.assertIs(target_group.targets[0].target_instance, service)
        self.assertListEqual(acg.availability_zones, ['us-east-2a'])
        self.assertListEqual(acg.subnet_ids, [])
        self.assertTrue(acg.launch_template)
        self.assertTrue(list(ec2.network_resource.security_groups)[0].is_default)
        self.assertTrue(ec2.network_resource.vpc.is_default)
        self.assertEqual(len(ec2.network_resource.subnets), 1)
        self.assertTrue(ec2.network_resource.subnets[0].is_default)
        self.assertEqual(ec2.network_resource.subnets[0].availability_zone, 'us-east-2a')

    @context(module_path="fargate/ecs-task-definition", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_ecs_task_definition(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.ecs_task_definitions))
        task: EcsTaskDefinition = ctx.ecs_task_definitions[0]
        if task.iac_state:
            self.assertEqual(task.task_arn, 'aws_ecs_task_definition.web-server-task-definition.arn')
            self.assertEqual(task.revision, 'aws_ecs_task_definition.web-server-task-definition.revision')
            self.assertEqual(task.task_role_arn, 'aws_iam_role.ecs-instance-role.arn')
            self.assertTrue('role/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS' in task.execution_role_arn)
        else:
            self.assertEqual(task.task_arn, 'arn:aws:ecs:us-east-1:111111111111:task-definition/web-server-task:2')
            self.assertEqual(task.revision, 1)
            self.assertEqual(task.task_role_arn, 'arn:aws:iam::111111111111:role/some-task-role')
            self.assertEqual(task.execution_role_arn, 'arn:aws:iam::111111111111:role/some-exec-role')
            self.assertEqual(task.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/ecs/home?region=us-east-1#/taskDefinitions/web-server-task/1')
        self.assertEqual(task.family, 'web-server-task')
        self.assertFalse(task.tags)
        self.assertEqual(task.network_mode, NetworkMode.AWS_VPC)
        self.assertFalse(task.is_volume_efs)
        self.assertFalse(task.efs_volume_data)
        self.assertEqual(1, len(task.container_definitions))
        container_definition: ContainerDefinition = task.container_definitions[0]
        self.assertEqual(container_definition.container_name, 'apache-web-server')
        self.assertEqual(container_definition.image, '/ecr/repository/image/path')

        self.assertEqual(1, len(container_definition.port_mappings))
        port_map: PortMappings = container_definition.port_mappings[0]
        self.assertEqual(port_map.container_port, 80)
        self.assertEqual(port_map.host_port, 80)
        self.assertEqual(port_map.protocol, IpProtocol('TCP'))

    @context(module_path="fargate/ecs-target-public-connections")
    def test_ecs_target_public_connections(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.cloud_watch_event_target_list))
        event_target: CloudWatchEventTarget = ctx.cloud_watch_event_target_list[0]
        self.assertEqual(1, len(event_target.ecs_target_list))
        ecs_target: EcsTarget = event_target.ecs_target_list[0]
        self._assert_inbound_connections(ecs_target, ConnectionType.PUBLIC)
        self._assert_outbound_connections(ecs_target, ConnectionType.PUBLIC)

    @context(module_path="fargate/ecs-service-private-connections")
    def test_ecs_service_private_connections(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.ecs_service_list))
        ecs_service: EcsService = ctx.ecs_service_list[0]
        self._assert_inbound_connections(ecs_service, ConnectionType.PRIVATE)
        self._assert_outbound_connections(ecs_service, ConnectionType.PRIVATE)
        if not ecs_service.is_managed_by_iac:
            self.assertEqual(ecs_service.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/ecs-cluster/services/web-server-service/details')

    @context(module_path="fargate/ecs-service-without-inbound-connections")
    def test_ecs_service_without_inbound_connections(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.ecs_service_list))
        ecs_service: EcsService = ctx.ecs_service_list[0]
        self.assertEqual(0, len(ecs_service.network_resource.inbound_connections))

    @context(module_path="fargate/ecs-instance-permissions-outbound-connections")
    def test_ecs_instance_permissions_outbound_connections(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.ecs_service_list))
        ecs_service: EcsService = ctx.ecs_service_list[0]
        bucket = ctx.s3_buckets['randombucketname92194']
        self.assertEqual(len(ecs_service.network_resource.network_interfaces), 1)

        conn = next((connection for connection in ecs_service.network_resource.network_interfaces[0].outbound_connections
                     if isinstance(connection, PrivateConnectionDetail) and connection.target_instance == bucket), None)
        self.assertIsNotNone(conn)

        policy_conn: PolicyConnectionProperty = conn.connection_property
        self.assertEqual(len(policy_conn.policy_evaluation), 1)
        policy_eval: PolicyEvaluation = policy_conn.policy_evaluation[0]
        self.assertTrue(is_any_action_allowed(policy_eval))

    @context(module_path="fargate/ecs-instance-inbound-permissions-connections")
    def test_ecs_instance_inbound_permissions_connections(self, ctx: AwsEnvironmentContext):
        ecs_service: EcsService = next((service for service in ctx.ecs_service_list if service.name == 'web-server-service'))
        self.assertIsNotNone(ecs_service)
        user = next((user for user in ctx.users if user.name == 'user-1'))
        self.assertIsNotNone(user)

        conn = next((connection for connection in ecs_service.inbound_connections
                     if isinstance(connection, PrivateConnectionDetail) and connection.target_instance == user), None)
        self.assertIsNotNone(conn)

    def _assert_network_configuration_list(self, net_conf: INetworkConfiguration):
        self.assertGreaterEqual(1, len(net_conf.get_all_network_configurations()), "empty service network configuration list")
        for conf in net_conf.get_all_network_configurations():
            self.assertTrue(conf.assign_public_ip)
            self.assertGreaterEqual(1, len(conf.security_groups_ids), "empty security group id list")
            self.assertGreaterEqual(1, len(conf.subnet_list_ids), "empty subnet id list")

    def _assert_network_connections(self, entity: NetworkEntity):
        self.assertGreaterEqual(len(entity.network_resource.inbound_connections), 1)
        self.assertGreaterEqual(len(entity.network_resource.outbound_connections), 1)

    def _assert_inbound_connections(self, net_entity: NetworkEntity, conn_type: ConnectionType):
        self.assertEqual(1, len(net_entity.network_resource.inbound_connections))
        conn_details: ConnectionDetail = net_entity.network_resource.inbound_connections[0]
        self.assertEqual(conn_details.connection_type, conn_type)
        conn: PortConnectionProperty = conn_details.connection_property
        self.assertEqual(1, len(conn.ports))
        self.assertEqual(conn.ports[0], (80, 80))
        self.assertEqual(conn.ip_protocol_type, IpProtocol('TCP'))
        if conn_type == ConnectionType.PRIVATE:
            self.assertTrue(is_subset(conn.cidr_block, "192.168.100.128/25"))
        else:
            self.assertTrue(conn.cidr_block == "0.0.0.0/0")

    def _assert_outbound_connections(self, net_entity: NetworkEntity, conn_type: ConnectionType):
        self.assertEqual(1, len(net_entity.network_resource.outbound_connections))
        conn_details: ConnectionDetail = net_entity.network_resource.outbound_connections[0]
        self.assertEqual(conn_details.connection_type, conn_type)
        conn: PortConnectionProperty = conn_details.connection_property
        self.assertEqual(1, len(conn.ports))
        if conn_type == ConnectionType.PRIVATE:
            self.assertEqual(conn.ip_protocol_type, IpProtocol('TCP'))
            self.assertEqual(conn.ports[0], (80, 80))
            self.assertTrue(is_subset(conn.cidr_block, "192.168.100.128/25"))
        else:
            self.assertEqual(conn.ip_protocol_type, IpProtocol('ALL'))
            self.assertEqual(conn.ports[0], (0, 65535))
            self.assertTrue(conn.cidr_block == "0.0.0.0/0")

    @context(module_path="task_definition_encrypted_in_transit")
    def test_ecs_task_definition_encrypted_in_transit(self, ctx: AwsEnvironmentContext):
        task_def = next((task_def for task_def in ctx.ecs_task_definitions if task_def.family == 'cloudrail-test-encryption'), None)
        self.assertIsNotNone(task_def)
        self.assertTrue(task_def.is_volume_efs)
        self.assertTrue(task_def.efs_volume_data[0].encrypt_efs_in_transit)
        self.assertTrue(task_def.efs_volume_data[0].efs_id)
        self.assertEqual(task_def.efs_volume_data[0].volume_name, 'service-storage')

    @context(module_path="task_definition_not_encrypted_in_transit")
    def test_task_definition_not_encrypted_in_transit(self, ctx: AwsEnvironmentContext):
        task_def = next((task_def for task_def in ctx.ecs_task_definitions if task_def.family == 'cloudrail-test-encryption'), None)
        self.assertIsNotNone(task_def)
        self.assertTrue(task_def.is_volume_efs)
        self.assertFalse(task_def.efs_volume_data[0].encrypt_efs_in_transit)
        self.assertTrue(task_def.efs_volume_data[0].efs_id)
        self.assertEqual(task_def.efs_volume_data[0].volume_name, 'service-storage')

    @context(module_path="task_definition_multiple_volumes")
    def test_task_definition_multiple_volumes(self, ctx: AwsEnvironmentContext):
        task_def = next((task_def for task_def in ctx.ecs_task_definitions if task_def.family == 'cloudrail-test-encryption'), None)
        self.assertIsNotNone(task_def)
        self.assertTrue(task_def.is_volume_efs)
        for volume in task_def.efs_volume_data:
            self.assertFalse(volume.encrypt_efs_in_transit)
            self.assertTrue(volume.efs_id)
            self.assertIn('service-storage', volume.volume_name)

    @context(module_path="with_tags")
    def test_ecs_cluster_with_tags(self, ctx: AwsEnvironmentContext):
        cluster = next(cluster for cluster in ctx.ecs_cluster_list if cluster.cluster_name == 'ecs-cluster')
        service = ctx.ecs_service_list[0]
        task: EcsTaskDefinition = ctx.ecs_task_definitions[0]
        subnet = next((subnet for subnet in ctx.subnets if "192.168.10.0/24" in subnet.cidr_block), None)
        self.assertTrue(cluster.tags)
        self.assertTrue(task.tags)
        self.assertTrue(service.tags)
        self.assertTrue(subnet.tags)

    @context(module_path="fargate/ecs_with_container_insights")
    def test_ecs_with_container_insights(self, ctx: AwsEnvironmentContext):
        cluster = next(cluster for cluster in ctx.ecs_cluster_list if cluster.cluster_name == 'ecs-insights-test')
        self.assertIsNotNone(cluster)
        self.assertTrue(cluster.is_container_insights_enabled)

    @context(module_path="fargate/ecs_disable_insight")
    def test_ecs_disable_insight(self, ctx: AwsEnvironmentContext):
        cluster = next(cluster for cluster in ctx.ecs_cluster_list if cluster.cluster_name == 'ecs-insights-test')
        self.assertIsNotNone(cluster)
        self.assertFalse(cluster.is_container_insights_enabled)

    @context(module_path="ec2/ecs_service_without_launch_type")
    def test_ecs_service_without_launch_type(self, ctx: AwsEnvironmentContext):
        cluster = next(cluster for cluster in ctx.ecs_cluster_list if cluster.cluster_name == 'ecs-cluster')
        self.assertIsNotNone(cluster)
        ecs_service = cluster.service_list[0]
        self.assertEqual(ecs_service.launch_type, LaunchType.EC2)
