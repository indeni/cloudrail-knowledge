from typing import List, Optional, Set
from botocore.utils import ArnParser
from cloudrail.knowledge.context.aws.resources.aws_client import AwsClient
from cloudrail.knowledge.context.aws.resources.aws_policied_resource import PoliciedResource
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloud_watch_log_group import CloudWatchLogGroup
from cloudrail.knowledge.context.aws.resources.lambda_.lambda_alias import create_lambda_function_arn, LambdaAlias
from cloudrail.knowledge.context.aws.resources.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceAttributes, AwsServiceName, AwsServiceType
from cloudrail.knowledge.utils.arn_utils import are_arns_intersected, is_valid_arn
from cloudrail.knowledge.utils.tags_utils import filter_tags


class LambdaFunction(NetworkEntity, PoliciedResource, AwsClient):
    """
        Attributes:
            arn: The ARN of the function.
            function_name: The name of the function.
            lambda_func_version: The version of the function.
            role_arn: The ARN of the role the Lambda Function is set to use.
            handler: The function handler in the Lambda code.
            runtime: The runtime used with the specific Lambda Function.
            vpc_config: The VPC configuration of the Lambda Function, if one was set.
            log_group: The matching log group associated with the Lambda Function.
            xray_tracing_enabled: Indication if X-Ray tracing is enabled for incoming requests.
    """

    ARN_PARSER: ArnParser = ArnParser()

    def __init__(self, account: str, region: str, arn: str, qualified_arn: str, function_name: str,
                 lambda_func_version: str, role_arn: str, handler: str,
                 runtime: str, vpc_config: NetworkConfiguration, xray_tracing_enabled: bool):
        NetworkEntity.__init__(self, function_name, account, region, AwsServiceName.AWS_LAMBDA_FUNCTION,
                               AwsServiceAttributes(aws_service_type=AwsServiceType.LAMBDA.value, region=region))
        PoliciedResource.__init__(self, account, region, AwsServiceName.AWS_LAMBDA_FUNCTION,
                                  AwsServiceAttributes(aws_service_type=AwsServiceType.LAMBDA.value, region=region))
        AwsClient.__init__(self)
        self.lambda_func_arn_set: Set[str] = {arn, qualified_arn, create_lambda_function_arn(account, region, function_name, lambda_func_version)}
        self.arn: str = arn
        self.qualified_arn: str = qualified_arn
        self.function_name: str = function_name
        self.lambda_func_version: str = lambda_func_version
        self.execution_role_arn: str = role_arn
        self.handler: str = handler
        self.runtime: str = runtime
        self.vpc_config: NetworkConfiguration = vpc_config
        self.lambda_func_alias: Optional[LambdaAlias] = None
        self.log_group: CloudWatchLogGroup = None
        self.xray_tracing_enabled: bool = xray_tracing_enabled

    def get_keys(self) -> List[str]:
        return [self._get_simplified_arn()]

    def get_name(self) -> str:
        return self.function_name

    def get_arn(self) -> str:
        return self.arn

    def is_arn_match(self, arn: str):
        return any(arn == a or are_arns_intersected(arn, a) for a in self.lambda_func_arn_set)

    def get_qualifier(self) -> str:
        if self.lambda_func_alias:
            return self.lambda_func_alias.name
        return self.parse_qualifier_from_arn(self.arn)

    def get_all_network_configurations(self) -> List[NetworkConfiguration]:
        return [NetworkConfiguration(self.vpc_config.assign_public_ip, self.vpc_config.security_groups_ids, self.vpc_config.subnet_list_ids)]

    @staticmethod
    def parse_qualifier_from_arn(qualified_arn: str) -> Optional[str]:
        if is_valid_arn(qualified_arn):
            arn_sections_dict: dict = LambdaFunction.ARN_PARSER.parse_arn(qualified_arn)
            resource_parts: List[str] = arn_sections_dict['resource'].split(':')
            if len(resource_parts) == 3:
                return resource_parts[-1]
        return None

    def get_id(self) -> str:
        return self.get_arn()  # todo - conflicts with CFN Ref Doc

    def get_cloud_resource_url(self) -> str:
        return '{0}lambda/home?region={1}#/functions/{2}?tab=configure' \
            .format(self.AWS_CONSOLE_URL, self.region, self.function_name)

    def get_friendly_name(self) -> str:
        if self.is_managed_by_iac:
            return self.iac_state.address
        return self.get_arn()

    @property
    def is_tagable(self) -> bool:
        return True

    def _get_simplified_arn(self) -> str:
        if not self.qualified_arn:
            return ''
        return "".join(self.qualified_arn.split(":")[:-1]) if ':' in self.qualified_arn else self.qualified_arn

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'function_name': self.function_name,
                'role_arn': self.execution_role_arn,
                'handler': self.handler,
                'runtime': self.runtime,
                'assign_public_ip': self.vpc_config and self.vpc_config.assign_public_ip,
                'security_groups_ids': self.vpc_config and self.vpc_config.security_groups_ids,
                'subnet_list_ids': self.vpc_config and self.vpc_config.subnet_list_ids,
                'xray_tracing_enabled': self.xray_tracing_enabled}
