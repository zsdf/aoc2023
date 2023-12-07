from collections import Counter
from typing import Tuple

cards = list("AKQJT98765432")

card_value: dict[str, int] = {}
for i, c in enumerate(reversed(cards)):
    card_value[c] = i

SAMPLE_INPUT = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

# - Five of a kind, where all five cards have the same label: AAAAA
# - Four of a kind, where four cards have the same label and one card has a different
#   label: AA8AA
# - Full house, where three cards have the same label, and the remaining two cards share
#   a different label: 23332
# - Three of a kind, where three cards have the same label, and the remaining two cards
#   are each different from any other card in the hand: TTT98
# - Two pair, where two cards share one label, two other cards share a second label, and
#   the remaining card has a third label: 23432
# - One pair, where two cards share one label, and the other three cards have a different
#   label from the pair and each other: A23A4
# - High card, where all cards' labels are distinct: 23456

SCORE_FIVE_KIND = 7
SCORE_FOUR_KIND = 6
SCORE_FULL_HOUSE = 5
SCORE_THREE_KIND = 4
SCORE_TWO_PAIR = 3
SCORE_ONE_PAIR = 2
SCORE_HIGH_CARD = 1


# 7 types of hands
def hand_score(hand: str) -> int:
    count = Counter(hand)
    counts = sorted(count.values(), reverse=True)

    if counts[0] == 5:
        return SCORE_FIVE_KIND
    elif counts[0] == 4:
        return SCORE_FOUR_KIND
    elif counts[0] == 3 and counts[1] == 2:
        return SCORE_FULL_HOUSE
    elif counts[0] == 3:
        return SCORE_THREE_KIND
    elif counts[0] == 2 and counts[1] == 2:
        return SCORE_TWO_PAIR
    elif counts[0] == 2:
        return SCORE_ONE_PAIR
    else:
        return SCORE_HIGH_CARD


def card_values(hand: str) -> list[int]:
    return [card_value[card] for card in hand]


def parse_line(line: str) -> Tuple[str, int]:
    [hand, bid] = line.split(" ")
    return hand, int(bid)


def solve1(lines: list[str]) -> int:
    total = 0
    hands: list[Tuple[int, list[int], str, int]] = []
    for line in lines:
        hand, bid = parse_line(line)
        hands.append((hand_score(hand), card_values(hand), hand, bid))

    # each hand wins amount of bid * rank,
    # where rank is the 1-indexed rank of the hands sorted by ascending... rank
    hands.sort()
    for rank, (_, _, _, bid) in enumerate(hands):
        total += bid * (rank + 1)
    return total


def main():
    with open("data/day07", encoding="utf-8") as f:
        data = f.read().splitlines()

    assert solve1(SAMPLE_INPUT.splitlines()) == 6440

    s1 = solve1(data)
    print(s1)
    assert s1 == 241344943


if __name__ == "__main__":
    main()
