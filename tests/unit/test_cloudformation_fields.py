import unittest
import os
import yaml

from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType

class TestCloudformationFields(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cfn_resources_enum = set(map(lambda resource: resource.value, CloudformationResourceType))
        cls.cfn_fields: set = {key for key in cls._get_cfn_yaml_fields().keys() if key != 'common'}
        cls._exclude_cfn_resources()

    def test_cfn_fields_not_empty(self):
        self.assertTrue(len(self.cfn_fields) > 0)

    def test_cfn_fields_equal_to_resources(self):
        self.assertEqual(len(self.cfn_fields), len(self.cfn_resources_enum))

    def test_all_resources_in_cfn_fields(self):
        self.assertEqual(len(self.cfn_resources_enum - self.cfn_fields), 0)

    @staticmethod
    def _get_cfn_yaml_fields():
        current_path = os.path.dirname(os.path.abspath(__file__))
        rules_metadata_path = os.path.join(current_path, '../../cloudrail/knowledge/context/aws/cloudformation/cloudformation_fields.yaml')
        with open(rules_metadata_path, 'r') as file:
            return yaml.load(file)

    @classmethod
    def _exclude_cfn_resources(cls):
        excluded_cfn_resources_list = ('AWS::EC2::TransitGateway',
                                       'AWS::EC2::InternetGateway',
                                       'AWS::CloudFront::CloudFrontOriginAccessIdentity')
        cls.cfn_fields = {field for field in cls.cfn_fields if field not in excluded_cfn_resources_list}
        cls.cfn_resources_enum = {field for field in cls.cfn_resources_enum if field not in excluded_cfn_resources_list}
