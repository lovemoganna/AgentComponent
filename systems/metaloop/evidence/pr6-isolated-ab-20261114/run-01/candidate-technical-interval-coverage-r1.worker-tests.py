import copy
import unittest
from solution import total_covered


class TotalCoveredTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(total_covered([], 0, 10), {'covered': 0, 'rejected': []})

    def test_overlap_nesting_duplicates_and_touching(self):
        intervals = [(7, 9), (1, 5), (2, 3), (4, 7), (1, 5)]
        self.assertEqual(total_covered(intervals, 0, 10), {'covered': 8, 'rejected': []})

    def test_clipping_outside_and_half_open_boundaries(self):
        intervals = [(-10, 0), (10, 20), (-3, 2), (8, 13), (4, 6)]
        self.assertEqual(total_covered(intervals, 0, 10), {'covered': 6, 'rejected': []})

    def test_spanning_interval(self):
        self.assertEqual(total_covered([(-100, 100)], -5, 5), {'covered': 10, 'rejected': []})

    def test_rejections_in_input_order(self):
        intervals = [None, (), [1], [1, 2, 3], '12', {1, 2},
                     (True, 2), (0, False), (1.0, 2), (0, '2'),
                     (3, 3), (5, 4), (-8, -4), [1, 3], (20, 10)]
        self.assertEqual(total_covered(intervals, 0, 10),
                         {'covered': 2, 'rejected': list(range(12)) + [14]})

    def test_invalid_bounds(self):
        for start, end in [(True, 5), (0, True), (0.0, 5), (0, 5.0),
                           ('0', 5), (0, None), (2, 2), (3, 2)]:
            with self.subTest(start=start, end=end):
                with self.assertRaises(ValueError):
                    total_covered([], start, end)

    def test_does_not_mutate_inputs(self):
        intervals = [[8, 12], [-2, 3], [2, 7], [9, 9]]
        original = copy.deepcopy(intervals)
        self.assertEqual(total_covered(intervals, 0, 10), {'covered': 9, 'rejected': [3]})
        self.assertEqual(intervals, original)

    def test_large_integer_precision(self):
        base = 10 ** 100
        self.assertEqual(total_covered([(base, base + 7), (base + 5, base + 9)],
                                       base, base + 20),
                         {'covered': 9, 'rejected': []})

    def test_exhaustive_small_valid_inputs(self):
        candidates = [(a, b) for a in range(-2, 4) for b in range(a + 1, 5)]
        for first in candidates:
            for second in candidates:
                intervals = [first, second]
                expected = sum(any(a <= x < b for a, b in intervals)
                               for x in range(-1, 3))
                self.assertEqual(total_covered(intervals, -1, 3),
                                 {'covered': expected, 'rejected': []})


if __name__ == '__main__':
    unittest.main()
