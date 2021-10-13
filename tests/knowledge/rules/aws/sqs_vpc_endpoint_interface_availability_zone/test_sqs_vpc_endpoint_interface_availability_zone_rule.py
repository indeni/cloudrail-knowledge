from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_interface_availability_zone_rule import \
    SqsVpcEndpointInterfaceAvailabilityZoneRule


class TestSqsVpcEndpointInterfaceAvailabilityZoneRule(AwsBaseRuleTest):

    def get_rule(self):
        return SqsVpcEndpointInterfaceAvailabilityZoneRule()

    def test_sqs_vpc_endpoint_exist_in_multi_az(self):
        self.run_test_case('sqs-vpc-endpoint-exist-in-multi-az', False)

    def test_sqs_vpc_endpoint_exist_in_single_az(self):
        self.run_test_case('sqs-vpc-endpoint-exist-in-single-az', True)

    def test_sqs_multi_vpc_endpoints_from_same_az(self):
        self.run_test_case('sqs-multi-vpc-endpoints-from-same-az', True)

    def test_sqs_multi_vpc_endpoints_from_different_az(self):
        self.run_test_case('sqs-multi-vpc-endpoints-from-different-az', False)
