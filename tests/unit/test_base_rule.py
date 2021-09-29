import unittest
import uuid
from typing import Dict, List

from mockito import mock, when

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.igw_type import IgwType
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue, RuleResultType
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class MockRule(BaseRule):

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return self.should_run

    account = '111111111111'
    region = 'us-east-1'

    def __init__(self):
        self.exposed1: Mergeable = InternetGateway(MockRule.account, MockRule.region, str(uuid.uuid4()), str(uuid.uuid4()), IgwType.IGW)
        self.violating1: Mergeable = InternetGateway(MockRule.account, MockRule.region, str(uuid.uuid4()), str(uuid.uuid4()), IgwType.IGW)
        self.exposed2: Mergeable = InternetGateway(MockRule.account, MockRule.region, str(uuid.uuid4()), str(uuid.uuid4()), IgwType.IGW)
        self.violating2: Mergeable = InternetGateway(MockRule.account, MockRule.region, str(uuid.uuid4()), str(uuid.uuid4()), IgwType.IGW)
        self.exposed1.iac_state = IacState('', '', None, True)
        self.exposed2.iac_state = IacState('', '', None, True)
        self.violating1.iac_state = IacState('', '', None, True)
        self.violating2.iac_state = IacState('', '', None, True)
        self.should_run = True

    def get_id(self) -> str:
        return 'mock_rule'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        return [Issue('issue', self.exposed1, self.violating1), Issue('issue', self.exposed2, self.violating2)]

    def get_needed_parameters(self) -> List[ParameterType]:
        return []


class TestBaseRule(unittest.TestCase):

    def setUp(self):
        self.mock_rule = MockRule()
        self.mock_context = mock()
        when(self.mock_context).get_all_mergeable_resources().thenReturn([self.mock_rule.exposed1,
                                                                          self.mock_rule.exposed2,
                                                                          self.mock_rule.violating1,
                                                                          self.mock_rule.violating2])

    def test_run_result_have_unknown_resources(self):
        # Arrange
        unknown_resource = InternetGateway(MockRule.account, MockRule.region, str(uuid.uuid4()), str(uuid.uuid4()), IgwType.IGW)
        self.mock_rule.exposed1 = unknown_resource

        # Act
        response = self.mock_rule.run(self.mock_context, {})

        # Assert
        self.assertEqual(RuleResultType.FAILED, response.status)
        self.assertEqual(1, len(response.issues))
