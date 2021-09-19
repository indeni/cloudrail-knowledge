import unittest

from cloudrail.knowledge.utils.port_utils import \
    add_port_range, \
    add_port_ranges, \
    remove_port_range, \
    remove_port_ranges, \
    intersect_port_range, \
    intersect_port_ranges


class TestPortUtils(unittest.TestCase):
    def test_add_port_range(self) -> None:
        # Arrange:
        current_ranges = [(10, 20), (30, 40), (50, 60)]

        # Act / Assert when new range is left of current ranges:
        self.assertEqual([(1, 5), (10, 20), (30, 40), (50, 60)], add_port_range(current_ranges, (1, 5)))
        self.assertEqual([(1, 20), (30, 40), (50, 60)], add_port_range(current_ranges, (1, 10)))
        self.assertEqual([(1, 20), (30, 40), (50, 60)], add_port_range(current_ranges, (1, 15)))
        self.assertEqual([(1, 20), (30, 40), (50, 60)], add_port_range(current_ranges, (1, 20)))
        self.assertEqual([(1, 25), (30, 40), (50, 60)], add_port_range(current_ranges, (1, 25)))
        self.assertEqual([(1, 40), (50, 60)], add_port_range(current_ranges, (1, 30)))
        self.assertEqual([(1, 60)], add_port_range(current_ranges, (1, 55)))
        self.assertEqual([(1, 60)], add_port_range(current_ranges, (1, 60)))
        self.assertEqual([(1, 70)], add_port_range(current_ranges, (1, 70)))

        # Act / Assert when new range is inside of current ranges:
        self.assertEqual([(10, 20), (30, 40), (50, 60)], add_port_range(current_ranges, (11, 15)))
        self.assertEqual([(10, 25), (30, 40), (50, 60)], add_port_range(current_ranges, (11, 25)))
        self.assertEqual([(10, 25), (30, 40), (50, 60)], add_port_range(current_ranges, (21, 25)))
        self.assertEqual([(10, 20), (30, 40), (50, 70)], add_port_range(current_ranges, (55, 70)))

        # Act / Assert when new range is right of current ranges:
        self.assertEqual([(10, 20), (30, 40), (50, 70)], add_port_range(current_ranges, (60, 70)))
        self.assertEqual([(10, 20), (30, 40), (50, 70)], add_port_range(current_ranges, (61, 70)))
        self.assertEqual([(10, 20), (30, 40), (50, 60), (65, 70)], add_port_range(current_ranges, (65, 70)))

    def test_add_port_ranges(self) -> None:
        # Arrange:
        current_ranges = [(10, 20), (30, 40), (50, 60)]

        # Act / Assert:
        self.assertEqual([(1, 5), (10, 25), (30, 40), (50, 60)], add_port_ranges(current_ranges, [(1, 5), (19, 25)]))

    def test_remove_port_range(self) -> None:
        # Arrange:
        current_ranges = [(10, 20), (30, 40), (50, 60)]

        # Act / Assert when new range is left of current ranges:
        self.assertEqual([(10, 20), (30, 40), (50, 60)], remove_port_range(current_ranges, (1, 5)))
        self.assertEqual([(11, 20), (30, 40), (50, 60)], remove_port_range(current_ranges, (1, 10)))
        self.assertEqual([(16, 20), (30, 40), (50, 60)], remove_port_range(current_ranges, (1, 15)))
        self.assertEqual([(30, 40), (50, 60)], remove_port_range(current_ranges, (1, 20)))
        self.assertEqual([(30, 40), (50, 60)], remove_port_range(current_ranges, (1, 25)))
        self.assertEqual([(31, 40), (50, 60)], remove_port_range(current_ranges, (1, 30)))
        self.assertEqual([(56, 60)], remove_port_range(current_ranges, (1, 55)))
        self.assertEqual([], remove_port_range(current_ranges, (1, 60)))
        self.assertEqual([], remove_port_range(current_ranges, (1, 70)))

        # Act / Assert when new range is inside of current ranges:
        self.assertEqual([(10, 10), (16, 20), (30, 40), (50, 60)], remove_port_range(current_ranges, (11, 15)))
        self.assertEqual([(10, 10), (30, 40), (50, 60)], remove_port_range(current_ranges, (11, 25)))
        self.assertEqual([(10, 20), (30, 40), (50, 60)], remove_port_range(current_ranges, (21, 25)))
        self.assertEqual([(10, 20), (30, 40), (50, 54)], remove_port_range(current_ranges, (55, 70)))
        #
        # # Act / Assert when new range is right of current ranges:
        self.assertEqual([(10, 20), (30, 40), (50, 59)], remove_port_range(current_ranges, (60, 70)))
        self.assertEqual([(10, 20), (30, 40), (50, 60)], remove_port_range(current_ranges, (65, 70)))

    def test_remove_port_ranges(self) -> None:
        # Arrange:
        current_ranges = [(10, 20), (30, 40), (50, 60)]

        # Act / Assert:
        self.assertEqual([(16, 20), (36, 40), (50, 60)], remove_port_ranges(current_ranges, [(1, 15), (30, 35)]))

    def test_intersect_port_range(self) -> None:
        # Arrange:
        current_ranges = [(10, 20), (30, 40), (50, 60)]

        # Act / Assert when new range is left of current ranges:
        self.assertEqual([], intersect_port_range(current_ranges, (1, 5)))
        self.assertEqual([(10, 10)], intersect_port_range(current_ranges, (1, 10)))
        self.assertEqual([(10, 15)], intersect_port_range(current_ranges, (1, 15)))
        self.assertEqual([(10, 20)], intersect_port_range(current_ranges, (1, 20)))
        self.assertEqual([(10, 20)], intersect_port_range(current_ranges, (1, 25)))
        self.assertEqual([(10, 20), (30, 30)], intersect_port_range(current_ranges, (1, 30)))
        self.assertEqual([(10, 20), (30, 40), (50, 55)], intersect_port_range(current_ranges, (1, 55)))
        self.assertEqual([(10, 20), (30, 40), (50, 60)], intersect_port_range(current_ranges, (1, 60)))
        self.assertEqual([(10, 20), (30, 40), (50, 60)], intersect_port_range(current_ranges, (1, 70)))
        #
        # Act / Assert when new range is inside of current ranges:
        self.assertEqual([(11, 15)], intersect_port_range(current_ranges, (11, 15)))
        self.assertEqual([(11, 20)], intersect_port_range(current_ranges, (11, 25)))
        self.assertEqual([], intersect_port_range(current_ranges, (21, 25)))
        self.assertEqual([(55, 60)], intersect_port_range(current_ranges, (55, 70)))

        # Act / Assert when new range is right of current ranges:
        self.assertEqual([(60, 60)], intersect_port_range(current_ranges, (60, 70)))
        self.assertEqual([], intersect_port_range(current_ranges, (61, 70)))
        self.assertEqual([], intersect_port_range(current_ranges, (65, 70)))

    def test_intersect_port_ranges(self) -> None:
        # Arrange:
        current_ranges = [(10, 20), (30, 40), (50, 60)]

        # Act / Assert:
        self.assertEqual([(10, 15), (30, 35)], intersect_port_ranges(current_ranges, [(1, 15), (30, 35)]))
