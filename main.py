import sys


def main():
    timestamps = parse_input()
    total_cov = merge_intervals_and_calculate_total_cov(timestamps)
    print(calculate_max_coverage(timestamps, total_cov))


def parse_input():
    timestamps = []
    N = int(sys.stdin.readline().strip())

    for _ in range(N):
        times = sys.stdin.readline().strip().split(" ")
        timestamps.append([int(times[0]), int(times[1])])

    timestamps.sort(key=lambda x: x[0])

    return timestamps


def merge_intervals_and_calculate_total_cov(timestamps):
    # Copy to ensure we don't change original array
    timestamps_copy = [row[:] for row in timestamps]

    # Merge intervals
    merged = []
    for ts in timestamps_copy:
        if not merged or merged[-1][1] < ts[0]:
            merged.append(ts)
        else:
            merged[-1][1] = max(merged[-1][1], ts[1])

    # Calculate total coverage
    total_cov = 0
    for interval in merged:
        total_cov += interval[1] - interval[0]

    return total_cov


def calculate_max_coverage(timestamps, total_cov):
    min_nonoverlap_cov = float("inf")

    prev = None
    curr = 0
    next = 1 if len(timestamps) > 1 else None

    while curr < len(timestamps):
        curr_coverage = timestamps[curr][1] - timestamps[curr][0]

        if prev is None and next is None:
            # Only one interval
            return 0
        elif prev is None:
            # First interval
            overlap = timestamps[curr][1] - timestamps[next][0]
            min_nonoverlap_cov = min(
                min_nonoverlap_cov, max(curr_coverage - overlap, 0)
            )
        elif next is None:
            # Last interval
            overlap = timestamps[prev][1] - timestamps[curr][0]
            min_nonoverlap_cov = min(
                min_nonoverlap_cov, max(curr_coverage - overlap, 0)
            )
        else:
            # Middle interval
            overlap_one = timestamps[prev][1] - timestamps[curr][0]
            overlap_two = timestamps[curr][1] - timestamps[next][0]

            min_nonoverlap_cov = min(
                min_nonoverlap_cov, max(curr_coverage - overlap_one - overlap_two, 0)
            )

        if prev is not None:
            prev += 1
        else:
            prev = 0

        curr += 1

        if next is not None and next + 1 < len(timestamps):
            next += 1
        else:
            next = None

    return total_cov - min_nonoverlap_cov


main()
