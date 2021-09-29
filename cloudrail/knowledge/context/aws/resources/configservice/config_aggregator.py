from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ConfigAggregator(AwsResource):
    """
        Attributes:
            aggregator_name: The name of the Config Aggregator.
            arn: The ARN of the Config Aggregator.
            account_aggregation_used: An indication if the aggregation data is set for the account.
            organization_aggregation_used: An indication if the aggregation data is set for the organization.
            account_aggregation_all_regions_enabled: An indication if the account to aggregate data is enabled on all regions.
            organization_aggregation_all_regions_enabled: An indication if the organization to aggregate data is enabled on all regions.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 aggregator_name: str,
                 arn: str,
                 account_aggregation_used: bool,
                 organization_aggregation_used: bool,
                 account_aggregation_all_regions_enabled: Optional[bool],
                 organization_aggregation_all_regions_enabled: Optional[bool]):
        super().__init__(account, region, AwsServiceName.AWS_CONFIG_CONFIGURATION_AGGREGATOR)
        self.aggregator_name: str = aggregator_name
        self.arn: str = arn
        self.account_aggregation_used: bool = account_aggregation_used
        self.organization_aggregation_used: bool = organization_aggregation_used
        self.account_aggregation_all_regions_enabled: Optional[bool] = account_aggregation_all_regions_enabled
        self.organization_aggregation_all_regions_enabled: Optional[bool] = organization_aggregation_all_regions_enabled

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.aggregator_name

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> str:
        return '{0}config/home?region={1}#/aggregators/details?name={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.aggregator_name)

    @property
    def is_tagable(self) -> bool:
        return True

    @property
    def is_enabled_all_regions(self) -> bool:
        if self.account_aggregation_used:
            return self.account_aggregation_all_regions_enabled
        else:
            return self.organization_aggregation_all_regions_enabled
