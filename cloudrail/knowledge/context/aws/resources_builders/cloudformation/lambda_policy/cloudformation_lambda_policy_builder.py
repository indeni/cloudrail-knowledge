from abc import abstractmethod
from typing import Dict, List
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect, \
    StatementCondition
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import create_lambda_function_arn
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_policy import LambdaPolicy
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLambdaPolicyBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.LAMBDA_PERMISSION, cfn_by_type_map)

    @abstractmethod
    def parse_resource(self, cfn_res_attr: dict) -> LambdaPolicy:
        account_id: str = cfn_res_attr['account_id']
        region: str = cfn_res_attr['region']
        properties: dict = cfn_res_attr['Properties']
        lambda_function_name: str = self.get_property(properties, 'FunctionName', self.get_resource_id(cfn_res_attr)).split(':')[-2]
        qualifier: str = self.get_property(properties, 'FunctionName', self.get_resource_id(cfn_res_attr)).split(':')[-1]
        principal_type: PrincipalType = PrincipalType.NO_PRINCIPAL
        if properties['Principal'].isnumeric() or ':' in properties['Principal']:
            principal_type = PrincipalType.AWS
        elif properties['Principal'].endswith(".com"):
            principal_type = PrincipalType.SERVICE
        principal: Principal = Principal(principal_type, [properties['Principal']])

        condition_block: List[StatementCondition] = [
            StatementCondition("ArnLike", "AWS:SourceArn", [properties.get('SourceArn')])] \
            if properties.get('SourceArn', None) else []
        if properties.get('SourceAccount', None):
            condition_block.append(
                StatementCondition("StringEquals", "AWS:SourceAccount", [properties.get('SourceAccount')]))

        statement: PolicyStatement = PolicyStatement(effect=StatementEffect.ALLOW,
                                                     actions=[properties['Action']],
                                                     resources=[
                                                         create_lambda_function_arn(account_id, cfn_res_attr['region'],
                                                                                    lambda_function_name, qualifier)
                                                         ],
                                                     principal=principal,
                                                     condition_block=condition_block)
        return LambdaPolicy(account=account_id,
                            region=region,
                            function_name=lambda_function_name,
                            statements=[statement],
                            qualifier=qualifier)

