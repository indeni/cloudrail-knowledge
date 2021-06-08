import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.aws.apigateway.rest_api_gw_policy import RestApiGwPolicy
from cloudrail.knowledge.context.aws.cloudwatch.cloudwatch_logs_destination import CloudWatchLogsDestination
from cloudrail.knowledge.context.aws.cloudwatch.cloudwatch_logs_destination_policy import CloudWatchLogsDestinationPolicy
from cloudrail.knowledge.context.aws.ecr.ecr_repository import EcrRepository
from cloudrail.knowledge.context.aws.ecr.ecr_repository_policy import EcrRepositoryPolicy
from cloudrail.knowledge.context.aws.efs.efs_policy import EfsPolicy
from cloudrail.knowledge.context.aws.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.context.aws.es.elastic_search_domain_policy import ElasticSearchDomainPolicy
from cloudrail.knowledge.context.aws.glacier.glacier_vault import GlacierVault
from cloudrail.knowledge.context.aws.glacier.glacier_vault_policy import GlacierVaultPolicy
from cloudrail.knowledge.context.aws.iam.policy import Policy, S3Policy
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.kms.kms_key_policy import KmsKeyPolicy
from cloudrail.knowledge.context.aws.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.secretsmanager.secrets_manager_secret import SecretsManagerSecret
from cloudrail.knowledge.context.aws.secretsmanager.secrets_manager_secret_policy import SecretsManagerSecretPolicy
from cloudrail.knowledge.context.aws.sqs.sqs_queue import SqsQueue
from cloudrail.knowledge.context.aws.sqs.sqs_queue_policy import SqsQueuePolicy
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureCloudWatchLogDestinationPolicyNotUseWildcard, EnsureEcrRepositoryPolicyNotUseWildcard, EnsureEfsPolicyNotUseWildcard, \
    EnsureElasticSearchDomainPolicyNotUseWildcard, \
    EnsureGlacierVaultPolicyNotUseWildcard, \
    EnsureKmsKeyPolicyNotUseWildcard, \
    EnsureLambdaFunctionPolicyNotUseWildcard, \
    EnsureRestApiGwPolicyNotUseWildcard, \
    EnsureS3BucketPolicyNotUseWildcard, \
    EnsureSecretsManagerSecretPolicyNotUseWildcard, \
    EnsureSqsQueuePolicyNotUseWildcard
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.aws.efs.efs_file_system import ElasticFileSystem


class TestEnsureLambdaFunctionPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureLambdaFunctionPolicyNotUseWildcard()

    def test_non_car_aws_lambda_func_policy_wildcard_fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
                                                                               ['lambda:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))])
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `lambda:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_lambda_func_policy_wildcard__only_action__fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
                                                                               ['lambda:*'], ['*'],
                                                                               Principal(PrincipalType.AWS, ['arn:aws:iam::123456789012:root']))])
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `lambda:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_lambda_func_policy_wildcard__only_principal__fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
                                                                               ['lambda:GetLogs'], ['*'],
                                                                               Principal(PrincipalType.PUBLIC, ['*']))])
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_lambda_func_policy_wildcard__no_policy__fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_lambda_func_policy_wildcard_pass(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
                                                                               ['lambda:GetLogs'], ['*'],
                                                                               Principal(PrincipalType.AWS, ['arn:aws:iam::123456789012:root']))])
        context = AwsEnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureKmsKeyPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureKmsKeyPolicyNotUseWildcard()

    def test_non_car_aws_kms_key_policy_wildcard_fail(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.policy = KmsKeyPolicy('kms_key', [PolicyStatement(StatementEffect.ALLOW,
                                                                  ['kms:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                      'raw_doc_string', 'account')
        kms_key.key_manager = KeyManager.CUSTOMER
        context = AwsEnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `kms:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_kms_key_policy_wildcard__only_action__fail(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.policy = KmsKeyPolicy('kms_key', [PolicyStatement(StatementEffect.ALLOW,
                                                                  ['kms:*'], ['*'],
                                                                  Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))],
                                      'raw_doc_string', 'account')
        kms_key.key_manager = KeyManager.CUSTOMER
        context = AwsEnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `kms:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_kms_key_policy_wildcard__only_principal__fail(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.policy = KmsKeyPolicy('kms_key', [PolicyStatement(StatementEffect.ALLOW,
                                                                  ['kms:GetLogs'], ['*'],
                                                                  Principal(PrincipalType.PUBLIC, ['*']))],
                                      'raw_doc_string', 'account')
        kms_key.key_manager = KeyManager.CUSTOMER
        context = AwsEnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_kms_key_policy_wildcard__no_policy__fail(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.CUSTOMER
        context = AwsEnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_kms_key_policy_wildcard_pass(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.policy = KmsKeyPolicy('kms_key', [PolicyStatement(StatementEffect.ALLOW,
                                                                  ['kms:GetLogs'], ['*'],
                                                                  Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))],
                                      'raw_doc_string', 'account')
        kms_key.key_manager = KeyManager.CUSTOMER
        context = AwsEnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_kms_key_policy_wildcard__no_customer_key__skip(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.policy = KmsKeyPolicy('kms_key', [PolicyStatement(StatementEffect.ALLOW,
                                                                  ['kms:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                      'raw_doc_string', 'account')
        kms_key.key_manager = KeyManager.AWS
        context = AwsEnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SKIPPED, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureSqsQueuePolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSqsQueuePolicyNotUseWildcard()

    def test_non_car_aws_sqs_policy_wildcard_fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.policy = SqsQueuePolicy('queue_name', [PolicyStatement(StatementEffect.ALLOW,
                                                                         ['sqs:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                          'raw_doc_string', 'account')
        context = AwsEnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `sqs:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_sqs_policy_wildcard__only_action__fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.policy = SqsQueuePolicy('queue_name', [PolicyStatement(StatementEffect.ALLOW,
                                                                         ['sqs:*'], ['*'],
                                                                         Principal(PrincipalType.AWS, ['arn:aws:iam::123456789012:root']))],
                                          'raw_doc_string', 'account')
        context = AwsEnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `sqs:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_sqs_policy_wildcard__only_principal__fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.policy = SqsQueuePolicy('queue_name', [PolicyStatement(StatementEffect.ALLOW,
                                                                         ['sqs:GetLogs'], ['*'],
                                                                         Principal(PrincipalType.PUBLIC, ['*']))],
                                          'raw_doc_string', 'account')
        context = AwsEnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_sqs_policy_wildcard__no_policy__fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        context = AwsEnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_sqs_policy_wildcard_pass(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.policy = SqsQueuePolicy('queue_name', [PolicyStatement(StatementEffect.ALLOW,
                                                                         ['sqs:GetLogs'], ['*'],
                                                                         Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))],
                                          'raw_doc_string', 'account')
        context = AwsEnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureSecretsManagerSecretPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSecretsManagerSecretPolicyNotUseWildcard()

    def test_non_car_aws_secrets_manager_secret_policy_wildcard_fail(self):
        # Arrange
        secret_manager: SecretsManagerSecret = create_empty_entity(SecretsManagerSecret)
        secret_manager.policy = SecretsManagerSecretPolicy('secret_arn', [PolicyStatement(StatementEffect.ALLOW,
                                                                                          ['secretsmanager:*'],
                                                                                          ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                                           'raw_doc_string', 'account')
        context = AwsEnvironmentContext(secrets_manager_secrets=[secret_manager])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `secretsmanager:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_secrets_manager_secret_policy_wildcard__only_action__fail(self):
        # Arrange
        secret_manager: SecretsManagerSecret = create_empty_entity(SecretsManagerSecret)
        secret_manager.policy = SecretsManagerSecretPolicy('secret_arn', [PolicyStatement(StatementEffect.ALLOW,
                                                                                          ['secretsmanager:*'],
                                                                                          ['*'],
                                                                                          Principal(PrincipalType.PUBLIC,
                                                                                                    ['arn:aws:iam::123456789012:root']))],
                                                           'raw_doc_string', 'account')
        context = AwsEnvironmentContext(secrets_manager_secrets=[secret_manager])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `secretsmanager:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_secrets_manager_secret_policy_wildcard__only_principal__fail(self):
        # Arrange
        secret_manager: SecretsManagerSecret = create_empty_entity(SecretsManagerSecret)
        secret_manager.policy = SecretsManagerSecretPolicy('secret_arn', [PolicyStatement(StatementEffect.ALLOW,
                                                                                          ['secretsmanager:GetLogs'],
                                                                                          ['*'],
                                                                                          Principal(PrincipalType.PUBLIC, ['*']))],
                                                           'raw_doc_string', 'account')
        context = AwsEnvironmentContext(secrets_manager_secrets=[secret_manager])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_secrets_manager_secret_policy_wildcard__no_policy__fail(self):
        # Arrange
        secret_manager: SecretsManagerSecret = create_empty_entity(SecretsManagerSecret)
        context = AwsEnvironmentContext(secrets_manager_secrets=[secret_manager])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_secrets_manager_secret_policy_wildcard_pass(self):
        # Arrange
        secret_manager: SecretsManagerSecret = create_empty_entity(SecretsManagerSecret)
        secret_manager.policy = SecretsManagerSecretPolicy('secret_arn', [PolicyStatement(StatementEffect.ALLOW,
                                                                                          ['secretsmanager:GetLogs'],
                                                                                          ['*'],
                                                                                          Principal(PrincipalType.PUBLIC,
                                                                                                    ['arn:aws:iam::123456789012:root']))],
                                                           'raw_doc_string', 'account')
        context = AwsEnvironmentContext(secrets_manager_secrets=[secret_manager])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureS3BucketPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureS3BucketPolicyNotUseWildcard()

    def test_non_car_aws_s3_bucket_policy_wildcard_fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.ALLOW, ['s3:*'],
                                                                                              ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                                   'raw_doc')
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `s3:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_s3_bucket_policy_wildcard__only_action__fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.ALLOW, ['s3:*'],
                                                                                              ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                               ['arn:aws:iam::123456789012:root']))],
                                                   'raw_doc')
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `s3:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_s3_bucket_policy_wildcard__only_principal__fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.ALLOW, ['s3:GetLogs'],
                                                                                              ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                                   'raw_doc')
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_s3_bucket_policy_wildcard__no_policy__fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_s3_bucket_policy_wildcard_wildcard_pass(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.ALLOW, ['s3:GetLogs'],
                                                                                              ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                               ['arn:aws:iam::123456789012:root']))],
                                                   'raw_doc')
        context = AwsEnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureRestApiGwPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureRestApiGwPolicyNotUseWildcard()

    def test_non_car_aws_api_gateway_endpoint_policy_wildcard_fail(self):
        # Arrange
        rest_api: RestApiGw = create_empty_entity(RestApiGw)
        rest_api.resource_based_policy = RestApiGwPolicy('rest_api_id', [PolicyStatement(StatementEffect.ALLOW, ['execute-api:*'],
                                                                                         ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                          ['*']))],
                                                         'raw_doc', 'account')
        context = AwsEnvironmentContext(rest_api_gw=[rest_api])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `execute-api:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_api_gateway_endpoint_policy_wildcard__only_action__fail(self):
        # Arrange
        rest_api: RestApiGw = create_empty_entity(RestApiGw)
        rest_api.resource_based_policy = RestApiGwPolicy('rest_api_id', [PolicyStatement(StatementEffect.ALLOW, ['execute-api:*'],
                                                                                         ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                          ['arn:aws:iam::123456789012:root']))],
                                                         'raw_doc', 'account')
        context = AwsEnvironmentContext(rest_api_gw=[rest_api])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `execute-api:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_api_gateway_endpoint_policy_wildcard__only_principal__fail(self):
        # Arrange
        rest_api: RestApiGw = create_empty_entity(RestApiGw)
        rest_api.resource_based_policy = RestApiGwPolicy('rest_api_id', [PolicyStatement(StatementEffect.ALLOW, ['execute-api:GetLogs'],
                                                                                         ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                          ['*']))],
                                                         'raw_doc', 'account')
        context = AwsEnvironmentContext(rest_api_gw=[rest_api])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_api_gateway_endpoint_policy_wildcard__no_policy__fail(self):
        # Arrange
        rest_api: RestApiGw = create_empty_entity(RestApiGw)
        context = AwsEnvironmentContext(rest_api_gw=[rest_api])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_api_gateway_endpoint_policy_wildcard_pass(self):
        # Arrange
        rest_api: RestApiGw = create_empty_entity(RestApiGw)
        rest_api.resource_based_policy = RestApiGwPolicy('rest_api_id', [PolicyStatement(StatementEffect.ALLOW, ['execute-api:GetLogs'],
                                                                                         ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                          ['arn:aws:iam::123456789012:root']))],
                                                         'raw_doc', 'account')
        context = AwsEnvironmentContext(rest_api_gw=[rest_api])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureGlacierVaultPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureGlacierVaultPolicyNotUseWildcard()

    def test_non_car_aws_glacier_vault_policy_wildcard_fail(self):
        # Arrange
        gc_vault: GlacierVault = create_empty_entity(GlacierVault)
        gc_vault.policy = GlacierVaultPolicy('vault_arn', [PolicyStatement(StatementEffect.ALLOW, ['glacier:*'],
                                                                           ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                             'raw_doc', 'account')
        context = AwsEnvironmentContext(glacier_vaults=[gc_vault])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `glacier:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_glacier_vault_policy_wildcard__only_action__fail(self):
        # Arrange
        gc_vault: GlacierVault = create_empty_entity(GlacierVault)
        gc_vault.policy = GlacierVaultPolicy('vault_arn', [PolicyStatement(StatementEffect.ALLOW, ['glacier:*'],
                                                                           ['*'], Principal(PrincipalType.PUBLIC,
                                                                                            ['arn:aws:iam::123456789012:root']))],
                                             'raw_doc', 'account')
        context = AwsEnvironmentContext(glacier_vaults=[gc_vault])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `glacier:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_glacier_vault_policy_wildcard__only_principal__fail(self):
        # Arrange
        gc_vault: GlacierVault = create_empty_entity(GlacierVault)
        gc_vault.policy = GlacierVaultPolicy('vault_arn', [PolicyStatement(StatementEffect.ALLOW, ['glacier:GetLogs'],
                                                                           ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                             'raw_doc', 'account')
        context = AwsEnvironmentContext(glacier_vaults=[gc_vault])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_glacier_vault_policy_wildcard__no_policy__fail(self):
        # Arrange
        gc_vault: GlacierVault = create_empty_entity(GlacierVault)
        context = AwsEnvironmentContext(glacier_vaults=[gc_vault])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_glacier_vault_policy_wildcard_pass(self):
        # Arrange
        gc_vault: GlacierVault = create_empty_entity(GlacierVault)
        gc_vault.policy = GlacierVaultPolicy('vault_arn', [PolicyStatement(StatementEffect.ALLOW, ['glacier:GetLogs'],
                                                                           ['*'], Principal(PrincipalType.PUBLIC,
                                                                                            ['arn:aws:iam::123456789012:root']))],
                                             'raw_doc', 'account')
        context = AwsEnvironmentContext(glacier_vaults=[gc_vault])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureElasticSearchDomainPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureElasticSearchDomainPolicyNotUseWildcard()

    def test_non_car_aws_es_service_domain_policy_wildcard_fail(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        es_domain.policy = ElasticSearchDomainPolicy('es_domain', [PolicyStatement(StatementEffect.ALLOW, ['es:*'],
                                                                                   ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                                     'raw_doc', 'account')
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `es:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_es_service_domain_policy_wildcard__only_action__fail(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        es_domain.policy = ElasticSearchDomainPolicy('es_domain', [PolicyStatement(StatementEffect.ALLOW, ['es:*'],
                                                                                   ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                    ['arn:aws:iam::123456789012:root']))],
                                                     'raw_doc', 'account')
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `es:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_es_service_domain_policy_wildcard__only_principal__fail(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        es_domain.policy = ElasticSearchDomainPolicy('es_domain', [PolicyStatement(StatementEffect.ALLOW, ['es:GetLogs'],
                                                                                   ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                                     'raw_doc', 'account')
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_es_service_domain_policy_wildcard__no_policy__fail(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_es_service_domain_policy_wildcard_pass(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        es_domain.policy = ElasticSearchDomainPolicy('es_domain', [PolicyStatement(StatementEffect.ALLOW, ['es:GetLogs'],
                                                                                   ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                    ['arn:aws:iam::123456789012:root']))],
                                                     'raw_doc', 'account')
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureEfsPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureEfsPolicyNotUseWildcard()

    def test_non_car_aws_efs_fs_policy_wildcard_fail(self):
        # Arrange
        efs: ElasticFileSystem = create_empty_entity(ElasticFileSystem)
        efs.policy = EfsPolicy('efs_id', [PolicyStatement(StatementEffect.ALLOW, ['elasticfilesystem:*'],
                                                          ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                               'raw_doc', 'account')
        context = AwsEnvironmentContext(efs_file_systems=[efs])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `elasticfilesystem:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_efs_fs_policy_wildcard__only_action__fail(self):
        # Arrange
        efs: ElasticFileSystem = create_empty_entity(ElasticFileSystem)
        efs.policy = EfsPolicy('efs_id', [PolicyStatement(StatementEffect.ALLOW, ['elasticfilesystem:*'],
                                                          ['*'], Principal(PrincipalType.PUBLIC,
                                                                           ['arn:aws:iam::123456789012:root']))],
                               'raw_doc', 'account')
        context = AwsEnvironmentContext(efs_file_systems=[efs])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `elasticfilesystem:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_efs_fs_policy_wildcard__only_principal__fail(self):
        # Arrange
        efs: ElasticFileSystem = create_empty_entity(ElasticFileSystem)
        efs.policy = EfsPolicy('efs_id', [PolicyStatement(StatementEffect.ALLOW, ['elasticfilesystem:GetLogs'],
                                                          ['*'], Principal(PrincipalType.PUBLIC,
                                                                           ['*']))],
                               'raw_doc', 'account')
        context = AwsEnvironmentContext(efs_file_systems=[efs])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_efs_fs_policy_wildcard__no_policy__fail(self):
        # Arrange
        efs: ElasticFileSystem = create_empty_entity(ElasticFileSystem)
        context = AwsEnvironmentContext(efs_file_systems=[efs])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_efs_fs_policy_wildcard_pass(self):
        # Arrange
        efs: ElasticFileSystem = create_empty_entity(ElasticFileSystem)
        efs.policy = EfsPolicy('efs_id', [PolicyStatement(StatementEffect.ALLOW, ['elasticfilesystem:GetLogs'],
                                                          ['*'], Principal(PrincipalType.PUBLIC,
                                                                           ['arn:aws:iam::123456789012:root']))],
                               'raw_doc', 'account')
        context = AwsEnvironmentContext(efs_file_systems=[efs])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureEcrRepositoryPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureEcrRepositoryPolicyNotUseWildcard()

    def test_non_car_aws_ecr_repo_policy_wildcard_fail(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        ecr_repo.policy = EcrRepositoryPolicy('repo_name', [PolicyStatement(StatementEffect.ALLOW, ['ecr:*'],
                                                                            ['*'], Principal(PrincipalType.PUBLIC,
                                                                                             ['*']))],
                                              'raw_doc', 'account')
        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `ecr:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_ecr_repo_policy_wildcard__only_action__fail(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        ecr_repo.policy = EcrRepositoryPolicy('repo_name', [PolicyStatement(StatementEffect.ALLOW, ['ecr:*'],
                                                                            ['*'], Principal(PrincipalType.PUBLIC,
                                                                                             ['arn:aws:iam::123456789012:root']))],
                                              'raw_doc', 'account')
        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `ecr:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_ecr_repo_policy_wildcard__only_principal__fail(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        ecr_repo.policy = EcrRepositoryPolicy('repo_name', [PolicyStatement(StatementEffect.ALLOW, ['ecr:GetLogs'],
                                                                            ['*'], Principal(PrincipalType.PUBLIC,
                                                                                             ['*']))],
                                              'raw_doc', 'account')
        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_ecr_repo_policy_wildcard__no_policy__fail(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_ecr_repo_policy_wildcard_pass(self):
        # Arrange
        ecr_repo: EcrRepository = create_empty_entity(EcrRepository)
        ecr_repo.policy = EcrRepositoryPolicy('repo_name', [PolicyStatement(StatementEffect.ALLOW, ['ecr:GetLogs'],
                                                                            ['*'], Principal(PrincipalType.PUBLIC,
                                                                                             ['arn:aws:iam::123456789012:root']))],
                                              'raw_doc', 'account')
        context = AwsEnvironmentContext(ecr_repositories=[ecr_repo])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureCloudWatchLogDestinationPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudWatchLogDestinationPolicyNotUseWildcard()

    def test_non_car_aws_cloudwatch_logs_destination_policy_wildcard_fail(self):
        # Arrange
        cloudwatch_dest: CloudWatchLogsDestination = create_empty_entity(CloudWatchLogsDestination)
        cloudwatch_dest.policy = CloudWatchLogsDestinationPolicy('dest_name', [PolicyStatement(StatementEffect.ALLOW, ['logs:*'],
                                                                                               ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                                ['*']))],
                                                                 'raw_doc', 'us-east-1', 'account')
        context = AwsEnvironmentContext(cloudwatch_logs_destinations=[cloudwatch_dest])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `logs:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_cloudwatch_logs_destination_policy_wildcard__only_action__fail(self):
        # Arrange
        cloudwatch_dest: CloudWatchLogsDestination = create_empty_entity(CloudWatchLogsDestination)
        cloudwatch_dest.policy = CloudWatchLogsDestinationPolicy('dest_name', [PolicyStatement(StatementEffect.ALLOW, ['logs:*'],
                                                                                               ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                                ['arn:aws:iam::123456789012:root']))],
                                                                 'raw_doc', 'us-east-1', 'account')
        context = AwsEnvironmentContext(cloudwatch_logs_destinations=[cloudwatch_dest])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `logs:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_cloudwatch_logs_destination_policy_wildcard__only_principal__fail(self):
        # Arrange
        cloudwatch_dest: CloudWatchLogsDestination = create_empty_entity(CloudWatchLogsDestination)
        cloudwatch_dest.policy = CloudWatchLogsDestinationPolicy('dest_name', [PolicyStatement(StatementEffect.ALLOW, ['logs:GetLogs'],
                                                                                               ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                                ['*']))],
                                                                 'raw_doc', 'us-east-1', 'account')
        context = AwsEnvironmentContext(cloudwatch_logs_destinations=[cloudwatch_dest])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_cloudwatch_logs_destination_policy_wildcard__no_policy__fail(self):
        # Arrange
        cloudwatch_dest: CloudWatchLogsDestination = create_empty_entity(CloudWatchLogsDestination)
        context = AwsEnvironmentContext(cloudwatch_logs_destinations=[cloudwatch_dest])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_cloudwatch_logs_destination_policy_wildcard_pass(self):
        # Arrange
        cloudwatch_dest: CloudWatchLogsDestination = create_empty_entity(CloudWatchLogsDestination)
        cloudwatch_dest.policy = CloudWatchLogsDestinationPolicy('dest_name', [PolicyStatement(StatementEffect.ALLOW, ['logs:GetLogs'],
                                                                                               ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                                ['arn:aws:iam::123456789012:root']))],
                                                                 'raw_doc', 'us-east-1', 'account')
        context = AwsEnvironmentContext(cloudwatch_logs_destinations=[cloudwatch_dest])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
