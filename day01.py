import re

sample = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""


def solve1(f):
    sum = 0
    for line in f:
        digits = [c for c in list(line) if c.isdecimal()]
        val = digits[0] + digits[-1]
        sum += int(val)
    return sum


# no zero ?
# pattern = r"[0-9]|one|two|three|four|five|six|seven|eight|nine"
digit_words = "one two three four five six seven eight nine".split(" ")
pattern = re.compile("([0-9]|" + "|".join(digit_words) + ")")
value = {}

for i in range(0, 10):
    value[str(i)] = str(i)

for i, word in enumerate(digit_words):
    value[word] = str(i + 1)


def line_digits(line):
    # matches = pattern.findall(line)
    matches = []
    for i in range(0, len(line)):
        if match := pattern.match(line[i:]):
            matches.append(match.group(0))

    return [value[d] for d in matches]


def solve2(f):
    sum = 0
    for line in f:
        digits = line_digits(line)
        val = digits[0] + digits[-1]
        sum += int(val)

    return sum


def main():
    if line_digits("fiveight") != ["5", "8"]:
        print(line_digits("fiveight"))
        assert False

    with open("data/day01") as f:
        s1 = solve1(f)
        print(s1)
        assert s1 == 52974

    with open("data/day01") as f:
        s2 = solve2(f)
        print(s2)
        assert s2 == 53340


if __name__ == "__main__":
    main()
