from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSageMakerEndpointConfigEncryptedAtRestRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'not_car_sagemaker_endpoint_configurations_encrypt_data_at_rest'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for sage_end_config in env_context.sagemaker_endpoint_config_list:
            if sage_end_config.is_new_resource() and not sage_end_config.encrypted:
                issues.append(
                    Issue(
                        f'The {sage_end_config.get_type()} `{sage_end_config.get_friendly_name()}` is not set to encrypt data at rest'
                        , sage_end_config, sage_end_config))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.sagemaker_endpoint_config_list)
