from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_interface_not_used_rule import SqsVpcEndpointExposureRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestVpcEndpointSqsExposureRule(AwsBaseRuleTest):

    def get_rule(self):
        return SqsVpcEndpointExposureRule()

    def test_sqs_vpc_endpoint_on_private_subnet(self):
        self.run_test_case('sqs-vpc-endpoint-on-private-subnet', False)

    def test_sqs_vpc_endpoint_exist_with_igw(self):
        self.run_test_case('sqs-vpc-endpoint-exist-with-igw', False)

    def test_sqs_vpc_endpoint_do_not_exist_with_igw(self):
        self.run_test_case('sqs-vpc-endpoint-do-not-exist-with-igw', True)

    def test_sqs_vpc_endpoint_do_not_exist(self):
        self.run_test_case('sqs-service-do-not-exist', False)

    def test_sqs_vpc_endpoint_without_dns_resolution(self):
        self.run_test_case('sqs-vpc-endpoint-without-dns-resolution', True)
