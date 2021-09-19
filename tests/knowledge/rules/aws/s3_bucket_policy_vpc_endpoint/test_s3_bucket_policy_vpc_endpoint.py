from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.s3_bucket_policy_vpc_endpoint_rule import S3BucketPolicyVpcEndpointRule


class TestS3BucketPolicyVpcEndpoint(AwsBaseRuleTest):

    def get_rule(self):
        return S3BucketPolicyVpcEndpointRule()

    def test_no_buckets_in_region(self):  # vpce
        self.run_test_case('no-buckets-in-region', False)

    def test_vpc_without_s3_endpoint(self):  # private-bucket + none-restrict-bucket-policy
        self.run_test_case('vpc-without-endpoint', False)

    def test_policy_with_vpce_restriction(self):  # private-bucket + restrict-bucket-policy + vpce
        self.run_test_case('private-bucket-policy-with-vpce-restriction', False)

    def test_public_bucket_with_policy_vpce_restriction(self):  # public-bucket + none-restrict-bucket-policy + vpce
        self.run_test_case('public-bucket-with-policy-vpce-restriction', False)

    def test_private_bucket_policy_without_vpce_restriction(self):  # private-bucket + none-restrict-bucket-policy + vpce
        self.run_test_case('private-bucket-policy-without-vpce-restriction', True)
