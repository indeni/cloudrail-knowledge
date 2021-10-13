import unittest
from unittest import skip

from core.rules.checkov.base_checkov_rule import BaseCheckovRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest

@unittest.skip('should not test checkov rules like this')
class TestCkvAws37(AwsBaseRuleTest):

    def get_rule(self):
        return BaseCheckovRule('CKV_AWS_37')

    @skip('flaky due to parallel')
    def test_failure(self):
        self.run_test_case('failure', True, 1)

    def test_pass(self):
        self.run_test_case('pass', False)
