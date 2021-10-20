from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.vpc_endpoint_gateway_not_used_rule import S3VpcEndpointGatewayNotUsedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestS3VpceGatewayNotUsed(AwsBaseRuleTest):

    def get_rule(self):
        return S3VpcEndpointGatewayNotUsedRule()

    @rule_test('vpc_instance_has_direct_s3_service_connection', True)
    def test_vpc_instance_has_direct_s3_service_connection(self, rule_result: RuleResponse):  # igw + bucket + eni
        pass

    @rule_test('no-buckets-in-region', False)
    def test_no_bucket_in_region(self, rule_result: RuleResponse):  # igw + eni
        pass

    @rule_test('vpc-do-not-contains-any-eni', False)
    def test_vpc_do_not_contains_any_eni(self, rule_result: RuleResponse):  # igw + bucket
        pass

    @rule_test('vpc_has_s3_vpce_gw_and_public_connection', False)
    def test_vpc_has_s3_vpce_gw_and_public_connection(self, rule_result: RuleResponse):  # igw + bucket + eni + vpce
        pass

    @rule_test('vpc_has_only_s3_vpce_gw_connection', False)
    def test_vpc_has_only_s3_vpce_gw_connection(self, rule_result: RuleResponse):  # igw + bucket + eni + vpce + natgw (private)
        pass
