from typing import Dict, List

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_list import CloudFrontDistribution, ViewerCertificate, CacheBehavior, OriginConfig
from cloudrail.knowledge.utils.arn_utils import build_arn


class CloudformationCloudfrontDistributionListBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.CLOUDFRONT_DISTRIBUTION_LIST, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> CloudFrontDistribution:
        properties: dict = cfn_res_attr['Properties']
        dist_config = properties['DistributionConfig']
        account = cfn_res_attr['account_id']
        name = self.create_random_pseudo_identifier()
        distribution_id = self.get_resource_id(cfn_res_attr)
        arn = build_arn('cloudfront', None, account, 'distribution', None, distribution_id)

        web_acl_id = self.get_property(dist_config, 'WebACLId')
        viewer_cert_dict = self.get_property(dist_config, 'ViewerCertificate')
        viewer_cert: ViewerCertificate = ViewerCertificate(cloudfront_default_certificate=self.get_property(viewer_cert_dict, 'CloudFrontDefaultCertificate', False),
                                                           minimum_protocol_version=self.get_property(viewer_cert_dict, 'MinimumProtocolVersion', 'TLSv1'))

        cache_behavior_list: List[CacheBehavior] = []
        order: int = 0
        default_cache_behavior_list = [self.get_property(dist_config, 'DefaultCacheBehavior')] if self.get_property(dist_config, 'DefaultCacheBehavior') else []
        for cache_behavior_dict in default_cache_behavior_list + self.get_property(dist_config, 'CacheBehaviors', []):
            cache_behavior: CacheBehavior = CacheBehavior(allowed_methods=self.get_property(cache_behavior_dict, 'AllowedMethods'),
                                                          cached_methods=self.get_property(cache_behavior_dict, 'CachedMethods'),
                                                          target_origin_id=self.get_property(cache_behavior_dict, 'TargetOriginId'),
                                                          viewer_protocol_policy=self.get_property(cache_behavior_dict, 'ViewerProtocolPolicy'),
                                                          trusted_signers=self.get_property(cache_behavior_dict, 'TrustedSigners', []),
                                                          precedence=order,
                                                          field_level_encryption_id=self.get_property(cache_behavior_dict, 'FieldLevelEncryptionId', ''))

            if 'PathPattern' in cache_behavior_dict:
                cache_behavior.path_pattern = self.get_property(cache_behavior_dict, 'PathPattern')
            cache_behavior_list.append(cache_behavior)
            order += 1

        origin_config_list: List[OriginConfig] = []
        for origin_dict in self.get_property(dist_config, 'Origins', []):
            s3_origin_config_data = self.get_property(origin_dict, 'S3OriginConfig', {})
            oai_path: str = self.get_property(s3_origin_config_data, 'OriginAccessIdentity')
            origin_config: OriginConfig = OriginConfig(domain_name=self.get_property(origin_dict, 'DomainName'),
                                                       origin_id=self.get_property(origin_dict, 'Id'),
                                                       oai_path=oai_path)
            origin_config_list.append(origin_config)

        return CloudFrontDistribution(account=account, name=name, arn=arn, distribution_id=distribution_id, viewer_cert=viewer_cert, web_acl_id=web_acl_id,
                                      cache_behavior_list=cache_behavior_list, origin_config_list=origin_config_list)
