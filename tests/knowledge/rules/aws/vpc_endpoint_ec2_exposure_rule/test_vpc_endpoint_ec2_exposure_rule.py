from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_interface_not_used_rule import Ec2VpcEndpointExposureRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestVpcEndpointEc2ExposureRule(AwsBaseRuleTest):

    def get_rule(self):
        return Ec2VpcEndpointExposureRule()

    def test_private_subnet_without_ec2_vpc_endpoint(self):
        self.run_test_case('private-subnet-without-ec2-vpc-endpoint', False)

    def test_ec2_vpc_endpoint_exist_with_igw(self):
        self.run_test_case('ec2-vpc-endpoint-exist-with-igw', False)

    def test_ec2_vpc_endpoint_do_not_exist_with_igw(self):
        self.run_test_case('ec2-vpc-endpoint-do-not-exist-with-igw', True)

    def test_ec2_vpc_endpoint_do_not_exist(self):
        self.run_test_case('ec2-service-do-not-exist', False)

    def test_ec2_vpc_endpoint_without_dns_resolution(self):
        self.run_test_case('ec2-vpc-endpoint-without-dns-resolution', True)
