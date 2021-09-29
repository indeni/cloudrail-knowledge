import unittest

from cloudrail.knowledge.utils.string_utils import StringUtils


class TestStringUtils(unittest.TestCase):

    def test_clean_markdown(self):
        # Arrange
        original_str = '<Hi> how are <You>?'
        # Act
        clean_str = StringUtils.clean_markdown(original_str)
        # Assert
        self.assertEqual('Hi how are You?', clean_str)

    def test_convert_to_bool_true(self):
        # Act
        result = StringUtils.convert_to_bool('TrUe')
        # Assert
        self.assertTrue(result)

    def test_convert_to_bool_false(self):
        # Act
        result = StringUtils.convert_to_bool('FaLSe')
        # Assert
        self.assertFalse(result)

    def test_convert_to_bool_none(self):
        # Act
        result = StringUtils.convert_to_bool(None)
        # Assert
        self.assertIsNone(result)

    def test_convert_to_bool_invalid(self):
        # Act
        result = StringUtils.convert_to_bool('asdasd')
        # Assert
        self.assertIsNone(result)

    def test_convert_strs_to_bool_true(self):
        # Act
        result = StringUtils.convert_strs_to_bool(['TrUe'])
        # Assert
        self.assertTrue(result)

    def test_convert_strs_to_bool_false(self):
        # Act
        result = StringUtils.convert_strs_to_bool(['False'])
        # Assert
        self.assertFalse(result)

    def test_convert_strs_to_bool_false_and_true(self):
        # Act
        result = StringUtils.convert_strs_to_bool(['False', 'TRUE'])
        # Assert
        self.assertIsNone(result)

    def test_convert_strs_to_bool_empty(self):
        # Act
        result = StringUtils.convert_strs_to_bool([])
        # Assert
        self.assertIsNone(result)
