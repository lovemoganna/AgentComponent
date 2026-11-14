import copy
import itertools
import unittest
from solution import total_covered


class TotalCoveredTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(total_covered([], 0, 10), {'covered': 0, 'rejected': []})

    def test_overlap_nesting_duplicates_and_adjacency(self):
        intervals = [(8, 12), (1, 5), (3, 9), (2, 4), (1, 5), (12, 14)]
        self.assertEqual(total_covered(intervals, 0, 20), {'covered': 13, 'rejected': []})

    def test_clipping_outside_and_half_open_boundaries(self):
        intervals = [(-10, 0), (10, 20), (-5, 3), (7, 15), (4, 6)]
        self.assertEqual(total_covered(intervals, 0, 10), {'covered': 8, 'rejected': []})

    def test_rejected_indices_in_input_order(self):
        intervals = [None, (0, 2), [1], [1, 2, 3], '12',
                     (True, 3), (0, False), (1.0, 3), (1, '3'),
                     (3, 3), (5, 4), {'a': 1, 'b': 2}, (-10, -5)]
        self.assertEqual(total_covered(intervals, 0, 10),
                         {'covered': 2, 'rejected': [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]})

    def test_invalid_bounds(self):
        for start, end in [(False, 3), (0, True), (0.0, 3), (0, 3.0),
                           ('0', 3), (0, None), (2, 2), (3, 2)]:
            with self.subTest(start=start, end=end):
                with self.assertRaises(ValueError):
                    total_covered([], start, end)

    def test_no_mutation(self):
        intervals = [[8, 15], [1, 4], [3, 9], [2], (0, 2)]
        before = copy.deepcopy(intervals)
        total_covered(intervals, 0, 10)
        self.assertEqual(intervals, before)

    def test_large_integer_result(self):
        n = 10 ** 100
        result = total_covered([(-n, 0), (0, n)], -n, n)
        self.assertEqual(result, {'covered': 2 * n, 'rejected': []})
        self.assertIs(type(result['covered']), int)

    def test_iterable_input(self):
        self.assertEqual(total_covered(iter([(1, 3), None, (2, 5)]), 0, 6),
                         {'covered': 4, 'rejected': [1]})

    def test_exhaustive_small_cases_against_discrete_oracle(self):
        candidates = list(itertools.combinations(range(-2, 4), 2))
        for intervals in itertools.product(candidates, repeat=3):
            expected = sum(any(a <= x < b for a, b in intervals)
                           for x in range(-1, 3))
            self.assertEqual(total_covered(intervals, -1, 3),
                             {'covered': expected, 'rejected': []}, intervals)


if __name__ == '__main__':
    unittest.main()
