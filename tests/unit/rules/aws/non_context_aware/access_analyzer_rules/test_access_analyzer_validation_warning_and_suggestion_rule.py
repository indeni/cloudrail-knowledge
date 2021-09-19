import unittest

from cloudrail.knowledge.context.aws.resources.iam.policy import ManagedPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.access_analyzer_rules.access_analyzer_validation_warning_and_suggestion_rule import \
    AccessAnalyzerValidationWarningAndSuggestionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestAccessAnalyzerValidationWarningAndSuggestionRule(unittest.TestCase):
    def setUp(self):
        self.rule = AccessAnalyzerValidationWarningAndSuggestionRule()

    def test_not_car_access_analyzer_validation_warning_and_suggestion__warning_finding__fail(self):
        # Arrange
        policy: ManagedPolicy = ManagedPolicy('111111111', 'ANPAILL3HVNFSB6DCOWYQ', 'ReadOnlyAccess', 'arn:aws:iam::aws:policy/ReadOnlyAccess',
                                              [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                               ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))],
                                              'state_id')
        policy.iac_state = IacState(address='address', action=IacActionType.CREATE, resource_metadata=None, is_new=True)
        policy.access_analyzer_findings = [{
            "findingDetails": "Add a value to the empty string in the Sid element.",
            "findingType": "WARNING",
            "issueCode": "EMPTY_SID_VALUE",
            "learnMoreLink": "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html",
            "locations": [
                {
                    "path": [
                        {
                            "value": "Statement"
                        },
                        {
                            "index": 0
                        },
                        {
                            "value": "Sid"
                        }
                    ],
                    "span": {
                        "end": {
                            "column": 19,
                            "line": 10,
                            "offset": 235
                        },
                        "start": {
                            "column": 17,
                            "line": 10,
                            "offset": 233
                        }
                    }
                }
            ]
        }]

        context = AwsEnvironmentContext(policies=[policy])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_access_analyzer_validation_warning_and_suggestion__suggestion_finding__fail(self):
        # Arrange
        policy: ManagedPolicy = ManagedPolicy('111111111', 'ANPAILL3HVNFSB6DCOWYQ', 'ReadOnlyAccess', 'arn:aws:iam::aws:policy/ReadOnlyAccess',
                                              [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                               ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))],
                                              'state_id')
        policy.iac_state = IacState(address='address', action=IacActionType.CREATE, resource_metadata=None, is_new=True)
        policy.access_analyzer_findings = [{
            "findingDetails": "Add a value to the empty string in the Sid element.",
            "findingType": "SUGGESTION",
            "issueCode": "EMPTY_SID_VALUE",
            "learnMoreLink": "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html",
            "locations": [
                {
                    "path": [
                        {
                            "value": "Statement"
                        },
                        {
                            "index": 0
                        },
                        {
                            "value": "Sid"
                        }
                    ],
                    "span": {
                        "end": {
                            "column": 19,
                            "line": 10,
                            "offset": 235
                        },
                        "start": {
                            "column": 17,
                            "line": 10,
                            "offset": 233
                        }
                    }
                }
            ]
        }]

        context = AwsEnvironmentContext(policies=[policy])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_access_analyzer_validation_warning_and_suggestion_pass(self):
        # Arrange
        policy: ManagedPolicy = ManagedPolicy('111111111', 'ANPAILL3HVNFSB6DCOWYQ', 'ReadOnlyAccess', 'arn:aws:iam::aws:policy/ReadOnlyAccess',
                                              [PolicyStatement(StatementEffect.ALLOW, ['*'],
                                                               ['*'], Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))],
                                              'state_id')
        policy.iac_state = IacState(address='address', action=IacActionType.CREATE, resource_metadata=None, is_new=True)
        policy.access_analyzer_findings = [{
            "findingDetails": "Add a value to the empty string in the Sid element.",
            "findingType": "ERROR",
            "issueCode": "EMPTY_SID_VALUE",
            "learnMoreLink": "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html",
            "locations": [
                {
                    "path": [
                        {
                            "value": "Statement"
                        },
                        {
                            "index": 0
                        },
                        {
                            "value": "Sid"
                        }
                    ],
                    "span": {
                        "end": {
                            "column": 19,
                            "line": 10,
                            "offset": 235
                        },
                        "start": {
                            "column": 17,
                            "line": 10,
                            "offset": 233
                        }
                    }
                }
            ]
        }]

        context = AwsEnvironmentContext(policies=[policy])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
