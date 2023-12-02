import io
import re

sample_input = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def parse_line(line):
    """
    get the maximum seen number of each color from each line
    """
    max = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for count, color in re.findall(r"(\d+) (red|blue|green)", line):
        if int(count) > max[color]:
            max[color] = int(count)
    return max


def solve1(f):
    # only 12 red cubes, 13 green cubes, and 14 blue cubes?
    sum = 0
    id = 0
    for line in f:
        id += 1
        count = parse_line(line)
        if count["red"] <= 12 and count["green"] <= 13 and count["blue"] <= 14:
            sum += id
    return sum


def solve2(f):
    # fewest number of cubes to make the game possible, per game
    sum = 0
    for line in (s.rstrip("\n") for s in f):
        count = parse_line(line)
        power = 1
        for val in count.values():
            power *= val
        sum += power
    return sum


def main():
    if parse_line(
        "Game 3: 8 green, 6 blue, 20 red; " "5 blue, 4 red, 13 green; 5 green, 1 red"
    ) != {"red": 20, "blue": 6, "green": 13}:
        assert False

    print(solve1(io.StringIO(sample_input)))
    with open("data/day02") as f:
        s1 = solve1(f)
        print(s1)
        assert s1 == 2810
    with open("data/day02") as f:
        s2 = solve2(f)
        print(s2)
        assert s2 == 69110


if __name__ == "__main__":
    main()
