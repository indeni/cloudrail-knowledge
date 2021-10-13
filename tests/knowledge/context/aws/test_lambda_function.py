from cloudrail.knowledge.context.connection import PolicyEvaluation, PortConnectionProperty, ConnectionDetail, PolicyConnectionProperty, \
    PrivateConnectionDetail
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import LambdaAlias
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect, StatementCondition
from cloudrail.knowledge.context.aws.resources.iam.principal import PrincipalType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.utils.policy_evaluator import get_allowed_actions, is_any_action_allowed

from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import TestOptions, context


class TestLambdaFunction(AwsContextTest):

    def get_component(self):
        return "lambda-function"

    # All tests here which marked not running drift - unable to apply the TF.
    @context(module_path="lambda-without-permissions", test_options=TestOptions(run_drift_detection=False))
    def test_lambda_without_permissions(self, ctx: AwsEnvironmentContext):
        lambda_func: LambdaFunction = self._assert_lambda(ctx)
        self.assertIsNone(lambda_func.resource_based_policy)
        self.assertFalse(lambda_func.tags)
        self.assertEqual(lambda_func.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/my-lambda?tab=configure')

    @context(module_path="lambda-permissions", test_options=TestOptions(run_drift_detection=False))
    def test_lambda_permissions(self, ctx: AwsEnvironmentContext):
        lambda_func: LambdaFunction = self._assert_lambda(ctx)
        self.assertIsNotNone(lambda_func.resource_based_policy)
        self.assertEqual(len(lambda_func.resource_based_policy.statements), 1)
        statement: PolicyStatement = lambda_func.resource_based_policy.statements[0]
        self.assertEqual(statement.effect, StatementEffect.ALLOW)
        self.assertEqual(len(statement.resources), 1)
        self.assertTrue(statement.resources[0] == f"arn:aws:lambda:us-east-1:{lambda_func.account}:function:my-lambda:v1")
        self.assertEqual(len(statement.actions), 1)
        self.assertEqual(statement.actions[0], "lambda:InvokeFunction")
        self.assertEqual(statement.principal.principal_type, PrincipalType.SERVICE)
        self.assertEqual(len(statement.principal.principal_values), 1)
        self.assertTrue(statement.principal.principal_values[0] == "s3.amazonaws.com" or
                        statement.principal.principal_values[0] == "ecr.amazonaws.com")
        self.assertEqual(len(statement.condition_block), 2)

        condition_statement: StatementCondition = next((cond for cond in statement.condition_block if cond.key == 'AWS:SourceArn'), None)
        self.assertIsNotNone(condition_statement)
        self.assertEqual(condition_statement.operator, "ArnLike")
        self.assertTrue(condition_statement.values == ['arn:aws:s3:::delete-me-eu-central-1-3214213'] or
                        condition_statement.values == ['aws_s3_bucket.bucket.arn'])

        condition_statement: StatementCondition = next((cond for cond in statement.condition_block if cond.key == 'AWS:SourceAccount'), None)
        self.assertIsNotNone(condition_statement)
        self.assertEqual(condition_statement.operator, "StringEquals")
        self.assertEqual(condition_statement.values, [self.DUMMY_ACCOUNT_ID])

    @context(module_path="lambda-alias", test_options=TestOptions(run_drift_detection=False))
    def test_lambda_alias(self, ctx: AwsEnvironmentContext):
        lambda_func: LambdaFunction = self._assert_lambda(ctx)
        alias: LambdaAlias = lambda_func.lambda_func_alias

        self.assertEqual(alias.region, 'us-east-1')
        self.assertEqual(alias.name, 'v1')
        self.assertEqual(alias.function_version, '$LATEST')
        if lambda_func.iac_state:
            self.assertEqual(alias.arn, 'aws_lambda_alias.my-lambda-alias.arn')
            self.assertEqual(alias.function_arn, 'aws_lambda_function.my-lambda.arn')
        else:
            self.assertEqual(alias.arn, f'arn:aws:lambda:us-east-1:{lambda_func.account}:function:my-lambda:v1')
            self.assertEqual(alias.function_arn, f'arn:aws:lambda:us-east-1:{lambda_func.account}:function:my-lambda')

    @context(module_path="lambda-inbound-permissions", test_options=TestOptions(run_drift_detection=False))
    def test_lambda_inbound_permissions(self, ctx: AwsEnvironmentContext):
        lambda_func: LambdaFunction = self._assert_lambda(ctx)
        user = next((user for user in ctx.users if user.name == 'user-1'), None)
        self.assertIsNotNone(user)
        inbound_connections = next((conn for conn in lambda_func.inbound_connections
                                   if isinstance(conn, PrivateConnectionDetail) and conn.target_instance == user), None)
        self.assertIsNotNone(inbound_connections)
        self.assertEqual(len(inbound_connections.connection_property.policy_evaluation), 1)
        self.assertEqual(get_allowed_actions(inbound_connections.connection_property.policy_evaluation[0]),
                         {'lambda:InvokeFunction'})

    @context(module_path="lambda-without-inbound-permissions", test_options=TestOptions(run_drift_detection=False))
    def test_lambda_without_inbound_permissions(self, ctx: AwsEnvironmentContext):
        lambda_func: LambdaFunction = self._assert_lambda(ctx)
        user = next((user for user in ctx.users if user.name == 'user-1'), None)
        self.assertIsNotNone(user)
        inbound_connection = next((conn for conn in lambda_func.inbound_connections
                                   if isinstance(conn, PrivateConnectionDetail) and conn.target_instance == user), None)
        self.assertIsNone(inbound_connection)

    @context(module_path="lambda-vpc-configuration", test_options=TestOptions(run_drift_detection=False))
    def test_lambda_vpc_configuration(self, ctx: AwsEnvironmentContext):
        lambda_func: LambdaFunction = self._assert_lambda(ctx)
        self.assertIsNotNone(lambda_func.vpc_config)

        security_group = next((sg for sg in ctx.security_groups if sg.name == 'security-group-test'))
        self.assertIsNotNone(security_group)
        self.assertEqual(len(lambda_func.vpc_config.security_groups), 1)
        self.assertEqual(lambda_func.vpc_config.security_groups[0], security_group)

        subnet = next((subnet for subnet in ctx.subnets if subnet.name == 'private-subnet-test'))
        self.assertIsNotNone(subnet)
        self.assertEqual(len(lambda_func.vpc_config.subnets), 1)
        self.assertEqual(lambda_func.vpc_config.subnets[0], subnet)
        self.assertTrue(lambda_func.network_resource.network_interfaces)

    @context(module_path="lambda-outbound-connections", test_options=TestOptions(run_drift_detection=False))
    def test_lambda_outbound_connections(self, ctx: AwsEnvironmentContext):
        lambda_func: LambdaFunction = self._assert_lambda(ctx)
        ec2 = next((ec2 for ec2 in ctx.ec2s if ec2.name == 'my-ec2-test'), None)
        self.assertIsNotNone(ec2)

        conn: ConnectionDetail = next((conn for conn in lambda_func.outbound_connections
                                      if isinstance(conn, PrivateConnectionDetail) and conn.target_instance == ec2), None)
        self.assertIsNotNone(conn)

        port_conn: PortConnectionProperty = conn.connection_property
        self.assertEqual(port_conn.cidr_block, '192.168.100.128/25')

    @context(module_path="lambda-outbound-permissions-connections", test_options=TestOptions(run_drift_detection=False))
    def test_lambda_outbound_permissions_connections(self, ctx: AwsEnvironmentContext):
        lambda_func: LambdaFunction = self._assert_lambda(ctx)
        bucket = ctx.s3_buckets['randombucketname132423']
        self.assertIsNotNone(bucket)

        conn: ConnectionDetail = next((conn for conn in lambda_func.outbound_connections
                                       if isinstance(conn, PrivateConnectionDetail) and conn.target_instance == bucket))
        self.assertIsNotNone(conn)

        policy_conn: PolicyConnectionProperty = conn.connection_property
        self.assertEqual(len(policy_conn.policy_evaluation), 1)
        policy_eval: PolicyEvaluation = policy_conn.policy_evaluation[0]
        self.assertTrue(is_any_action_allowed(policy_eval))

    @context(module_path="lambda-outbound-connections-mismatch", test_options=TestOptions(run_drift_detection=False))
    def test_lambda_outbound_connections_mismatch(self, ctx: AwsEnvironmentContext):
        lambda_func: LambdaFunction = self._assert_lambda(ctx)
        ec2 = next((ec2 for ec2 in ctx.ec2s if ec2.name == 'my-ec2-test'))
        self.assertIsNotNone(ec2)
        self.assertFalse(
            any(conn for conn in ec2.outbound_connections if isinstance(conn, PrivateConnectionDetail) and conn.target_instance == lambda_func)
        )

    @context(module_path="lambda-filter-un-used-versions", test_options=TestOptions(run_drift_detection=False))
    def test_lambda_filter_un_used_versions(self, ctx: AwsEnvironmentContext):
        self.assertTrue(
            all(
                x.is_managed_by_iac or x.lambda_func_alias or x.lambda_func_version == '$LATEST'
                for x in ctx.lambda_function_list
            )
        )

    def _assert_lambda(self, ctx: AwsEnvironmentContext) -> LambdaFunction:
        lambda_func: LambdaFunction = next((lambda_ for lambda_ in ctx.lambda_function_list if lambda_.function_name == 'my-lambda'), None)
        self.assertIsNotNone(lambda_func)
        self.assertEqual(lambda_func.handler, 'lambda_function.lambda_handler')
        self.assertEqual(lambda_func.region, 'us-east-1')
        self.assertEqual(lambda_func.runtime, 'python3.8')
        self.assertEqual(lambda_func.lambda_func_version, '$LATEST')
        if lambda_func.iac_state:
            self.assertEqual(lambda_func.execution_role_arn, 'aws_iam_role.lambda-role.arn')
        else:
            self.assertEqual(lambda_func.execution_role_arn, f'arn:aws:iam::{lambda_func.account}:role/lambda-role')
        return lambda_func

    @context(module_path="lambda_tracing_enabled")
    def test_lambda_tracing_enabled(self, ctx: AwsEnvironmentContext):
        lambda_func = next((lambda_func for lambda_func in ctx.lambda_function_list
                            if lambda_func.function_name == 'my-lambda'), None)
        self.assertIsNotNone(lambda_func)
        self.assertTrue(lambda_func.xray_tracing_enabled)

    @context(module_path="lambda_tracing_disabled")
    def test_lambda_tracing_disabled(self, ctx: AwsEnvironmentContext):
        lambda_func = next((lambda_func for lambda_func in ctx.lambda_function_list
                            if lambda_func.function_name == 'my-lambda'), None)
        self.assertIsNotNone(lambda_func)
        self.assertFalse(lambda_func.xray_tracing_enabled)

    def _assert_lambda_relations_statement(self, ctx: AwsEnvironmentContext):
        lambda_func = next((lambda_func for lambda_func in ctx.lambda_function_list
                            if lambda_func.function_name == 'ServerlessExample'), None)
        self.assertIsNotNone(lambda_func)
        self.assertTrue(lambda_func.resource_based_policy)
        self.assertEqual(lambda_func.resource_based_policy.statements[0].actions, ['lambda:InvokeFunction'])

    @context(module_path="lambda_statements_relations/link_with_arn")
    def test_lambda_statement_link_using_arn(self, ctx: AwsEnvironmentContext):
        self._assert_lambda_relations_statement(ctx)

    @context(module_path="lambda_statements_relations/link_with_function_name")
    def test_lambda_statement_link_with_function_name(self, ctx: AwsEnvironmentContext):
        self._assert_lambda_relations_statement(ctx)

    @context(module_path="lambda_statements_relations/link_with_partial_arn")
    def test_lambda_statement_link_with_partial_arn(self, ctx: AwsEnvironmentContext):
        self._assert_lambda_relations_statement(ctx)

    @context(module_path="lambda_statements_relations/link_with_using_qualifier")
    def test_lambda_statement_link_with_using_qualifier(self, ctx: AwsEnvironmentContext):
        self._assert_lambda_relations_statement(ctx)
