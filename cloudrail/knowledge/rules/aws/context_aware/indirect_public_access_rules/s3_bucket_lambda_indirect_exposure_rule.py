from typing import List, Dict

from cloudrail.knowledge.context.aws.resources.apigateway.rest_api_gw import RestApiGw
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class S3BucketLambdaIndirectExposureRule(AwsBaseRule):

    def get_id(self) -> str:
        return 's3_lambda_indirect_exposure'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for s3_bucket in env_context.s3_buckets:
            for agw_method in s3_bucket.exposed_to_agw_methods:
                if not self._is_api_gateway_public(agw_method.rest_api_id, env_context.rest_api_gw):
                    continue
                issues.append(Issue(evidence=f"The S3 Bucket `{s3_bucket.get_friendly_name()}`. is exposed via the execution role in "
                                             f"Lambda Function `{agw_method.integration.lambda_func_integration.get_friendly_name()}`. "
                                             f"which can be invoked by public API Gateway `{agw_method.get_friendly_name()}`",
                                    exposed=s3_bucket,
                                    violating=agw_method.integration.lambda_func_integration))

        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.s3_buckets
                    and environment_context.lambda_function_list
                    and environment_context.api_gateway_methods)

    @staticmethod
    def _is_api_gateway_public(rest_api_gw_id: str, api_gateways: List[RestApiGw]) -> bool:
        for api_gateway in api_gateways:
            if api_gateway.rest_api_gw_id == rest_api_gw_id:
                return api_gateway.is_public
        raise Exception(f'Rest API Gateway {rest_api_gw_id} could not be found')
