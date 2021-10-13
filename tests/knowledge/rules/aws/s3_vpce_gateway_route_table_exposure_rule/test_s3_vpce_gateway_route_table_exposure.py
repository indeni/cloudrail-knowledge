from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.vpc_endpoint_route_table_exposure_rule import S3VpcEndpointRouteTableExposureRule


class TestS3VpceGatewayRouteTableExposure(AwsBaseRuleTest):

    def get_rule(self):
        return S3VpcEndpointRouteTableExposureRule()

    def test_invalid_s3_vpce_association(self):  # bucket + eni + vpce + mismatch vpce
        self.run_test_case('invalid-s3-vpce-association', True)

    def test_no_bucket_in_region(self):  # igw + eni
        self.run_test_case('no-buckets-in-region', False)

    def test_vpc_do_not_contains_any_eni(self):  # bucket + vpce + vpce route
        self.run_test_case('vpc-do-not-contains-any-eni', False)

    def test_vpce_exist_with_route_table_association(self):  # bucket + eni + vpce
        self.run_test_case('vpce-exist-with-route-table-association', False)

    def test_vpc_has_s3_vpce_gw_valid_route(self):  # bucket + eni + vpce + vpce route
        self.run_test_case('vpc-has-s3-vpce-gw-valid-route', False)

    def test_s3_vpce_gw_not_exist_with_route(self):  # bucket + eni + vpce route
        self.run_test_case('s3-vpce-gw-not-exist-with-route', False)
