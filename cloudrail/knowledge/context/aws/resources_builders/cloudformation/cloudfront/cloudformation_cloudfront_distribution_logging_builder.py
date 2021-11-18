from typing import Dict

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_logging import CloudfrontDistributionLogging
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationCloudfrontDistributionLoggingBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CLOUDFRONT_DISTRIBUTION_LIST, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> CloudfrontDistributionLogging:
        properties: dict = cfn_res_attr['Properties']
        dist_config = properties['DistributionConfig']
        logging_enabled = bool('Logging' in dist_config)
        account = cfn_res_attr['account_id']
        name = self.create_random_pseudo_identifier()
        distribution_id = self.get_resource_id(cfn_res_attr)
        arn = build_arn('cloudfront', None, account, 'distribution', None, distribution_id)
        logging_properties = self.get_property(dist_config, 'Logging', {})
        include_cookies = bool(logging_properties.get('IncludeCookies'))
        s3_bucket = logging_properties.get('Bucket')
        prefix = self.get_property(logging_properties, 'Prefix')
        return CloudfrontDistributionLogging(account=account, name=name, arn=arn, distribution_id=distribution_id,
                                             include_cookies=include_cookies, s3_bucket=s3_bucket, prefix=prefix,
                                             logging_enabled=logging_enabled)
