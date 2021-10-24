from typing import Dict, List

from cloudrail.knowledge.rules.base_rule import BaseRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_instance_no_public_ip_rule import \
    SqlDatabaseNoPublicIpRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_database_ssl_required_rule import SqlDatabaseSslRequiredRule
from cloudrail.knowledge.rules.gcp.non_context_aware.sql_restrict_trusted_ip_rule import SqlDatabaseRestrictTrustedIpRule
from cloudrail.knowledge.rules.abstract_rules_loader import AbstractRulesLoader


class GcpRulesLoader(AbstractRulesLoader):

    def load(self) -> Dict[str, BaseRule]:
        rules: List[BaseRule] = [
            SqlDatabaseSslRequiredRule(),
            SqlDatabaseRestrictTrustedIpRule(),
            SqlDatabaseNoPublicIpRule()
        ]
        return {rule.get_id(): rule for rule in rules}
