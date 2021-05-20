import os

import json
import unittest

import jsonpickle
from cloudrail.knowledge.utils.connection_utils import get_allowing_public_access_on_ports


class TestConnectionUtils(unittest.TestCase):

    def test_public_connection_exists(self):
        redshift = self._get_scenario_object('test_public_connection_exists')
        res = get_allowing_public_access_on_ports(redshift, [5439])

        self.assertTrue(res)
        self.assertEqual(res.name, 'aws_security_group.nondefault.id')

    def test_no_public_connection_exists(self):
        redshift = self._get_scenario_object('test_no_public_connection_exists')
        res = get_allowing_public_access_on_ports(redshift, [5439])

        self.assertFalse(res)

    @staticmethod
    def _get_scenario_object(scenario: str):
        current_path = os.path.dirname(os.path.abspath(__file__))
        scenarios_json_path = os.path.join(current_path, 'test_connection_utils_scenarios.json')
        with open(scenarios_json_path, 'r') as scenarios:
            scenarios_json = json.load(scenarios)
            scenario_dict = scenarios_json[scenario]
            pickled_object = json.dumps(scenario_dict)

        jsonpickle.decode(pickled_object)
        return jsonpickle.decode(str(pickled_object))
