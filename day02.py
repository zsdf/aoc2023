import re

SAMPLE_INPUT = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def parse_line(line: str) -> dict[str, int]:
    """
    get the maximum seen number of each color from each line
    """
    cubes = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for count, color in re.findall(r"(\d+) (red|blue|green)", line):
        if int(count) > cubes[color]:
            cubes[color] = int(count)
    return cubes


def solve1(lines: list[str]) -> int:
    # only 12 red cubes, 13 green cubes, and 14 blue cubes?
    total = 0

    for game_id, line in enumerate(lines):
        count = parse_line(line)
        if count["red"] <= 12 and count["green"] <= 13 and count["blue"] <= 14:
            total += game_id + 1
    return total


def solve2(lines: list[str]) -> int:
    # fewest number of cubes to make the game possible, per game
    total = 0
    for line in lines:
        count = parse_line(line)
        power = 1
        for val in count.values():
            power *= val
        total += power
    return total


def main():
    if parse_line(
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
    ) != {"red": 20, "blue": 6, "green": 13}:
        assert False

    with open("data/day02", encoding="utf-8") as f:
        data = f.read().splitlines()

    assert solve1(SAMPLE_INPUT.splitlines()) == 8
    s1 = solve1(data)
    print(s1)
    assert s1 == 2810

    assert solve2(SAMPLE_INPUT.splitlines()) == 2286
    s2 = solve2(data)
    print(s2)
    assert s2 == 69110


if __name__ == "__main__":
    main()
