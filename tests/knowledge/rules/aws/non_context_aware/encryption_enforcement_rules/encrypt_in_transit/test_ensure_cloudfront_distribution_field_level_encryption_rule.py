import unittest
from typing import List

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.cloudfront.cloud_front_distribution_list import CloudFrontDistribution, CacheBehavior
from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_in_transit.ensure_cloudfront_distribution_field_level_encryption_rule import EnsureCloudfrontDistributionFieldLevelEncryptionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureCloudfrontDistributionFieldLevelEncryptionRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudfrontDistributionFieldLevelEncryptionRule()

    def test_non_car_cloudfront_distribution_field_level_encryption_creating_fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_dist_list.iac_state = IacState(address='address',
                                                  action=TerraformActionType.CREATE,
                                                  resource_metadata=None,
                                                  is_new=True)
        cache_behave_list: List[CacheBehavior] = [create_empty_entity(CacheBehavior), create_empty_entity(CacheBehavior)]
        cache_behave_list[0].path_pattern = '*'
        cache_behave_list[0].field_level_encryption_id = True
        cache_behave_list[1].path_pattern = 'path'
        cache_behave_list[1].precedence = 2
        cloudfront_dist_list._cache_behavior_list = cache_behave_list
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_distribution_field_level_encryption_creating__no_encrypt_fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_dist_list.iac_state = IacState(address='address',
                                                  action=TerraformActionType.CREATE,
                                                  resource_metadata=None,
                                                  is_new=True)
        cache_behave_list: List[CacheBehavior] = [create_empty_entity(CacheBehavior), create_empty_entity(CacheBehavior)]
        cache_behave_list[0].path_pattern = '*'
        cache_behave_list[0].field_level_encryption_id = False
        cache_behave_list[1].path_pattern = 'path'
        cache_behave_list[1].precedence = 2
        cache_behave_list[1].field_level_encryption_id = False
        cloudfront_dist_list._cache_behavior_list = cache_behave_list
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_distribution_field_level_encryption_creating__ordered_list_fail(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_dist_list.iac_state = IacState(address='address',
                                                  action=TerraformActionType.CREATE,
                                                  resource_metadata=None,
                                                  is_new=True)
        cache_behave_list: List[CacheBehavior] = [create_empty_entity(CacheBehavior), create_empty_entity(CacheBehavior)]
        cache_behave_list[0].path_pattern = '*'
        cache_behave_list[0].field_level_encryption_id = False
        cache_behave_list[1].path_pattern = 'path'
        cache_behave_list[1].precedence = 2
        cloudfront_dist_list._cache_behavior_list = cache_behave_list
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_cloudfront_distribution_field_level_encryption_creating__not_new__pass(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_dist_list.iac_state = IacState(address='address',
                                                  action=TerraformActionType.CREATE,
                                                  resource_metadata=None,
                                                  is_new=False)
        cache_behave_list: List[CacheBehavior] = [create_empty_entity(CacheBehavior), create_empty_entity(CacheBehavior)]
        cache_behave_list[0].path_pattern = '*'
        cache_behave_list[0].field_level_encryption_id = False
        cache_behave_list[1].path_pattern = 'path'
        cache_behave_list[1].precedence = 2
        cloudfront_dist_list._cache_behavior_list = cache_behave_list
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_cloudfront_distribution_field_level_encryption_creating_pass(self):
        # Arrange
        cloudfront_dist_list: CloudFrontDistribution = create_empty_entity(CloudFrontDistribution)
        cloudfront_dist_list.iac_state = IacState(address='address',
                                                  action=TerraformActionType.CREATE,
                                                  resource_metadata=None,
                                                  is_new=True)
        cache_behave_list: List[CacheBehavior] = [create_empty_entity(CacheBehavior), create_empty_entity(CacheBehavior)]
        cache_behave_list[0].path_pattern = '*'
        cache_behave_list[0].field_level_encryption_id = True
        cache_behave_list[1].path_pattern = 'path'
        cache_behave_list[1].precedence = 2
        cache_behave_list[1].field_level_encryption_id = True
        cloudfront_dist_list._cache_behavior_list = cache_behave_list
        context = AwsEnvironmentContext(cloudfront_distribution_list=[cloudfront_dist_list])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
