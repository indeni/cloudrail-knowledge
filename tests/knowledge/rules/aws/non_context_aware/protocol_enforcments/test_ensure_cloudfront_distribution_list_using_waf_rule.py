import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.cloudfront.cloud_front_distribution_list import CloudFrontDistribution
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_cloudfront_distribution_list_using_waf_rule import \
    CloudFrontEnsureWafUsedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestCloudFrontEnsureWafUsedRule(unittest.TestCase):
    def setUp(self):
        self.rule = CloudFrontEnsureWafUsedRule()

    def test_non_car_cloudfront_distribution_using_waf__empty_string__fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_dist_list.web_acl_id = ''
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_distribution_using_waf__tf_address__fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_dist_list.web_acl_id = 'aws_cloudfront_distribution.test.web_acl_id'
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_distribution_using_waf__tf_link__pass(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_dist_list.web_acl_id = 'aws_wafv2_web_acl.test.arn'
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_cloudfront_distribution_using_waf__aws_using_arn__pass(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_dist_list.web_acl_id = 'arn:waf:region:account'
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
