from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.vpc_endpoint_route_table_exposure_rule import DynamoDbVpcEndpointRouteTableExposureRule


class TestDynamodbVpceGatewayRouteTableExposure(AwsBaseRuleTest):

    def get_rule(self):
        return DynamoDbVpcEndpointRouteTableExposureRule()

    def test_invalid_dynamodb_vpce_association(self):  # table + eni + vpce + mismatch vpce
        self.run_test_case('invalid-dynamodb-vpce-association', True)

    def test_no_tables_in_region(self):  # eni + vpce + vpce route
        self.run_test_case('no-tables-in-region', False)

    def test_vpc_do_not_contains_any_eni(self):  # table + vpce + vpce route
        self.run_test_case('vpc-do-not-contains-any-eni', False)

    def test_dynamodb_vpce_exist_with_route_table_association(self):  # table + eni + vpce
        self.run_test_case('dynamodb-vpce-exist-with-route-table-association', False)

    def test_vpc_has_dynamodb_vpce_gw_valid_route(self):  # table + eni + vpce + vpce route
        self.run_test_case('vpc-has-dynamodb-vpce-gw-valid-route', False)

    def test_dynamodb_vpce_gw_not_exist_with_route(self):  # table + eni + vpce route
        self.run_test_case('dynamodb-vpce-gw-not-exist-with-route', False)
