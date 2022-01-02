from typing import List

from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.abstract_policy_wildcard_violation_rule \
    import AbstractPolicyWildcardViolationRule
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.aws_policied_resource import PoliciedResource
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager


class EnsureCloudWatchLogDestinationPolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):
    def _get_violating_actions(self) -> List[str]:
        return ['logs:*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return env_context.cloudwatch_logs_destinations

    def get_id(self) -> str:
        return "non_car_aws_cloudwatch_logs_destination_policy_wildcard"


class EnsureEcrRepositoryPolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):

    def _get_violating_actions(self) -> List[str]:
        return ['ecr:*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return env_context.ecr_repositories

    def get_id(self) -> str:
        return "non_car_aws_ecr_repo_policy_wildcard"


class EnsureEfsPolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):
    def _get_violating_actions(self) -> List[str]:
        return ['elasticfilesystem:*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return env_context.efs_file_systems

    def get_id(self) -> str:
        return 'non_car_aws_efs_fs_policy_wildcard'


class EnsureElasticSearchDomainPolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):
    def _get_violating_actions(self) -> List[str]:
        return ['es:*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return env_context.elastic_search_domains

    def get_id(self) -> str:
        return "non_car_aws_es_service_domain_policy_wildcard"


class EnsureGlacierVaultPolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):
    def _get_violating_actions(self) -> List[str]:
        return ['glacier:*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return env_context.glacier_vaults

    def get_id(self) -> str:
        return "non_car_aws_glacier_vault_policy_wildcard"


class EnsureRestApiGwPolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):
    def _get_violating_actions(self) -> List[str]:
        return ['execute-api:*', 'execute-api:/*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return env_context.rest_api_gw

    def get_id(self) -> str:
        return "non_car_aws_api_gateway_endpoint_policy_wildcard"


class EnsureS3BucketPolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):

    def _get_violating_actions(self) -> List[str]:
        return ['s3:*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return env_context.s3_buckets

    def get_id(self) -> str:
        return "non_car_aws_s3_bucket_policy_wildcard"


class EnsureSecretsManagerSecretPolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):

    def _get_violating_actions(self) -> List[str]:
        return ['secretsmanager:*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return env_context.secrets_manager_secrets

    def get_id(self) -> str:
        return "non_car_aws_secrets_manager_secret_policy_wildcard"


class EnsureSqsQueuePolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):

    def _get_violating_actions(self) -> List[str]:
        return ['sqs:*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return env_context.sqs_queues

    def get_id(self) -> str:
        return "non_car_aws_sqs_policy_wildcard"


class EnsureKmsKeyPolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):

    def _get_violating_actions(self) -> List[str]:
        return ['kms:*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return [kms_key for kms_key in env_context.kms_keys if kms_key.key_manager == KeyManager.CUSTOMER]

    def get_id(self) -> str:
        return "non_car_aws_kms_key_policy_wildcard"


class EnsureLambdaFunctionPolicyNotUseWildcard(AbstractPolicyWildcardViolationRule):

    def _get_violating_actions(self) -> List[str]:
        return ['lambda:*']

    def _get_context_policy_resources(self, env_context: AwsEnvironmentContext) -> List[PoliciedResource]:
        return env_context.lambda_function_list

    def get_id(self) -> str:
        return "non_car_aws_lambda_func_policy_wildcard"
