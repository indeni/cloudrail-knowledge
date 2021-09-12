import logging
from typing import List, Dict

from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.rules.base_rule import RuleResponse, BaseRule, RuleResultType

from cloudrail.knowledge.rules.rules_loader import RulesLoader


class RulesExecutor:

    @staticmethod
    def execute(cloud_provider: CloudProvider,
                environment_context: BaseEnvironmentContext,
                include_rules: List[str] = None,
                exclude_rules: List[str] = None) -> List[RuleResponse]:
        all_rules: Dict[str, BaseRule] = RulesLoader.load(cloud_provider)
        exclude_rules = exclude_rules or []
        include_rules = include_rules or []
        rule_results: List[RuleResponse] = []
        if not include_rules:
            include_rules = all_rules.keys()
        for rule_id, rule_implementation in all_rules.items():
            if rule_id in include_rules and rule_id not in exclude_rules:
                try:
                    result = rule_implementation.run(environment_context, {})
                    rule_results.append(result)
                except Exception as exception:
                    logging.exception('run failed for rule {}, reason={}'.format(rule_id, str(exception)))
                    rule_results.append(RuleResponse(rule_id, RuleResultType.SKIPPED, reason=str(exception)))
        return rule_results
