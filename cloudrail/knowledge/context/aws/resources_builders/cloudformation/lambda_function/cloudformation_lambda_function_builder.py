from abc import abstractmethod
from typing import Dict, Optional
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import create_lambda_function_arn
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationLambdaFunctionBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.LAMBDA_FUNCTION, cfn_by_type_map)

    @abstractmethod
    def parse_resource(self, cfn_res_attr: dict) -> LambdaFunction:
        properties: dict = cfn_res_attr['Properties']
        vpc_config: Optional[NetworkConfiguration] = None
        if 'VpcConfig' in properties:
            vpc_config_dict: dict = self.get_property(properties, 'VpcConfig')
            vpc_config = NetworkConfiguration(False, self.get_property(vpc_config_dict, 'SecurityGroupIds'),
                                              self.get_property(vpc_config_dict, 'SubnetIds'))
        account_id: str = cfn_res_attr['account_id']
        region: str = cfn_res_attr['region']
        func_name: str = self.get_property(properties, 'FunctionName', self.get_resource_id(cfn_res_attr))
        lambda_func_version = '$LATEST'
        func_arn: str = create_lambda_function_arn(account_id, region, func_name, ':' + lambda_func_version)
        xray_tracing_enabled: bool = bool(properties.get('TracingConfig', {}).get('Mode') == 'Active')
        return LambdaFunction(account=account_id,
                              region=region,
                              function_name=func_name,
                              lambda_func_version=lambda_func_version,
                              arn=func_arn,
                              qualified_arn=func_arn,
                              role_arn=self.get_property(properties, 'Role'),
                              handler=self.get_property(properties, 'Handler'),
                              runtime=self.get_property(properties, 'Runtime'),
                              vpc_config=vpc_config,
                              xray_tracing_enabled=xray_tracing_enabled)
