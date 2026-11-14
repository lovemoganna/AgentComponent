import copy
import itertools
import unittest

from solution import total_covered


class TotalCoveredTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(total_covered([], 0, 10), {'covered': 0, 'rejected': []})

    def test_overlap_nesting_duplicates_touching_and_gaps(self):
        intervals = [(8, 12), (1, 5), (2, 3), (1, 5), (5, 7)]
        self.assertEqual(total_covered(intervals, 0, 10), {'covered': 8, 'rejected': []})

    def test_clipping_and_valid_outside_intervals(self):
        intervals = [(-10, -5), (-5, 0), (10, 20), (20, 30), (-2, 3), (8, 15)]
        self.assertEqual(total_covered(intervals, 0, 10), {'covered': 5, 'rejected': []})
        self.assertEqual(total_covered([(-100, 100)], 0, 10), {'covered': 10, 'rejected': []})

    def test_invalid_intervals_and_rejection_order(self):
        intervals = [None, 7, '12', {1, 2}, {0: 1, 1: 2}, [], [1],
                     [1, 2, 3], [True, 2], [0, False], [1.0, 2],
                     [1, '2'], [2, 2], [4, 3], [20, 10], (0, 2), [3, 5]]
        self.assertEqual(total_covered(intervals, 0, 10),
                         {'covered': 4, 'rejected': list(range(15))})

    def test_invalid_bounds(self):
        for bounds in [(True, 5), (0, False), (0.0, 5), (0, 5.0),
                       ('0', 5), (0, None), (2, 2), (3, 2)]:
            with self.subTest(bounds=bounds):
                with self.assertRaises(ValueError):
                    total_covered([], *bounds)

    def test_bounds_checked_before_consuming_intervals(self):
        def intervals():
            raise AssertionError('intervals must not be consumed')
            yield
        with self.assertRaises(ValueError):
            total_covered(intervals(), 1, 1)

    def test_does_not_mutate_inputs(self):
        intervals = [[5, 12], [-2, 4], [4, 4], (3, 8)]
        original = copy.deepcopy(intervals)
        self.assertEqual(total_covered(intervals, 0, 10),
                         {'covered': 10, 'rejected': [2]})
        self.assertEqual(intervals, original)

    def test_negative_and_large_integer_bounds(self):
        self.assertEqual(total_covered([(-9, -4), (-6, -1)], -8, -2),
                         {'covered': 6, 'rejected': []})
        n = 10 ** 100
        result = total_covered([(n - 1, n + 3), (n + 2, n + 20)], n, n + 10)
        self.assertEqual(result, {'covered': 10, 'rejected': []})
        self.assertIs(type(result['covered']), int)

    def test_exhaustive_small_union_against_unit_cell_oracle(self):
        candidates = list(itertools.combinations(range(-2, 4), 2))
        for count in range(4):
            for intervals in itertools.combinations_with_replacement(candidates, count):
                expected = sum(any(a <= x < b for a, b in intervals)
                               for x in range(-1, 3))
                with self.subTest(intervals=intervals):
                    self.assertEqual(total_covered(intervals, -1, 3),
                                     {'covered': expected, 'rejected': []})


if __name__ == '__main__':
    unittest.main()
