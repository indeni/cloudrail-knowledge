from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.s3_bucket_lambda_indirect_exposure_rule import S3BucketLambdaIndirectExposureRule


class TestS3BucketLambdaIndirectExposureRule(AwsBaseRuleTest):

    def get_rule(self):
        return S3BucketLambdaIndirectExposureRule()

    @rule_test('private-api-gateway-with-wide-restrictions', False)
    def test_private_api_gateway_with_wide_restrictions(self, rule_result: RuleResponse):
        pass

    @rule_test('edge-api-gateway-with-wide-restrictions', True)
    def test_edge_api_gateway_with_wide_restrictions(self, rule_result: RuleResponse):
        pass

    @rule_test('policy-restriction-api-gateway', False)
    def test_policy_restriction_api_gateway(self, rule_result: RuleResponse):
        pass

    @rule_test('policy-permit-public-access-api-gateway', True)
    def test_policy_permit_public_access_api_gateway(self, rule_result: RuleResponse):
        pass

    @rule_test('lambda-function-block-api-gateway-access', False)
    def test_lambda_function_block_api_gateway_access(self, rule_result: RuleResponse):
        pass

    @rule_test('s3-bucket-block-lambda-function-access', False)
    def test_s3_bucket_block_lambda_function_access(self, rule_result: RuleResponse):
        pass

    @rule_test('lambda-function-no-s3-bucket-permissions', False)
    def test_lambda_function_no_s3_bucket_permissions(self, rule_result: RuleResponse):
        pass

    @rule_test('specific-s3-bucket-resource-permissions', False)
    def test_specific_s3_bucket_resource_permissions(self, rule_result: RuleResponse):
        pass
