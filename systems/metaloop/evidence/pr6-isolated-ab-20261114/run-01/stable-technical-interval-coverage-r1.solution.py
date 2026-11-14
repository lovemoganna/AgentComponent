def total_covered(intervals, start, end):
    """Return union coverage within [start, end) and invalid interval indices."""
    def is_integer(value):
        return isinstance(value, int) and not isinstance(value, bool)

    if not is_integer(start) or not is_integer(end) or end <= start:
        raise ValueError('start and end must be non-bool integers with start < end')

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
    if clipped:
        left, right = clipped[0]
        for a, b in clipped[1:]:
            if a <= right:
                right = max(right, b)
            else:
                covered += right - left
                left, right = a, b
        covered += right - left
    return {'covered': covered, 'rejected': rejected}
