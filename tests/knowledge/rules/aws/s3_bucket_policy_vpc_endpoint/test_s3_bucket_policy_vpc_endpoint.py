from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.s3_bucket_policy_vpc_endpoint_rule import S3BucketPolicyVpcEndpointRule


class TestS3BucketPolicyVpcEndpoint(AwsBaseRuleTest):

    def get_rule(self):
        return S3BucketPolicyVpcEndpointRule()

    @rule_test('no-buckets-in-region', False)
    def test_no_buckets_in_region(self, rule_result: RuleResponse):  # vpce
        pass

    @rule_test('vpc-without-endpoint', False)
    def test_vpc_without_s3_endpoint(self, rule_result: RuleResponse):  # private-bucket + none-restrict-bucket-policy
        pass

    @rule_test('private-bucket-policy-with-vpce-restriction', False)
    def test_policy_with_vpce_restriction(self, rule_result: RuleResponse):  # private-bucket + restrict-bucket-policy + vpce
        pass

    @rule_test('public-bucket-with-policy-vpce-restriction', False)
    def test_public_bucket_with_policy_vpce_restriction(self, rule_result: RuleResponse):  # public-bucket + none-restrict-bucket-policy + vpce
        pass

    @rule_test('private-bucket-policy-without-vpce-restriction', True)
    def test_private_bucket_policy_without_vpce_restriction(self, rule_result: RuleResponse):  # private-bucket + none-restrict-bucket-policy + vpce
        pass
