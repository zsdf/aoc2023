import re

SAMPLE_INPUT = """\
Time:      7  15   30
Distance:  9  40  200
"""


def line_numbers(line: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", line)]


# hold down button
# boat speed = 0mm/ms
# each ms you hold down the button, the speed increases by 1mm/ms
def solve1(lines: list[str]) -> int:
    """Return the sum of the number of ways to beat each race"""
    races = list(zip(line_numbers(lines[0]), line_numbers(lines[1])))
    # print(races)
    product = 1
    for time, dist in races:
        winners = []
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

    total = 0
    for t in range(0, time):
        d = t * (time - t)
        if d > dist:
            total += 1
    return total


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
