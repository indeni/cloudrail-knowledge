from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.vpc_endpoint_gateway_not_used_rule import DynamoDbVpcEndpointGatewayNotUsedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestDynamoDbVpceGatewayNotUsed(AwsBaseRuleTest):

    def get_rule(self):
        return DynamoDbVpcEndpointGatewayNotUsedRule()

    @rule_test('vpc_instance_has_direct_dynamodb_service_connection', True)
    def test_vpc_instance_has_direct_dynamodb_service_connection(self, rule_result: RuleResponse):
        pass

    @rule_test('vpc-do-not-contains-any-eni', False)
    def test_vpc_do_not_contains_any_eni(self, rule_result: RuleResponse):
        pass

    @rule_test('vpc-do-not-have-dynamodb-tables-in-region', False)
    def test_vpc_do_not_have_dynamodb_tables_in_region(self, rule_result: RuleResponse):
        pass

    @rule_test('vpc_has_dynamodb_vpce_gw_and_public_connection', False)
    def test_vpc_has_dynamodb_vpce_gw_and_public_connection(self, rule_result: RuleResponse):
        pass

    @rule_test('vpc_has_only_dynamodb_vpce_gw_connection', False)
    def test_vpc_has_only_dynamodb_vpce_gw_connection(self, rule_result: RuleResponse):
        pass
