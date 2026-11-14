import copy
import itertools
import unittest

from solution import total_covered


class TotalCoveredTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(total_covered([], 0, 10), {'covered': 0, 'rejected': []})

    def test_overlap_nesting_duplicates_and_touching(self):
        intervals = [(7, 12), (1, 5), (2, 3), (1, 5), (5, 7)]
        self.assertEqual(total_covered(intervals, 0, 10), {'covered': 9, 'rejected': []})

    def test_clipping_and_valid_outside_intervals(self):
        intervals = [(-20, -10), (-10, 0), (10, 20), (20, 30), (-3, 2), (8, 15)]
        self.assertEqual(total_covered(intervals, 0, 10), {'covered': 4, 'rejected': []})
        self.assertEqual(total_covered([(-100, 100)], -5, 5), {'covered': 10, 'rejected': []})

    def test_rejected_indices_in_input_order(self):
        intervals = [None, (0, 2), '12', [], [1], [1, 2, 3],
                     (True, 3), (1, False), (1.0, 3), (1, '3'),
                     (3, 3), (4, 2), {1, 2}, {'a': 1, 'b': 2},
                     (-5, -2), [3, 5], (20, 10)]
        self.assertEqual(total_covered(intervals, 0, 10), {
            'covered': 4,
            'rejected': [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16],
        })

    def test_invalid_bounds(self):
        for start, end in [(True, 3), (0, False), (0.0, 3), (0, 3.0),
                           ('0', 3), (0, None), (2, 2), (3, 2)]:
            with self.subTest(start=start, end=end):
                with self.assertRaises(ValueError):
                    total_covered([], start, end)

    def test_no_mutation(self):
        intervals = [[5, 9], [0, 4], [3, 7], [True, 8], []]
        original = copy.deepcopy(intervals)
        total_covered(intervals, 1, 8)
        self.assertEqual(intervals, original)

    def test_arbitrary_precision_integer_result(self):
        size = 10 ** 100
        result = total_covered([(-size, size)], -size, size)
        self.assertEqual(result, {'covered': 2 * size, 'rejected': []})
        self.assertIs(type(result['covered']), int)

    def test_exhaustive_small_pairs_against_unit_cell_oracle(self):
        candidates = list(itertools.combinations(range(-3, 4), 2))
        for first, second in itertools.product(candidates, repeat=2):
            intervals = [first, second]
            expected = sum(any(a <= x < b for a, b in intervals)
                           for x in range(-2, 3))
            with self.subTest(intervals=intervals):
                self.assertEqual(total_covered(intervals, -2, 3),
                                 {'covered': expected, 'rejected': []})


if __name__ == '__main__':
    unittest.main()
