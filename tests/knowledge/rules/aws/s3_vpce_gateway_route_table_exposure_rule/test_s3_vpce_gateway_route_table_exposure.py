from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.vpc_endpoint_route_table_exposure_rule import S3VpcEndpointRouteTableExposureRule


class TestS3VpceGatewayRouteTableExposure(AwsBaseRuleTest):

    def get_rule(self):
        return S3VpcEndpointRouteTableExposureRule()

    @rule_test('invalid-s3-vpce-association', True)
    def test_invalid_s3_vpce_association(self, rule_result: RuleResponse):  # bucket + eni + vpce + mismatch vpce
        pass

    @rule_test('no-buckets-in-region', False)
    def test_no_bucket_in_region(self, rule_result: RuleResponse):  # igw + eni
        pass

    @rule_test('vpc-do-not-contains-any-eni', False)
    def test_vpc_do_not_contains_any_eni(self, rule_result: RuleResponse):  # bucket + vpce + vpce route
        pass

    @rule_test('vpce-exist-with-route-table-association', False)
    def test_vpce_exist_with_route_table_association(self, rule_result: RuleResponse):  # bucket + eni + vpce
        pass

    @rule_test('vpc-has-s3-vpce-gw-valid-route', False)
    def test_vpc_has_s3_vpce_gw_valid_route(self, rule_result: RuleResponse):  # bucket + eni + vpce + vpce route
        pass

    @rule_test('s3-vpce-gw-not-exist-with-route', False)
    def test_s3_vpce_gw_not_exist_with_route(self, rule_result: RuleResponse):  # bucket + eni + vpce route
        pass
