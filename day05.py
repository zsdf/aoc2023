from datetime import datetime
import re
import sys
from typing import Tuple

# format

# seeds: x1 x2 xn
#
# X-to-Y map:
# D1 S1 R2
# Dn Sn Rn
# blank line

# where Dn Sn Rn means
# for i in 0..Rn: Dn + i -> Sn + i
# any omitted Sn maps to itself

SAMPLE_INPUT = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def abort(message: str) -> None:  # or never?
    print(message, file=sys.stderr)
    sys.exit(1)


def parse_input(lines: list[str]):
    initial_seeds = [int(n) for n in re.findall(r"\d+", lines[0])]

    almanac = {}
    reverse = {}

    src_type = ""
    dst_type = ""
    src = 0
    dst = 0
    range_len = 0
    m: list[Tuple[int, int, int]] = []
    r: list[Tuple[int, int, int]] = []

    # if we didn't trust the input to be well-formed we
    # would not want to parse the file like this
    for ln, line in enumerate(lines[2:] + [""]):
        if re.match(r"^$", line):
            almanac[src_type] = (dst_type, m)
            reverse[dst_type] = (src_type, r)
            m = []
            r = []
        elif match := re.match(r"(\w+)-to-(\w+) map:$", line):
            (src_type, dst_type) = match.groups()
        elif matches := re.findall(r"\d+", line):
            if len(matches) != 3:
                abort(f"error line {ln+2}: {line}")
            [dst, src, range_len] = [int(n) for n in matches]
            # the data contains ranges far too long to want to do this
            # for i in range(0, range_len):
            #     m[src + i] = dst + i
            m.append((dst, src, range_len))
            r.append((src, dst, range_len))
        else:
            abort(f"error line {ln+2}: {line}")

    return (initial_seeds, almanac, reverse)


def find_value(almanac, desired_type, src_type, src_val):
    """
    Finds the value in almanac corresponding to... better docstring
    """
    # NOTE: iteration vs recursion saves no noticable time
    # print(src_type, src_val)
    while src_type != desired_type:
        dst_type, m = almanac[src_type]

        dst_val = src_val
        # this is a small number - linear search ought to be okay.
        # we could sort it and use binary search but I doubt we'll benefit much
        for dst, src, count in m:
            if src <= src_val < src + count:
                dst_val = dst + src_val - src

        if dst_type == desired_type:
            return dst_val
        else:
            # return find_value(almanac, desired_type, dst_type, dst_val)
            src_type = dst_type
            src_val = dst_val


def solve1(lines: list[str]) -> int:
    """
    Find the lowest location number that corresponds to any initial seed.
    """
    (initial_seeds, almanac, _) = parse_input(lines)

    locations = []
    for seed in initial_seeds:
        locations.append(find_value(almanac, "location", "seed", seed))
    return min(locations)


# Questions:
# - Can we run this backwards? AKA iterate through location ids,
#   and stop when we get to a seed we have?
# - Can we collapse the map so we have one dict lookup instead of 7?
#   And if so, do we care? Making it 7x faster will not help much.
# - Can we stop iterating through the ranges, and map Range -> [Range]


def solve2_naive(lines: list[str]) -> int:
    """
    Same as part-1, but treat the initial seed as start1 len1 start2 len2 ....

    This is too slow to work (will take ~6hrs on my computer)
    """
    (initial_seeds, almanac, _) = parse_input(lines)
    seed_ranges = list(zip(initial_seeds[::2], initial_seeds[1::2]))

    min_location = -1
    for start, count in seed_ranges[0:1]:
        for seed in range(start, start + count):
            loc = find_value(almanac, "location", "seed", seed)
            if loc == 0:
                return 0
            elif min_location == -1 or loc < min_location:
                min_location = loc

    return min_location


def solve2_reverse(lines: list[str]) -> int:
    """
    Finds lowest location by finding the seed of every location starting at 0,
    until it finds a seed in our initial seed range check.

    This feels suboptimal, and maybe wouldn't work on arbitrary input?

    Runtime is ~3 minutes
    """
    (initial_seeds, _, almanac) = parse_input(lines)
    seed_ranges = list(zip(initial_seeds[::2], initial_seeds[1::2]))

    location = 0
    while True:
        seed = find_value(almanac, "seed", "location", location)
        for base, count in seed_ranges:
            if base <= seed < base + count:
                return location
        location += 1


def main():
    with open("data/day05", encoding="utf-8") as f:
        data = f.read().splitlines()

    assert solve1(SAMPLE_INPUT.splitlines()) == 35

    s1 = solve1(data)
    print(s1)
    assert s1 == 621354867

    solve2 = solve2_reverse
    assert solve2(SAMPLE_INPUT.splitlines()) == 46
    s2 = solve2(data)
    print(s2)
    assert s2 == 15880236


if __name__ == "__main__":
    main()
