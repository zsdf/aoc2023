from dataclasses import dataclass
import re
from typing import Tuple
import sys

# (79,93) -> (81,95)
# (55,68) -> (57,70)
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


@dataclass
class Mapping:
    src: range
    dst: range


def parse_seeds(line: str) -> list[range]:
    xs = [int(n) for n in re.findall(r"\d+", line)]
    return [range(start, start + count) for start, count in zip(xs[::2], xs[1::2])]


def parse_mappings(lines: list[str]) -> dict[str, Tuple[str, list[Mapping]]]:
    mappings = {}
    ranges: list[Mapping] = []
    stype = ""
    dtype = ""

    for line in lines:
        if match := re.match(r"(\w+)-to-(\w+) map:", line):
            stype, dtype = match.groups()
            ranges = []
        elif matches := [int(n) for n in re.findall(r"\d+", line)]:
            [dst, src, count] = matches
            srange = range(src, src + count)
            drange = range(dst, dst + count)
            if len(srange) == 0 or len(drange) == 0:
                raise RuntimeError("parsing error")
            ranges.append(Mapping(src=srange, dst=drange))
        elif re.match(r"$", line):
            mappings[stype] = (dtype, ranges)
        else:
            raise RuntimeError("what happened here: " + line)
    if len(ranges) > 0:
        mappings[stype] = (dtype, ranges)
    return mappings


def project(r: range, m: Mapping) -> range:
    """Projects range r from src to dst"""
    offset = m.dst.start - m.src.start
    return range(r.start + offset, r.stop + offset)


def split(r: range, d: range) -> Tuple[range, range]:
    """Returns the portition of r contained by d, and the remainder"""
    pass


def contains(r: range, d: range) -> bool:
    """Does range r contain range d entirely?"""
    return d.start in r and d.stop in r


def find_ranges(query: range, mappings: list[Mapping]) -> list[range]:
    ranges: list[range] = []
    if len(query) == 0:
        return []

    for mapping in mappings:
        if len(query) == 0:
            break

        if contains(mapping.src, query):
            overlap = query
            remainder = range(0, 0)
        elif contains(query, mapping.src):
            overlap = mapping.src
            r1 = range(query.start, mapping.src.start)
            r2 = range(mapping.src.stop, query.stop)
            # can't do iteration here so recurse instead
            return (
                [project(overlap, mapping)]
                + find_ranges(r1, mappings)
                + find_ranges(r2, mappings)
            )
        elif query.start in mapping.src:
            overlap = range(query.start, mapping.src.stop)
            remainder = range(mapping.src.stop, query.stop)
        elif query.stop in mapping.src:
            overlap = range(mapping.src.start, query.stop)
            remainder = range(query.start, mapping.src.start)
        else:
            # print("nothing found")
            overlap = range(0, 0)
            remainder = query

        if len(overlap) > 0:
            ranges.append(project(overlap, mapping))
        query = remainder

    # final remainder, just maps 1:1
    if len(query) > 0:
        ranges.append(query)

    if len(ranges) == 0:
        raise RuntimeError("this is impossible")
    return ranges


def solve(lines: list[str]) -> int:
    initial_seeds = parse_seeds(lines[0])
    mappings = parse_mappings(lines[2:])

    src_type = "seed"
    src_ranges = initial_seeds
    while src_type != "location":
        dst_type, maps = mappings[src_type]
        dst_ranges = []
        for src_range in src_ranges:
            dst_ranges += find_ranges(src_range, maps)
        src_type = dst_type
        src_ranges = dst_ranges

    return min([r.start for r in src_ranges])


def main():
    assert solve(SAMPLE_INPUT.splitlines()) == 46

    with open("data/day05", encoding="utf-8") as f:
        data = f.read().splitlines()
    s = solve(data)
    print(s)
    assert s == 15880236


if __name__ == "__main__":
    main()
