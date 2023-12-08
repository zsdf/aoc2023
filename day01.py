import re

SAMPLE_INPUT_1 = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

SAMPLE_INPUT_2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


def solve1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        digits = [c for c in list(line) if c.isdecimal()]
        val = digits[0] + digits[-1]
        total += int(val)
    return total


# no zero ?
# pattern = r"[0-9]|one|two|three|four|five|six|seven|eight|nine"
digit_words = "one two three four five six seven eight nine".split(" ")
pattern = re.compile("([0-9]|" + "|".join(digit_words) + ")")
value = {}

for i in range(0, 10):
    value[str(i)] = str(i)

for i, word in enumerate(digit_words):
    value[word] = str(i + 1)


def line_digits(line: str) -> list[int]:
    # matches = pattern.findall(line)
    matches: list[str] = []
    for i in range(0, len(line)):
        if match := pattern.match(line[i:]):
            matches.append(match.group(0))

    return [value[d] for d in matches]


def solve2(lines: list[str]) -> int:
    total = 0
    for line in lines:
        digits = line_digits(line)
        val = digits[0] + digits[-1]
        total += int(val)

    return total


def main():
    if line_digits("fiveight") != ["5", "8"]:
        print(line_digits("fiveight"))
        assert False

    with open("data/day01", encoding="utf-8") as f:
        data = f.read().splitlines()

    assert solve1(SAMPLE_INPUT_1.splitlines()) == 142
    s1 = solve1(data)
    print(s1)
    assert s1 == 52974

    assert solve2(SAMPLE_INPUT_2.splitlines()) == 281
    s2 = solve2(data)
    print(s2)
    assert s2 == 53340


if __name__ == "__main__":
    main()
