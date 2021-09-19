from typing import List

from cloudrail.knowledge.drift_detection.drift_detection_result import Drift
from test.knowledge.context.drift.base_drift_test import BaseDriftTest, drift_test


class TestRds(BaseDriftTest):

    def get_component(self):
        return 'security_group'

    @drift_test(module_path="add_rule_to_existing_security_group")
    def test_add_rule_to_existing_security_group(self, results: List[Drift]):
        security_group = next(res for res in results
                              if res.resource_type == 'Security group'
                              and res.resource_id == 'aws_security_group.security_group_test')
        live_inbound_permissions = security_group.resource_live['inbound_permissions']
        iac_inbound_permissions = security_group.resource_iac['inbound_permissions']
        live_global_rule = next((rule for rule in live_inbound_permissions if rule['property_value'] == '0.0.0.0/0'), None)
        iac_global_rule = next((rule for rule in iac_inbound_permissions if rule['property_value'] == '0.0.0.0/0'), None)
        self.assertIsNotNone(live_global_rule)
        self.assertIsNone(iac_global_rule)
