import unittest
from cloudrail.knowledge.rules.rules_metadata_store import CloudrailRulesMetadataStore

class TestRulesMetadataStore(unittest.TestCase):


    def test_rules_metadata_store(self):
        rules_metadata_store = CloudrailRulesMetadataStore()

        self.assertTrue(len(rules_metadata_store.list_rules_metadata()) > 0)

    def test_get_rule_metadata_by_id(self):
        rule_id = 'public_access_security_groups_postgres_port_rule'

        res = CloudrailRulesMetadataStore().get_by_rule_id(rule_id)

        self.assertEqual(res.rule_id, rule_id)

    def test_get_rule_metadata_by_id_when_rule_id_not_found(self):
        rule_id = 'public_access_security_groups_postgresh_port_rule'

        rule_metadata = CloudrailRulesMetadataStore().get_by_rule_id(rule_id)

        self.assertIsNone(rule_metadata)
