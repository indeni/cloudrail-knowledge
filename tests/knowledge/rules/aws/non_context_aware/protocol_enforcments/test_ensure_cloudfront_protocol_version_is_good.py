import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.cloudfront.cloud_front_distribution_list import CloudFrontDistribution, ViewerCertificate
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_cloudfront_protocol_version_is_good import \
    CloudFrontEnsureVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestCloudFrontEnsureVersionRule(unittest.TestCase):
    def setUp(self):
        self.rule = CloudFrontEnsureVersionRule()

    def test_non_car_cloudfront_protocol_version_fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        viewer_cert: ViewerCertificate = create_empty_entity(ViewerCertificate)
        viewer_cert.minimum_protocol_version = 'TLSv1.2_2018'
        cloudfront_dist_list.viewer_cert = viewer_cert
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_protocol_version_pass(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        viewer_cert: ViewerCertificate = create_empty_entity(ViewerCertificate)
        viewer_cert.minimum_protocol_version = 'TLSv1.2_2019'
        cloudfront_dist_list.viewer_cert = viewer_cert
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
