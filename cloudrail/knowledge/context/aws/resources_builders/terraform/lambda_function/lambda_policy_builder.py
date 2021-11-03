from typing import List

from cloudrail.knowledge.context.aws.resources.lambda_.lambda_policy import LambdaPolicy
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_lambda_policy
from cloudrail.knowledge.context.iac_action_type import IacActionType


class LambdaPolicyBuilder(AwsTerraformBuilder):

    def do_build(self, attributes) -> LambdaPolicy:
        return build_lambda_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LAMBDA_PERMISSION

    @staticmethod
    def _post_build(build_results: List[LambdaPolicy]) -> List[LambdaPolicy]:
        policy_statements = {}

        for policy in build_results:
            if policy.lambda_func_arn not in policy_statements:
                policy_statements[policy.lambda_func_arn] = [policy.statements[0]]
            else:
                policy_statements[policy.lambda_func_arn].append(policy.statements[0])

        arns = {lambda_policy.lambda_func_arn for lambda_policy in build_results}
        policies = []
        for arn in arns:
            policy = next((policy for policy in build_results
                           if policy.lambda_func_arn == arn and policy.iac_state.action != IacActionType.DELETE), None)
            if policy:
                policy.statements = policy_statements[arn]
                policies.append(policy)

        return policies
