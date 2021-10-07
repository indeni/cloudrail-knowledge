from typing import Dict
import json

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloudwatch_logs_destination import CloudWatchLogsDestination
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloudwatch_logs_destination_policy import CloudWatchLogsDestinationPolicy
from cloudrail.knowledge.utils.arn_utils import build_arn
from cloudrail.knowledge.context.environment_context.common_component_builder import build_policy_statement

class CloudformationCloudwatchLogsDestinationBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CLOUDWATCH_LOGS_DESTINATION, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> CloudWatchLogsDestination:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        name = properties['DestinationName']
        arn = build_arn('logs', region, account, 'destination', None, name)
        return CloudWatchLogsDestination(account=account, region=region, name=name, arn=arn)

class CloudformationCloudwatchLogsDestinationPolicyBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CLOUDWATCH_LOGS_DESTINATION, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> CloudWatchLogsDestinationPolicy:
        properties: dict = cfn_res_attr['Properties']
        region = cfn_res_attr['region']
        account = cfn_res_attr['account_id']
        name = properties['DestinationName']
        policy_statements = [build_policy_statement(raw_statement) for raw_statement in json.loads(properties['DestinationPolicy'])['Statement']]
        return CloudWatchLogsDestinationPolicy(account=account, region=region, destination_name=name,
                                               policy_statements=policy_statements, raw_document=properties['DestinationPolicy'])
