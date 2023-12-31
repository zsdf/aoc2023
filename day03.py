import re
from typing import Tuple


def is_symbol(c: str) -> bool:
    return not (c.isdecimal() or c == ".")


def adjacencies(pos: Tuple[int, int]) -> list[Tuple[int, int]]:
    (x, y) = pos
    return [
        (x + 0, y - 1),
        (x + 1, y - 1),
        (x + 1, y + 0),
        (x + 1, y + 1),
        (x + 0, y + 1),
        (x - 1, y + 1),
        (x - 1, y + 0),
        (x - 1, y - 1),
    ]


def parse_input(data: list[str]):
    id_seq = 0
    numbers: dict[Tuple[int, int], Tuple[int, int]] = {}
    symbols: dict[Tuple[int, int], str] = {}

    for y, line in enumerate(data):
        # find all symbols on the line and record their positions
        for x, c in enumerate(line):
            if is_symbol(c):
                symbols[(x, y)] = c

        # find all the numbers on the line, same
        offset = 0
        while match := re.search(r"\d+", line[offset:]):
            id_seq += 1
            (start, end) = match.span()

            n = int(match.group(0))
            for x in range(start + offset, end + offset):
                # print(n, (x, y))
                numbers[(x, y)] = (id_seq, n)

            offset += end

    return numbers, symbols


def solve1(data: list[str]) -> int:
    numbers, symbols = parse_input(data)

    known_parts: set[int] = set()
    total = 0

    for number_pos, (key, val) in numbers.items():
        # if adjacent to a symbol...
        for pos in adjacencies(number_pos):
            if pos in symbols and key not in known_parts:
                total += val
                known_parts.add(key)
                # print("part:", id, val)

    return total


def solve2(data: list[str]) -> int:
    numbers, symbols = parse_input(data)

    total = 0
    for symbol_pos, symbol in symbols.items():
        if symbol != "*":
            continue
        adjacent_numbers: dict[int, int] = {}
        for pos in adjacencies(symbol_pos):
            if pos in numbers:
                (number_id, number_value) = numbers[pos]
                adjacent_numbers[number_id] = number_value
        if len(adjacent_numbers) == 2:
            values = list(adjacent_numbers.values())
            total += values[0] * values[1]
    return total


SAMPLE_INPUT = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def main():
    with open("data/day03", encoding="utf-8") as f:
        data = f.read().splitlines()

    assert solve1(SAMPLE_INPUT.splitlines()) == 4361
    s1 = solve1(data)
    print(s1)
    assert s1 == 525119

    assert solve2(SAMPLE_INPUT.splitlines()) == 467835
    s2 = solve2(data)
    print(s2)
    assert s2 == 76504829


if __name__ == "__main__":
    main()
