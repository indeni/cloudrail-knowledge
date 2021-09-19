import unittest
from typing import List

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.cloudfront.cloud_front_distribution_list import CacheBehavior, CloudFrontDistribution
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_in_transit.ensure_cloudfront_distribution_encrypt_in_transit_rule import EnsureCloudfrontDistributionEncryptInTransitRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureCloudfrontDistributionEncryptInTransitRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudfrontDistributionEncryptInTransitRule()

    def test_non_car_cloudfront_distribution_encrypt_in_transit_fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cache_behave_list: List[CacheBehavior] = [create_empty_entity(CacheBehavior)]
        cache_behave_list[0].path_pattern = '*'
        cache_behave_list[0].viewer_protocol_policy = 'dist_protocol_policy'
        cloudfront_dist_list._cache_behavior_list = cache_behave_list
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_distribution_encrypt_in_transit__not_ordered_cached_restrict__fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cache_behave_list: List[CacheBehavior] = [create_empty_entity(CacheBehavior), create_empty_entity(CacheBehavior)]
        cache_behave_list[0].path_pattern = '*'
        cache_behave_list[0].viewer_protocol_policy = 'https-only'
        cache_behave_list[1].path_pattern = 'path'
        cache_behave_list[1].viewer_protocol_policy = 'dist_protocol_policy'
        cloudfront_dist_list._cache_behavior_list = cache_behave_list
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_distribution_encrypt_in_transit__both_not__fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cache_behave_list: List[CacheBehavior] = [create_empty_entity(CacheBehavior), create_empty_entity(CacheBehavior)]
        cache_behave_list[0].path_pattern = '*'
        cache_behave_list[0].viewer_protocol_policy = 'dist_protocol_policy'
        cache_behave_list[1].path_pattern = 'path'
        cache_behave_list[1].viewer_protocol_policy = 'dist_protocol_policy'
        cloudfront_dist_list._cache_behavior_list = cache_behave_list
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_distribution_encrypt_in_transit_pass(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cache_behave_list: List[CacheBehavior] = [create_empty_entity(CacheBehavior), create_empty_entity(CacheBehavior)]
        cache_behave_list[0].path_pattern = '*'
        cache_behave_list[0].viewer_protocol_policy = 'https-only'
        cache_behave_list[1].path_pattern = 'path'
        cache_behave_list[1].viewer_protocol_policy = 'https-only'
        cloudfront_dist_list._cache_behavior_list = cache_behave_list
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
