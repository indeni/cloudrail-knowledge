from abc import ABC, abstractmethod
from typing import List, Dict, Set

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AccessAnalyzerValidationBaseRule(AwsBaseRule, ABC):

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.get_iac_managed_policies())

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues = []

        for policy in env_context.get_iac_managed_policies():
            evidence = self._create_evidence_from_findings(policy.access_analyzer_findings)
            if evidence:
                issues.append(Issue(evidence, policy, policy))

        return issues

    def _create_evidence_from_findings(self, findings):
        evidences = []
        for finding in findings:
            evidence = ''
            if finding.get('findingType') in self._get_violated_finding_types():
                if finding.get('locations'):
                    start = finding['locations'][0]['span']['start']
                    line = start['line']
                    column = start['column']
                    prefix = f'Line {line}, Col {column}:'
                else:
                    prefix = 'Finding Without Specific Location In Policy:'
                finding_details = finding['findingDetails']
                learn_more = finding['learnMoreLink']
                evidence += f'~{prefix}~. {finding_details} See {learn_more}'
                evidences.append(evidence)
        return '. '.join(evidences)

    @abstractmethod
    def _get_violated_finding_types(self) -> Set[str]:
        pass
