from dataclasses import dataclass, field
from typing import List, Optional, Dict

import dataclasses
from cloudrail.knowledge.context.connection import ConnectionInstance
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_logging import CloudfrontDistributionLogging
from cloudrail.knowledge.context.aws.resources.cloudfront.origin_access_identity import OriginAccessIdentity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName, AwsServiceType, AwsServiceAttributes
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.utils.tags_utils import filter_tags


class OriginConfig:
    """
        Attributes:
            domain_name: The domain name for the origin.
            origin_id: The ID of the origin.
            oai_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin.
            origin_access_identity_list: List of OriginAccessIdentity configurations.
    """
    def __init__(self, domain_name: str, origin_id: str, oai_path: str, origin_access_identity_list: Optional[List[OriginAccessIdentity]] = None):
        self.domain_name = domain_name
        self.origin_id = origin_id
        self.oai_path = oai_path
        self.origin_access_identity_list = origin_access_identity_list or []

    def to_drift_detection_object(self):
        return {'domain_name': self.domain_name}


@dataclass
class ViewerCertificate:
    """
        Attributes:
            cloudfront_default_certificate: Is this the default certificate.
            minimum_protocol_version: One of SSLv3 | TLSv1 | TLSv1_2016 | TLSv1.1_2016 | TLSv1.2_2018 | TLSv1.2_2019.
    """
    cloudfront_default_certificate: bool
    minimum_protocol_version: str


@dataclass
class CacheBehavior:
    """
        Attributes:
            allowed_methods: The list of HTTP methods allowed.
            cached_methods: The list of HTTP methods whose responses are cached.
            target_origin_id: The origin this cache is targeting.
            viewer_protocol_policy: One of allow-all, redirect-to-https, https-only.
            precedence: The order of the cache behavior.
            path_partern: The URL pattern to match.
            trusted_signers: A list of AWS account IDs whose public keys CloudFront can use to validate signed URLs or signed cookies.
            field_level_encryption_id: The value of ID for the field-level encryption
                configuration to use, may be None.
    """
    allowed_methods: List[str]
    cached_methods: List[str]
    target_origin_id: str
    viewer_protocol_policy: str
    precedence: int
    path_pattern: str = field(default="*")
    trusted_signers: List[str] = field(default=list)
    field_level_encryption_id: str = field(default=None)


class CloudFrontDistribution(AwsResource, ConnectionInstance):
    """
        Attributes:
            arn: The ARN of the CloudFront Distribution.
            name: The name of the distribution.
            distribution_id: The ID of the distribution.
            viewer_cert: An object of type ViewerCertificate representing the viewer certificate
                 used with this distribution.
            origin_config_list: A list of OriginConfig, the order is not guaranteed.
            web_acl_id: The ID of the AWS WAF web ACL, to associate with this distribution.
            logs_settings: The logs settings of the CloudFront Distribution, if configured.
    """

    def __init__(self,
                 arn: str,
                 name: str,
                 distribution_id: str,
                 account: str,
                 viewer_cert: ViewerCertificate,
                 cache_behavior_list: List[CacheBehavior],
                 origin_config_list: List[OriginConfig],
                 web_acl_id: str,
                 tags: Dict[str, str] = None):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_CLOUDFRONT_DISTRIBUTION_LIST,
                         aws_service_attributes=AwsServiceAttributes(AwsServiceType.CLOUDFRONT.value))
        ConnectionInstance.__init__(self)
        self.arn: str = arn
        self.name: str = name
        self.distribution_id: str = distribution_id
        self.viewer_cert: ViewerCertificate = viewer_cert
        self._cache_behavior_list: List[CacheBehavior] = cache_behavior_list
        self.origin_config_list: List[OriginConfig] = origin_config_list
        self.web_acl_id: str = web_acl_id
        if tags:
            self.tags = tags
        self.logs_settings: Optional[CloudfrontDistributionLogging] = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.distribution_id

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudFront Distribution'
        else:
            return 'CloudFront Distributions'

    def get_cloud_resource_url(self) -> str:
        return '{0}cloudfront/home?region={1}#distribution-settings:{2}' \
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.distribution_id)

    @property
    def is_tagable(self) -> bool:
        return True

    @property
    def is_waf_enabled(self) -> bool:
        return bool(self.web_acl_id and 'aws_cloudfront_distribution' not in self.web_acl_id)

    def get_default_behavior(self) -> Optional[CacheBehavior]:
        """
            Returns:
                the default cache behavior.
        """
        for cache in self._cache_behavior_list:
            if cache.path_pattern == "*":
                return cache
        return None

    def get_ordered_behavior_list(self) -> List[CacheBehavior]:
        """
            Returns:
                A list of CacheBehavior, if caching is configured. The order
                    of the list is - first the default cache behavior, and then the specific
                    cache behaviors by their defined order.

        """
        return [cache for cache in self._cache_behavior_list if cache.path_pattern != "*"]

    def get_all_cache_behaviors(self):
        return list(self._cache_behavior_list)

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'name': self.name,
                'viewer_cert': dataclasses.asdict(self.viewer_cert),
                'cache_behavior_list': [dataclasses.asdict(cache_behavior) for cache_behavior in self.get_all_cache_behaviors()],
                'origin_config_list': [original_config.to_drift_detection_object() for original_config in self.origin_config_list],
                'web_acl_id': self.web_acl_id}
