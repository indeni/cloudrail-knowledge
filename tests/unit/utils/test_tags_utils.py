import unittest

from cloudrail.knowledge.utils.hash_utils import to_hashcode
from cloudrail.knowledge.utils.tags_utils import get_aws_tags, extract_name_from_tags


class TestTagsUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.salt = '00000000-0000-0000-0000-000000000000'
        cls.possible_tag_keys = ['tags', 'Tags', 'TagSet']
        cls.expected_name = 'myname'
        cls.name_key = 'Name'
        cls.key1 = 'key1'
        cls.val1 = 'someval1'
        cls.key2 = 'key2'
        cls.val2 = 'someval2'
        cls.val1_expected_key = cls.key1 + '_hashcode'
        cls.val2_expected_key = cls.key2 + '_hashcode'
        cls.val1_expected_value = to_hashcode(cls.val1, cls.salt)
        cls.val2_expected_value = to_hashcode(cls.val2, cls.salt)
        cls.fail_msg = 'assertion failed for tag_key {0}'

    def test_get_aws_tags_empty_dict(self):
        # Arrange
        raw_aws_data = {}
        # Act
        result = get_aws_tags(raw_aws_data)
        # Assert
        self.assertEqual(result, {})

    def test_get_aws_tags_no_tags(self):
        # Arrange
        raw_aws_data = {'somekey': 'somevalue', 'salt': self.salt}
        # Act
        result = get_aws_tags(raw_aws_data)
        # Assert
        self.assertEqual(result, {})

    def test_get_aws_tags_with_tags_as_dict(self):
        # Arrange
        for possible_tags_key in self.possible_tag_keys:
            raw_aws_data_with_tags_as_dict = self._create_raw_aws_data_with_tags_as_dict(possible_tags_key)
            # Act
            result = get_aws_tags(raw_aws_data_with_tags_as_dict)
            # Assert
            self._assert_get_aws_tags_results(result, possible_tags_key)

    def test_get_aws_tags_with_tags_as_list(self):
        # Arrange
        for possible_tags_key in self.possible_tag_keys:
            raw_aws_data_with_tags_as_list = self._create_raw_aws_data_with_tags_as_list(possible_tags_key)
            # Act
            result = get_aws_tags(raw_aws_data_with_tags_as_list)
            # Assert
            self._assert_get_aws_tags_results(result, possible_tags_key)

    def test_extract_name_from_tags_as_dict(self):
        # Arrange
        for possible_tags_key in self.possible_tag_keys:
            raw_aws_data_with_tags_as_dict = self._create_raw_aws_data_with_tags_as_dict(possible_tags_key)
            # Act
            name = extract_name_from_tags(raw_aws_data_with_tags_as_dict)
            # Assert
            self.assertEqual(name, self.expected_name, self.fail_msg.format(possible_tags_key))

    def test_extract_name_from_tags_as_list(self):
        # Arrange
        for possible_tags_key in self.possible_tag_keys:
            raw_aws_data_with_tags_as_list = self._create_raw_aws_data_with_tags_as_list(possible_tags_key)
            # Act
            name = extract_name_from_tags(raw_aws_data_with_tags_as_list)
            # Assert
            self.assertEqual(name, self.expected_name, self.fail_msg.format(possible_tags_key))

    def _assert_get_aws_tags_results(self, result: dict, tag_key: str):
        fail_msg = self.fail_msg.format(tag_key)
        self.assertIn(self.val1_expected_key, result, fail_msg)
        self.assertEqual(result[self.val1_expected_key], self.val1_expected_value, fail_msg)
        self.assertIn(self.val2_expected_key, result, fail_msg)
        self.assertEqual(result[self.val2_expected_key], self.val2_expected_value, fail_msg)
        self.assertIn(self.name_key, result, fail_msg)
        self.assertEqual(result['Name'], self.expected_name, fail_msg)

    def _create_raw_aws_data_with_tags_as_dict(self, tag_key: str):
        return {
            'salt': self.salt,
            tag_key: {
                self.key1: self.val1,
                self.key2: self.val2,
                self.name_key: self.expected_name
            }
        }

    def _create_raw_aws_data_with_tags_as_list(self, tag_key: str):
        return {
            'salt': self.salt,
            tag_key: [
                {'Key': self.key1, 'Value': self.val1},
                {'Key': self.key2, 'Value': self.val2},
                {'Key': self.name_key, 'Value': self.expected_name}
            ]
        }
