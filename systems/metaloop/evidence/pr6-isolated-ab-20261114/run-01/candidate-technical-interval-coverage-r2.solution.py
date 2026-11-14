def total_covered(intervals, start, end):
    """Return union coverage in [start, end) and invalid interval indices."""
    def is_integer(value):
        return isinstance(value, int) and not isinstance(value, bool)

    if not is_integer(start) or not is_integer(end) or end <= start:
        raise ValueError('start and end must be non-bool integers with end > start')

    clipped = []
    rejected = []
    for index, interval in enumerate(intervals):
        if not isinstance(interval, (list, tuple)) or len(interval) != 2:
            rejected.append(index)
            continue
        a, b = interval
        if not is_integer(a) or not is_integer(b) or a >= b:
            rejected.append(index)
            continue
        left, right = max(a, start), min(b, end)
        if left < right:
            clipped.append((left, right))

    clipped.sort()
    covered = 0
    merged_end = start
    for left, right in clipped:
        covered += max(0, right - max(left, merged_end))
        merged_end = max(merged_end, right)
    return {'covered': covered, 'rejected': rejected}
