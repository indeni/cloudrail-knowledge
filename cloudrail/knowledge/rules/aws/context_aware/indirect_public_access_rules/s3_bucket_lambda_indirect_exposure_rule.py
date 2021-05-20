from typing import List, Dict, Tuple

from cloudrail.knowledge.context.aws.aws_connection import PolicyEvaluation
from cloudrail.knowledge.context.aws.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.iam.policy import Policy
from cloudrail.knowledge.context.aws.resource_based_policy import ResourceBasedPolicy
from cloudrail.knowledge.context.aws.apigateway.api_gateway_method import ApiGatewayMethod
from cloudrail.knowledge.context.aws.apigateway.rest_api_gw import ApiGatewayType, RestApiGw
from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils.policy_evaluator import PolicyEvaluator, is_action_subset_allowed
from cloudrail.knowledge.utils.policy_utils import is_policy_block_public_access


class S3BucketLambdaIndirectExposureRule(AwsBaseRule):

    def get_id(self) -> str:
        return 's3_lambda_indirect_exposure'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        api_gateway_to_methods_map: Dict[str, Tuple[RestApiGw, List[ApiGatewayMethod]]] = \
            self._init_api_gateway_to_methods_map(env_context.rest_api_gw)
        self._add_methods_to_api_gateway_map(api_gateway_to_methods_map, env_context.api_gateway_methods)

        for _, agw_methods in api_gateway_to_methods_map.values():
            for agw_method in agw_methods:
                for resource_arn, evaluation_results in agw_method.integration.lambda_func_integration.iam_role.policy_evaluation_result_map.items():
                    if resource_arn in env_context.s3_buckets.keys() and \
                            self._is_all_bucket_resources_allowed(evaluation_results,
                                                                  agw_method.integration.lambda_func_integration.iam_role.permissions_policies):
                        s3_bucket: S3Bucket = env_context.s3_buckets.get(resource_arn)
                        issues.append(Issue(evidence=f"The S3 Bucket `{s3_bucket.get_friendly_name()}`. is exposed via the execution role in "
                                                     f"Lambda Function `{agw_method.integration.lambda_func_integration.get_friendly_name()}`. "
                                                     f"which can be invoked by public API Gateway `{agw_method.get_friendly_name()}`",
                                            exposed=s3_bucket,
                                            violating=agw_method.integration.lambda_func_integration))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.s3_buckets
                    and environment_context.lambda_function_list
                    and environment_context.api_gateway_methods)

    @classmethod
    def _init_api_gateway_to_methods_map(cls, api_gateways: List[RestApiGw]) -> Dict[str, Tuple[RestApiGw, List[ApiGatewayMethod]]]:
        api_gateway_to_methods_map: Dict[str, Tuple[RestApiGw, List[ApiGatewayMethod]]] = {}
        for api_gateway in api_gateways:
            if api_gateway.api_gateway_type != ApiGatewayType.PRIVATE and \
                    (api_gateway.resource_based_policy is None or cls._is_policy_publicly_allow(api_gateway)):
                api_gateway_to_methods_map[api_gateway.rest_api_gw_id] = (api_gateway, [])
        return api_gateway_to_methods_map

    @staticmethod
    def _is_policy_publicly_allow(agw_resource: ResourceBasedPolicy) -> bool:
        return not is_policy_block_public_access(agw_resource.resource_based_policy)

    @classmethod
    def _add_methods_to_api_gateway_map(cls, api_gateway_to_methods_map: Dict[str, Tuple[RestApiGw, List[ApiGatewayMethod]]],
                                        api_gateway_methods: List[ApiGatewayMethod]):
        if api_gateway_to_methods_map:
            for agw_method in api_gateway_methods:
                if agw_method.rest_api_id in api_gateway_to_methods_map:
                    api_gateway, methods = api_gateway_to_methods_map[agw_method.rest_api_id]
                    if agw_method.integration and \
                            agw_method.integration.lambda_func_integration and \
                            cls._is_lambda_policy_allow_access_to_api_gateway(api_gateway, agw_method.integration.lambda_func_integration):
                        methods.append(agw_method)

    @staticmethod
    def _is_lambda_policy_allow_access_to_api_gateway(api_gateway: RestApiGw, lambda_func: LambdaFunction) -> bool:
        evaluation_results: PolicyEvaluation = PolicyEvaluator.evaluate_actions(source=api_gateway, destination=lambda_func,
                                                                                resource_based_policies=[lambda_func.resource_based_policy],
                                                                                identity_based_policies=[],
                                                                                permission_boundary=None)
        return is_action_subset_allowed(evaluation_results, 'lambda:InvokeFunction')

    @staticmethod
    def _is_all_bucket_resources_allowed(results: PolicyEvaluation, policies: List[Policy]):
        if is_action_subset_allowed(results, 's3:*'):
            for statement in [statement for policy in policies for statement in policy.statements]:
                if any(resource == '*' for resource in statement.resources) and \
                        any(action.startswith('s3:') or action == '*' for action in statement.actions):
                    return True
        return False
