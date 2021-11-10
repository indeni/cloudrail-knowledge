from typing import Dict

from cloudrail.knowledge.context.aws.resources.configservice.config_aggregator import ConfigAggregator
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationConfigServiceAggregatorBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CONFIG_SERVICE_AGGREGATOR, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> ConfigAggregator:
        properties: dict = cfn_res_attr['Properties']
        aggregator_name = self.get_property(properties, 'ConfigurationAggregatorName', self.get_resource_id(cfn_res_attr))
        account=cfn_res_attr['account_id']
        region=cfn_res_attr['region']
        arn = build_arn('config', region, account, 'config-aggregator/', 'config-aggregator-', self.create_random_pseudo_identifier())
        organization_aggregation_all_regions_enabled = None
        account_aggregation_all_regions_enabled = None
        account_aggregation_used = bool(properties.get('AccountAggregationSources'))
        if account_aggregation_used:
            account_aggregation_all_regions_enabled = bool(properties['AccountAggregationSources'][0].get('AllAwsRegions'))
        organization_aggregation_used = bool(properties.get('OrganizationAggregationSource'))
        if organization_aggregation_used:
            organization_aggregation_all_regions_enabled = bool(properties['OrganizationAggregationSource'].get('AllAwsRegions'))
        return ConfigAggregator(account=account, region=region, aggregator_name=aggregator_name, arn=arn, account_aggregation_used=account_aggregation_used,
                                organization_aggregation_used=organization_aggregation_used, organization_aggregation_all_regions_enabled=organization_aggregation_all_regions_enabled,
                                account_aggregation_all_regions_enabled=account_aggregation_all_regions_enabled)
