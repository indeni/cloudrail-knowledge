from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.vpc_endpoint_route_table_exposure_rule import DynamoDbVpcEndpointRouteTableExposureRule


class TestDynamodbVpceGatewayRouteTableExposure(AwsBaseRuleTest):

    def get_rule(self):
        return DynamoDbVpcEndpointRouteTableExposureRule()

    @rule_test('invalid-dynamodb-vpce-association', True)
    def test_invalid_dynamodb_vpce_association(self, rule_result: RuleResponse):  # table + eni + vpce + mismatch vpce
        pass

    @rule_test('no-tables-in-region', False)
    def test_no_tables_in_region(self, rule_result: RuleResponse):  # eni + vpce + vpce route
        pass

    @rule_test('vpc-do-not-contains-any-eni', False)
    def test_vpc_do_not_contains_any_eni(self, rule_result: RuleResponse):  # table + vpce + vpce route
        pass

    @rule_test('dynamodb-vpce-exist-with-route-table-association', False)
    def test_dynamodb_vpce_exist_with_route_table_association(self, rule_result: RuleResponse):  # table + eni + vpce
        pass

    @rule_test('vpc-has-dynamodb-vpce-gw-valid-route', False)
    def test_vpc_has_dynamodb_vpce_gw_valid_route(self, rule_result: RuleResponse):  # table + eni + vpce + vpce route
        pass

    @rule_test('dynamodb-vpce-gw-not-exist-with-route', False)
    def test_dynamodb_vpce_gw_not_exist_with_route(self, rule_result: RuleResponse):  # table + eni + vpce route
        pass
