from abc import abstractmethod
from typing import Dict
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import LambdaAlias, create_lambda_function_arn
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLambdaAliasBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.LAMBDA_ALIAS, cfn_by_type_map)

    @abstractmethod
    def parse_resource(self, cfn_res_attr: dict) -> LambdaAlias:
        properties: dict = cfn_res_attr['Properties']
        arn: str = create_lambda_function_arn(cfn_res_attr['account_id'], cfn_res_attr['region'], properties['FunctionName'], ':' + properties['FunctionVersion'])
        return LambdaAlias(account=cfn_res_attr['account_id'],
                           region=cfn_res_attr['region'],
                           arn=arn,
                           name=properties['Name'],
                           function_name_or_arn=properties['FunctionName'],
                           function_version=properties['FunctionVersion'],
                           description=properties.get('Description', None))
