import re

# winning | have
SAMPLE_INPUT = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def score_cards(data: list[str]) -> list[int]:
    cards = []
    for line in data:
        [_, winning_input, ticket_input] = re.split(r"[:|]", line)
        winners = set(int(n) for n in re.findall(r"\d+", winning_input))
        ticket = set(int(n) for n in re.findall(r"\d+", ticket_input))

        score = 0
        for n in ticket:
            if n in winners:
                score += 1
        cards.append(score)

    return cards


def solve1(data: list[str]) -> int:
    total = 0
    for score in score_cards(data):
        if score > 0:
            total += int(2 ** (score - 1))
    return total


def solve2(data: list[str]) -> int:
    max_cards = len(data)
    scored_cards = score_cards(data)
    cards = [1 for n in range(0, len(data))]

    for i, points in enumerate(scored_cards):
        for j in range(1, points + 1):
            if i + j < max_cards:
                cards[i + j] += cards[i]

    return sum(cards)


def main():
    with open("data/day04", encoding="utf-8") as f:
        data = f.read().splitlines()

    assert solve1(SAMPLE_INPUT.splitlines()) == 13
    s1 = solve1(data)
    print(s1)
    assert s1 == 18619

    assert solve2(SAMPLE_INPUT.splitlines()) == 30
    s2 = solve2(data)
    print(s2)
    assert s2 == 8063216


if __name__ == "__main__":
    main()
