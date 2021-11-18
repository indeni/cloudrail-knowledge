import unittest

from cloudrail.knowledge.utils.utils import is_iterable_with_values


class TestCheckIterableHasValue(unittest.TestCase):

    def test_empty_list(self):
        # Arrange
        testing_list = []
        # Act
        bool_value = is_iterable_with_values(testing_list)
        # Assert
        self.assertFalse(bool_value)

    def test_list_with_none_value(self):
        # Arrange
        testing_list = [None]
        # Act
        bool_value = is_iterable_with_values(testing_list)
        # Assert
        self.assertFalse(bool_value)

    def test_list_with_one_none_value(self):
        # Arrange
        testing_list = [None, 'value']
        # Act
        bool_value = is_iterable_with_values(testing_list)
        # Assert
        self.assertTrue(bool_value)

    def test_list_with_multiple_none_values(self):
        # Arrange
        testing_list = [None, None]
        # Act
        bool_value = is_iterable_with_values(testing_list)
        # Assert
        self.assertFalse(bool_value)

    def test_list_with_none_value_and_bool_value_1(self):
        # Arrange
        testing_list = [None, False]
        # Act
        bool_value = is_iterable_with_values(testing_list)
        # Assert
        self.assertTrue(bool_value)

    def test_list_with_none_value_and_bool_value_2(self):
        # Arrange
        testing_list = [None, True]
        # Act
        bool_value = is_iterable_with_values(testing_list)
        # Assert
        self.assertTrue(bool_value)

    def test_simple_list(self):
        # Arrange
        testing_list = ['value_1', 'value_2']
        # Act
        bool_value = is_iterable_with_values(testing_list)
        # Assert
        self.assertTrue(bool_value)

    def test_simple_set(self):
        # Arrange
        testing_set = {'value_1', 'value_2'}
        # Act
        bool_value = is_iterable_with_values(testing_set)
        # Assert
        self.assertTrue(bool_value)

    def test_set_with_none_value(self):
        # Arrange
        testing_set = {None}
        # Act
        bool_value = is_iterable_with_values(testing_set)
        # Assert
        self.assertFalse(bool_value)

    def test_set_with_one_none_value(self):
        # Arrange
        testing_set = {None, 'value'}
        # Act
        bool_value = is_iterable_with_values(testing_set)
        # Assert
        self.assertTrue(bool_value)

    def test_set_with_multiple_none_values(self):
        # Arrange
        testing_set = {None, None}
        # Act
        bool_value = is_iterable_with_values(testing_set)
        # Assert
        self.assertFalse(bool_value)

    def test_set_with_none_value_and_bool_value_1(self):
        # Arrange
        testing_set = {None, False}
        # Act
        bool_value = is_iterable_with_values(testing_set)
        # Assert
        self.assertTrue(bool_value)

    def test_set_with_none_value_and_bool_value_2(self):
        # Arrange
        testing_set = {None, True}
        # Act
        bool_value = is_iterable_with_values(testing_set)
        # Assert
        self.assertTrue(bool_value)
