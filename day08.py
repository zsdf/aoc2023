import math
import re

SAMPLE_INPUT = [
    """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""",
    """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""",
    """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""",
]


def solve1(lines: list[str]) -> int:
    directions = lines[0]

    graph = parse_graph(lines[2:])

    steps = 0
    position = "AAA"
    while position != "ZZZ":
        branch = directions[steps % len(directions)]

        position = graph[position][branch]

        steps += 1
    return steps


def is_start_node(node: str) -> bool:
    return node.endswith("A")


def is_end_node(node: str) -> bool:
    return node.endswith("Z")


def parse_graph(lines: list[str]) -> dict[str, dict[str, str]]:
    """
    Returns a dictionary like
    {
        "AAA": { "L": "BBB", "R": "CCC" },
        "BBB": { "L": "CCC", "R": "DDD" },
        ...
    }
    """
    graph: dict[str, dict[str, str]] = {}
    for line in lines:
        if match := re.search(r"^(\w+) = \((\w+), (\w+)\)$", line):
            key, left, right = match.groups()
            graph[key] = {
                "L": left,
                "R": right,
            }
        else:
            raise RuntimeError("failed to parse line")
    return graph


def solve2_naive(lines: list[str]) -> int:
    directions = lines[0]
    graph = parse_graph(lines[2:])

    steps = 0
    positions = list(filter(is_start_node, graph.keys()))
    while not all(is_end_node(node) for node in positions):
        branch = directions[steps % len(directions)]

        for i, position in enumerate(positions):
            positions[i] = graph[position][branch]

        steps += 1
    return steps


def solve2(lines: list[str]) -> int:
    directions = lines[0]
    graph = parse_graph(lines[2:])

    start_nodes = list(filter(is_start_node, graph.keys()))

    cycle_times: list[int] = []
    for node in start_nodes:
        step = 0
        while not is_end_node(node):
            node = graph[node][directions[step % len(directions)]]
            step += 1
        cycle_times.append(step)

    return math.lcm(*cycle_times)


def main() -> None:
    with open("data/day08", encoding="utf-8") as f:
        data = f.read().splitlines()

    assert solve1(SAMPLE_INPUT[0].splitlines()) == 2
    assert solve1(SAMPLE_INPUT[1].splitlines()) == 6

    s1 = solve1(data)
    print(s1)
    assert s1 == 18827

    assert solve2_naive(SAMPLE_INPUT[2].splitlines()) == 6
    s2 = solve2(data)
    print(s2)
    assert s2 == 20220305520997


if __name__ == "__main__":
    main()
