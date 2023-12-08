import math
import re
from typing import Tuple

SAMPLE_INPUT = """\
Time:      7  15   30
Distance:  9  40  200
"""


def line_numbers(line: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", line)]


def find_min_max_naive(time: int, dist: int) -> Tuple[int, int]:
    winners: list[int] = []
    for r in range(0, time):
        d = r * (time - r)
        if d >= dist:
            winners.append(r)
    return (winners[0], winners[-1])


def find_min_max_only(time: int, dist: int) -> Tuple[int, int]:
    winners: list[int] = []
    for r in range(0, time):
        d = r * (time - r)
        if d >= dist:
            winners.append(r)
            break
    for r in range(time, 0, -1):
        d = r * (time - r)
        if d >= dist:
            winners.append(r)
            break
    return winners[0], winners[1]


def roots(a: int, b: int, c: int) -> list[float]:
    """Roots of ax^2 + bx + c = 0"""
    x1 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    x2 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
    return [x1, x2]


def find_min_max_calc(time: int, dist: int) -> Tuple[int, int]:
    """
    The distance traveled is described by `dist = (time - x) * x`, which is
    a quadtratic equation, so we can just calculate the roots to solve it.
    """
    winners = roots(-1, time, -dist)
    return math.ceil(winners[0]), math.floor(winners[1])


# hold down button
# boat speed = 0mm/ms
# each ms you hold down the button, the speed increases by 1mm/ms
def solve1(lines: list[str]) -> int:
    """Return the sum of the number of ways to beat each race"""
    races = list(zip(line_numbers(lines[0]), line_numbers(lines[1])))
    # print(races)
    product = 1
    for time, dist in races:
        winners: list[Tuple[int, int]] = []
        # we don't have to iterate through every number
        # we could just find the min and max
        # or there is probably just a way to compute it
        for t in range(0, time):
            d = t * (time - t)
            if d > dist:
                winners.append((t, d))
        product *= len(winners)
    return product


def solve2(lines: list[str]) -> int:
    """Return the total ways to beat the input as just one race"""
    lines = [re.sub(r" ", "", line) for line in lines]
    time, dist = next(zip(line_numbers(lines[0]), line_numbers(lines[1])))

    x1, x2 = find_min_max_calc(time, dist)
    # if x2 == x2 then the answer is 1, not 0
    return x2 - x1 + 1


def main():
    with open("data/day06", encoding="utf-8") as f:
        data = f.read().splitlines()

    assert solve1(SAMPLE_INPUT.splitlines()) == 288
    s1 = solve1(data)
    print(s1)
    assert s1 == 800280

    assert solve2(SAMPLE_INPUT.splitlines()) == 71503
    s2 = solve2(data)
    print(s2)
    assert s2 == 45128024


if __name__ == "__main__":
    main()
