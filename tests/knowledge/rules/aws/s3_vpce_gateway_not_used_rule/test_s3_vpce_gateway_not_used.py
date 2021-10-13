from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.vpc_endpoint_gateway_not_used_rule import S3VpcEndpointGatewayNotUsedRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestS3VpceGatewayNotUsed(AwsBaseRuleTest):

    def get_rule(self):
        return S3VpcEndpointGatewayNotUsedRule()

    def test_vpc_instance_has_direct_s3_service_connection(self):  # igw + bucket + eni
        self.run_test_case('vpc_instance_has_direct_s3_service_connection', True)

    def test_no_bucket_in_region(self):  # igw + eni
        self.run_test_case('no-buckets-in-region', False)

    def test_vpc_do_not_contains_any_eni(self):  # igw + bucket
        self.run_test_case('vpc-do-not-contains-any-eni', False)

    def test_vpc_has_s3_vpce_gw_and_public_connection(self):  # igw + bucket + eni + vpce
        self.run_test_case('vpc_has_s3_vpce_gw_and_public_connection', False)

    def test_vpc_has_only_s3_vpce_gw_connection(self):  # igw + bucket + eni + vpce + natgw (private)
        self.run_test_case('vpc_has_only_s3_vpce_gw_connection', False)
