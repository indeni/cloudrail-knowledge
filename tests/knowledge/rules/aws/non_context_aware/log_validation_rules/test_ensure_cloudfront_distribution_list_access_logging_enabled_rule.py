import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.cloudfront.cloud_front_distribution_list import CloudFrontDistribution
from cloudrail.knowledge.context.aws.resources.cloudfront.cloudfront_distribution_logging import CloudfrontDistributionLogging
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_cloudfront_distribution_list_access_logging_enabled_rule import \
    EnsureCloudfrontDistributionListAccessLoggingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureCloudfrontDistributionListAccessLoggingEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudfrontDistributionListAccessLoggingEnabledRule()

    def test_non_car_cloudfront_distribution_access_logging_enabled__logging_disabled__fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_logging: CloudfrontDistributionLogging = create_empty_entity(CloudfrontDistributionLogging)
        cloudfront_logging.logging_enabled = False
        cloudfront_dist_list.logs_settings = cloudfront_logging
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list], cloudfront_log_settings=[cloudfront_logging])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_distribution_access_logging_enabled__no_logging__fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_distribution_access_logging_enabled_pass(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_logging: CloudfrontDistributionLogging = create_empty_entity(CloudfrontDistributionLogging)
        cloudfront_logging.logging_enabled = True
        cloudfront_dist_list.logs_settings = cloudfront_logging
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list], cloudfront_log_settings=[cloudfront_logging])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
