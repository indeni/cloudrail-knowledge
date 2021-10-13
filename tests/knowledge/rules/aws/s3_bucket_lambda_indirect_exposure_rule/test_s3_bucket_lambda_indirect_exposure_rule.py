from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.s3_bucket_lambda_indirect_exposure_rule import S3BucketLambdaIndirectExposureRule


class TestS3BucketLambdaIndirectExposureRule(AwsBaseRuleTest):

    def get_rule(self):
        return S3BucketLambdaIndirectExposureRule()

    def test_private_api_gateway_with_wide_restrictions(self):
        self.run_test_case('private-api-gateway-with-wide-restrictions', False)

    def test_edge_api_gateway_with_wide_restrictions(self):
        self.run_test_case('edge-api-gateway-with-wide-restrictions', True)

    def test_policy_restriction_api_gateway(self):
        self.run_test_case('policy-restriction-api-gateway', False)

    def test_policy_permit_public_access_api_gateway(self):
        self.run_test_case('policy-permit-public-access-api-gateway', True)

    def test_lambda_function_block_api_gateway_access(self):
        self.run_test_case('lambda-function-block-api-gateway-access', False)

    def test_s3_bucket_block_lambda_function_access(self):
        self.run_test_case('s3-bucket-block-lambda-function-access', False)

    def test_lambda_function_no_s3_bucket_permissions(self):
        self.run_test_case('lambda-function-no-s3-bucket-permissions', False)

    def test_specific_s3_bucket_resource_permissions(self):
        self.run_test_case('specific-s3-bucket-resource-permissions', False)
