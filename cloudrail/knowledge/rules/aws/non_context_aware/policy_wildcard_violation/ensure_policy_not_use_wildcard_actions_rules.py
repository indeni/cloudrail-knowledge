from abc import abstractmethod

from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.abstract_policy_wildcard_violation_rule \
    import AbstractPolicyWildcardViolationRule


class EnsurePolicyNotUseWildcardRules(AbstractPolicyWildcardViolationRule):

    @abstractmethod
    def get_id(self) -> str:
        pass


class EnsureCloudWatchLogDestinationPolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('CloudWatch Logs Destination',
                         'cloudwatch_logs_destinations',
                         ['logs:*'])

    def get_id(self) -> str:
        return "non_car_aws_cloudwatch_logs_destination_policy_wildcard"


class EnsureEcrRepositoryPolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('ECR repository',
                         'ecr_repositories',
                         ['ecr:*'])

    def get_id(self) -> str:
        return "non_car_aws_ecr_repo_policy_wildcard"


class EnsureEfsPolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('EFS file system',
                         'efs_file_systems',
                         ['elasticfilesystem:*'])

    def get_id(self) -> str:
        return "non_car_aws_efs_fs_policy_wildcard"


class EnsureElasticSearchDomainPolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('Elasticsearch Service domain',
                         'elastic_search_domains',
                         ['es:*'])

    def get_id(self) -> str:
        return "non_car_aws_es_service_domain_policy_wildcard"


class EnsureGlacierVaultPolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('S3 Glacier vault',
                         'glacier_vaults',
                         ['glacier:*'])

    def get_id(self) -> str:
        return "non_car_aws_glacier_vault_policy_wildcard"


class EnsureRestApiGwPolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('API Gateway endpoint',
                         'rest_api_gw',
                         ['execute-api:*', 'execute-api:/*'])

    def get_id(self) -> str:
        return "non_car_aws_api_gateway_endpoint_policy_wildcard"


class EnsureS3BucketPolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('S3 bucket',
                         's3_buckets',
                         ['s3:*'])

    def get_id(self) -> str:
        return "non_car_aws_s3_bucket_policy_wildcard"


class EnsureSecretsManagerSecretPolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('Secrets Manager secret',
                         'secrets_manager_secrets',
                         ['secretsmanager:*'])

    def get_id(self) -> str:
        return "non_car_aws_secrets_manager_secret_policy_wildcard"


class EnsureSqsQueuePolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('SQS queue',
                         'sqs_queues',
                         ['sqs:*'])

    def get_id(self) -> str:
        return "non_car_aws_sqs_policy_wildcard"


class EnsureKmsKeyPolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('KMS key',
                         'kms_keys',
                         ['kms:*'])

    def get_id(self) -> str:
        return "non_car_aws_kms_key_policy_wildcard"


class EnsureLambdaFunctionPolicyNotUseWildcard(EnsurePolicyNotUseWildcardRules):

    def __init__(self) -> None:
        super().__init__('Lambda function',
                         'lambda_function_list',
                         ['lambda:*'])

    def get_id(self) -> str:
        return "non_car_aws_lambda_func_policy_wildcard"
