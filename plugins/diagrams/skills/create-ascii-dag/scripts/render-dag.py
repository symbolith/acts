#!/usr/bin/env python3
import re
import sys
from dataclasses import dataclass
from itertools import permutations
from math import inf
from pathlib import Path
from statistics import mean

ENACTABLE_TYPES = ("20260608023505", "20260923150308")
PLACE_TYPE = "20260608023514"
SKIPPED = {"node_modules", "target"}
WIDTH = 98
SHAPES = ["ud", "lr", "dr", "dl", "ur", "ul", "udr", "udl", "dlr", "ulr", "udlr"]
GLYPHS = dict(zip(SHAPES, "│─┌┐└┘├┤┬┴┼"))
SIGN = {"map": "+", "collect": "-"}
FILL = "━"
GAP = 3
SPACING = 6
START = "<!-- render-dag -->"
END = "<!-- render-dag-end -->"


@dataclass(frozen=True)
class Arc:
    place: str
    star: bool


@dataclass(frozen=True)
class Act:
    name: str
    inputs: tuple
    outputs: tuple
    follows: tuple = ()


def arcs(text):
    items = [item.strip() for item in text.split(",") if item.strip() and not item.strip().startswith("@")]
    return tuple(Arc(item.lstrip("*").strip(), item.startswith("*")) for item in items)


def predecessors_of(text):
    return tuple(item.strip()[1:].strip() for item in text.split(",") if item.strip().startswith("@"))


def parse_spec(text):
    lines = [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    matches = [(line, re.fullmatch(r"\s*([^:]+):(.*)->(.*)", line)) for line in lines]
    failed = [line for line, match in matches if not match]
    if failed:
        sys.exit(f"render-dag: cannot parse {failed[0]!r}")
    return [Act(match[1].strip(), arcs(match[2]), arcs(match[3]), predecessors_of(match[2])) for _, match in matches]


def frontmatter(path):
    match = re.match(r"---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    fields, key = {}, None
    for line in match[1].splitlines() if match else []:
        item, pair = re.match(r"\s+- (.*)", line), re.match(r"(\w+):\s*(.*)", line)
        if item and key:
            fields[key].append(item[1].strip('"'))
        elif pair:
            key = pair[1]
            fields[key] = [pair[2].strip('"')] if pair[2] else []
    return fields


def targets(values):
    return [match[1] for value in values for match in re.finditer(r"([^\s\[\]()/|]+)\.md", value)]


def workspace(path):
    return next((folder for folder in path.resolve().parents if (folder / ".obsidian").is_dir()), path.resolve().parent)


def parse_factor(path):
    root = workspace(path)
    files = (note for note in root.rglob("*.md") if not any(part.startswith(".") or part in SKIPPED for part in note.relative_to(root).parts))
    notes = {note.stem: frontmatter(note) for note in files}
    factor = path.stem
    refers = lambda note, key, identifier: identifier in targets(notes[note].get(key, []))
    alias = lambda note: (notes[note].get("aliases") or [note])[0]
    name = lambda place: alias(place).removeprefix(alias(factor) + ": ")
    parts = [
        note
        for note in notes
        if refers(note, "isPartOf", factor) or refers(note, "dcIsPartOf", factor) or refers(factor, "hasPart", note)
    ]
    acts = sorted((note for note in parts if any(refers(note, "type", kind) for kind in ENACTABLE_TYPES)), key=alias)
    places = sorted((note for note in parts if refers(note, "type", PLACE_TYPE)), key=alias)
    side = lambda act, plain, star, inverse: tuple(
        Arc(name(place), refers(act, star, place))
        for place in places
        if any(refers(act, key, place) for key in (*plain, star)) or any(refers(place, key, act) for key in inverse)
    )
    identifiers = {f"act:{alias(act)}": act for act in acts} | {f"place:{name(place)}": place for place in places}
    return [
        Act(
            alias(act),
            side(act, ("hasInputPlace", "hasInput"), "hasInputCollectPlace", ("isInputPlaceOf", "isInputOf")),
            side(act, ("hasOutputPlace", "hasOutput"), "hasOutputMapPlace", ("isOutputPlaceOf", "isOutputOf")),
            tuple(alias(earlier) for earlier in acts if refers(act, "follows", earlier) or refers(earlier, "precedes", act)),
        )
        for act in acts
    ], identifiers


def order(acts):
    producers = {arc.place: {act.name for act in acts if arc in act.outputs} for act in acts for arc in act.outputs}
    ordered, remaining = [], list(acts)
    while remaining:
        done = {act.name for act in ordered}
        ready = [
            act
            for act in remaining
            if all(producers.get(arc.place, set()) <= done for arc in act.inputs) and set(act.follows) <= done
        ]
        if not ready:
            sys.exit("render-dag: cycle among " + ", ".join(act.name for act in remaining))
        previous = {arc.place for arc in ordered[-1].outputs} if ordered else set()
        chosen = max(ready, key=lambda act: sum(arc.place in previous for arc in act.inputs))
        ordered.append(chosen)
        remaining.remove(chosen)
    return ordered


def check_depths(acts):
    place_depth = {}
    for act in acts:
        collected = [arc.place for arc in act.inputs if arc.star and place_depth.get(arc.place, 0) == 0]
        if collected:
            sys.exit(f"render-dag: {act.name} collects {collected[0]}, which no map produced")
        depth = max((place_depth.get(arc.place, 0) - arc.star for arc in act.inputs), default=0)
        for arc in act.outputs:
            new = depth + arc.star
            if place_depth.setdefault(arc.place, new) != new:
                sys.exit(f"render-dag: {arc.place} has map depth {place_depth[arc.place]} and {new}")


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str


def graph(acts):
    labels, edges = {}, []
    for act in acts:
        for arc in act.inputs:
            labels.setdefault(f"place:{arc.place}", f"({arc.place})")
            edges.append(Edge(f"place:{arc.place}", f"act:{act.name}", "collect" if arc.star else "seq"))
        labels[f"act:{act.name}"] = f"[{act.name}]"
        for arc in act.outputs:
            labels.setdefault(f"place:{arc.place}", f"({arc.place})")
            edges.append(Edge(f"act:{act.name}", f"place:{arc.place}", "map" if arc.star else "seq"))
    produced = {act.name: {arc.place for arc in act.outputs} for act in acts}
    edges += [
        Edge(f"act:{earlier}", f"act:{act.name}", "order")
        for act in acts
        for earlier in act.follows
        if not produced.get(earlier, set()) & {arc.place for arc in act.inputs}
    ]
    return labels, edges


def layering(labels, edges):
    predecessors = {node: [edge.source for edge in edges if edge.target == node] for node in labels}
    level = {}

    act = lambda node: node.startswith("act:")
    step = lambda earlier, later: 2 if act(earlier) == act(later) else 1

    def depth(node):
        if node not in level:
            level[node] = max((depth(other) + step(other, node) for other in predecessors[node]), default=int(act(node)))
        return level[node]

    for node in labels:
        depth(node)
    return level


@dataclass(frozen=True)
class Segment:
    source: str
    target: str
    kind: str
    net: str


def origin(net):
    return net[len("link:"):].split("#")[0] if net.startswith("link:") else net


def letters(number, alphabet):
    return letters(number // 26 - 1, alphabet) + alphabet[number % 26] if number >= 26 else alphabet[number]


def identify(rows, width, fill):
    acts = [node for row in rows for node in row if node.startswith("act:")]
    places = [node for row in rows for node in row if node.startswith("place:")]
    bar = lambda name, node: name + fill * (width[node] - len(name)) if fill == "┃" else name.center(width[node], fill)
    identifiers = {node: bar(letters(index, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"), node) for index, node in enumerate(acts)}
    identifiers |= {node: "(" + letters(index, "abcdefghijklmnopqrstuvwxyz").center(max(width[node] - 2, 1)) + ")" for index, node in enumerate(places)}
    links = [node for row in rows for node in row if node.startswith("link:")]
    identifiers |= {node: "{" + identifiers[origin(node)].strip(fill + "()").strip() + "}" for node in links}
    return identifiers


def stack(bent, order):
    ends, track = [], {}
    span = lambda bar: (min(bar[1], *(column for column, _ in bar[2])), max(bar[1], *(column for column, _ in bar[2])))
    for bar in order:
        low, high = span(bar)
        free = next((slot for slot, end in enumerate(ends) if not any(low - 1 <= used <= high + 1 for used in end)), len(ends))
        ends[free:free + 1] = [(ends[free] if free < len(ends) else set()) | set(range(low, high + 1))]
        track[bar] = free
    return track, len(ends)


def tangles(bars, track):
    bottom = 10 ** 6
    verticals = []
    for bar in bars:
        net, anchor, members = bar
        row = track.get(bar)
        verticals += [(net, anchor, -1, bottom)] if row is None else [(net, anchor, -1, row)] + [(net, column, row, bottom) for column, _ in members]
    count = 0
    for bar, row in track.items():
        low, high = min(bar[1], *(column for column, _ in bar[2])), max(bar[1], *(column for column, _ in bar[2]))
        count += sum(1 for net, column, top, end in verticals if net != bar[0] and low <= column <= high and top <= row <= end)
    return count


def route(rows, segments, stem, port):
    plans = []
    for row in rows[:-1]:
        bars = []
        for node in row:
            members = tuple((port[segment], segment) for segment in segments if segment.source == node)
            if members:
                bars.append((members[0][1].net, stem[node], members))
        bent = [bar for bar in bars if any(column != bar[1] for column, _ in bar[2])]
        orders = permutations(bent) if len(bent) <= 7 else [sorted(bent, key=lambda bar: bar[1])]
        track, count = min(
            (stack(bent, order) for order in orders),
            key=lambda result: (tangles(bars, result[0]), result[1]),
            default=({}, 0),
        )
        plans.append((bars, track, count))
    return plans


def kind_of(edges):
    kinds = {edge.kind for edge in edges}
    return kinds.pop() if len(kinds) == 1 else "seq"


def glyph(nets):
    directions = next(iter(nets.values()))
    if len(nets) > 1:
        crossing = next((found for found in nets.values() if "u" in found or "d" in found), directions)
        directions = {key: value for key, value in crossing.items() if key in "ud"} or crossing
    shape = "".join(key for key in "udlr" if key in directions)
    shape = {"u": "ud", "d": "ud", "l": "lr", "r": "lr"}.get(shape, shape)
    if shape in ("ud", "lr") and set(directions.values()) == {"order"}:
        return "┆" if shape == "ud" else "┄"
    return GLYPHS[shape]


def draw(rows, nodes, identifiers, left, stem, plans, sideways):
    cells, marks, line, first = {}, {}, 0, {}

    def link(first, second, kind, net):
        forward, backward = ("d", "u") if first[1] == second[1] else ("r", "l")
        cells.setdefault(first, {}).setdefault(net, {})[forward] = kind
        cells.setdefault(second, {}).setdefault(net, {})[backward] = kind

    def vertical(column, top, bottom, kind, net):
        for number in range(top, bottom):
            link((number, column), (number + 1, column), kind, net)

    def horizontal(number, start, stop, kind, net):
        for column in range(start, stop):
            link((number, column), (number, column + 1), kind, net)

    for index, row in enumerate(rows):
        thin = [node for node in row if sideways and node.startswith(("place:", "link:"))]
        bottom = line + max((len(identifiers[node]) for node in thin), default=1) - 1
        for node in row:
            if nodes[node] is not None:
                first[node] = (left[node] if sideways else line, stem[node] if sideways else left[node])
            if node in thin:
                marks.update(((line + offset, stem[node]), char) for offset, char in enumerate(identifiers[node]))
            elif nodes[node] is not None:
                marks.update(((line, left[node] + offset), char) for offset, char in enumerate(identifiers[node]))
                vertical(stem[node], line, bottom, "seq", node)
        if index == len(rows) - 1:
            break
        bars, track, count = plans[index]
        signed = any(segment.kind in SIGN and nodes[segment.target] is not None for bar in bars for _, segment in bar[2])
        lead = 1 if sideways or count else 0
        head = bottom + lead + count + 1 + signed + 1
        for bar in bars:
            net, anchor, members = bar
            bar_line = line
            if bar in track:
                bar_line = bottom + 1 + lead + track[bar]
                for column, segment in sorted(members, key=lambda member: member[1].kind == "seq"):
                    horizontal(bar_line, min(anchor, column), max(anchor, column), segment.kind, net)
                vertical(anchor, line, bar_line, kind_of([segment for _, segment in members]), net)
            for column, segment in members:
                if nodes[segment.target] is None:
                    vertical(column, bar_line, head + 1, segment.kind, net)
                    continue
                vertical(column, bar_line, head, segment.kind, net)
                marks[(head, column)] = "▼"
                if segment.kind in SIGN:
                    marks[(head - 1, column) if bar_line < head - 1 else (bar_line, (anchor + column) // 2)] = SIGN[segment.kind]
        line = head + 1
    return cells, marks, first


def spread(row, desired, width):
    left, cursor = [], -inf
    for node, want in zip(row, desired):
        left.append(max(round(want), cursor))
        cursor = left[-1] + width[node] + GAP
    right, limit = [], inf
    for node, want in zip(reversed(row), reversed(desired)):
        right.append(min(round(want), limit - width[node]))
        limit = right[-1] - GAP
    placed, cursor = [], -inf
    for node, low, high in zip(row, left, reversed(right)):
        placed.append(max((low + high) // 2, cursor))
        cursor = placed[-1] + width[node] + GAP
    return placed


def deterministic(labels, edges, level):
    nodes, segments, rows, left, width, stem = dict(labels), [], [], {}, {}, {}
    sequence = list(labels)
    producer = {}
    for edge in edges:
        if edge.source.startswith("act:") and edge.target.startswith("place:"):
            producer.setdefault(edge.target, edge.source)
    above, margin, lines, slot = [], [], {}, {}
    first_readers = {edge.source: min(level[other.target] for other in edges if other.source == edge.source) for edge in edges}
    for row in range(0, max(level.values()) + 1, 2):
        made = lambda edge: edge.source in producer and level[edge.source] == row and producer[edge.source] in stem
        acts = sorted(
            (node for node in sequence if level[node] == row + 1),
            key=lambda act: (mean([stem[producer[edge.source]] for edge in edges if edge.target == act and made(edge)] or [inf]), sequence.index(act)),
        )
        chronology = {
            act: [edge.source for edge in sorted(
                (edge for edge in edges if edge.target == act),
                key=lambda edge: (level[edge.source], stem.get(producer.get(edge.source), 0), sequence.index(edge.source)),
            )]
            for act in acts
        }
        anchor, followers = {}, {}
        for place in {place for act in acts for place in chronology[act] if level[place] == row}:
            readers = [act for act in acts if place in chronology[act]]
            if len(readers) < 2:
                continue
            options = [
                (reader, [other for other in readers if other != reader and chronology[other][0] == place])
                for reader in readers
                if chronology[reader][-1] == place
            ]
            if options:
                anchor[place], followers[place] = max(options, key=lambda option: len(option[1]))
        arranged, waiting = [], {other: place for place, others in followers.items() for other in others}
        for act in acts:
            if act in arranged or act in waiting:
                continue
            arranged.append(act)
            for place in chronology[act]:
                if anchor.get(place) == act:
                    arranged += [other for other in followers[place] if other not in arranged]
        acts = arranged + [act for act in acts if act not in arranged]
        used, blocks, maker = set(), [], {}
        for edge in edges:
            if edge.source in above and edge.target.startswith("place:"):
                if level[edge.target] == row:
                    maker[edge.target] = edge.source
                    segments.append(Segment(edge.source, edge.target, edge.kind, edge.source))
                else:
                    link = f"link:{edge.target}#{len(nodes)}"
                    nodes[link], maker[link] = labels[edge.target], edge.source
                    segments.append(Segment(edge.source, link, edge.kind, edge.source))
        for act in acts:
            block = []
            inputs = sorted(
                (edge for edge in edges if edge.target == act),
                key=lambda edge: (level[edge.source], stem.get(producer.get(edge.source), 0), sequence.index(edge.source)),
            )
            for edge in inputs:
                node = edge.source
                if act in followers.get(node, []):
                    block.append(("slot", node, edge.kind))
                    continue
                if level[node] != row or node in used or anchor.get(node, act) != act:
                    node = f"link:{edge.source}#{len(nodes)}"
                    nodes[node] = labels[edge.source]
                used.add(node)
                block.append(node)
                segments.append(Segment(node, act, edge.kind, node))
            blocks.append((act, block))
        spare = [node for node in maker if node not in used] + [node for node in sequence if level[node] == row and node not in used and node not in maker and node.startswith("place:")]
        if row == 0:
            margin = sorted(spare, key=lambda node: (first_readers.get(node, inf), sequence.index(node)))
            spare = []
        blocks += [(None, [node]) for node in spare]
        rank, keyed, previous = {}, [], -inf
        for number, (act, block) in enumerate(blocks):
            want = None
            for index, node in enumerate(block):
                if not isinstance(node, tuple) and node in maker:
                    want = stem[maker[node]] + SPACING * rank.get(maker[node], 0) - SPACING * index
                    break
            for node in block:
                if not isinstance(node, tuple) and node in maker:
                    rank[maker[node]] = rank.get(maker[node], 0) + 1
            previous = want if want is not None else previous
            keyed.append((previous, number, act, block, want))
        keyed.sort(key=lambda item: (item[0], item[1]))
        size = {number: SPACING * (len(block) - 1) + 3 if block else 3 for _, number, _, block, _ in keyed}
        wanted = []
        for position, (_, number, _, _, want) in enumerate(keyed):
            if want is not None:
                wanted.append(want - 1)
            else:
                wanted.append(wanted[-1] + size[keyed[position - 1][1]] + GAP if position else 0)
        starts = spread([item[1] for item in keyed], wanted, size)
        places, ordered = [], []
        for start, (_, _, act, block, _) in zip(starts, keyed):
            centers = [start + 1 + SPACING * index for index in range(len(block))]
            for node, center in zip(block, centers):
                if isinstance(node, tuple):
                    segments.append(Segment(node[1], act, node[2], node[1]))
                    slot[segments[-1]] = center
                    continue
                left[node], width[node], stem[node] = center - 1, 3, center
                places.append(node)
            if act is not None:
                left[act] = start
                width[act] = centers[-1] - centers[0] + 3 if block else 3
                stem[act] = centers[-1] if block else start + 1
                ordered.append(act)
        for act in above:
            within = [stem[node] for node in maker if maker[node] == act and left[act] <= stem[node] < left[act] + width[act]]
            stem[act] = min(within, key=lambda column: abs(column - stem[act]), default=stem[act])
        leftmost = min(keyed, key=lambda item: starts[keyed.index(item)]) if keyed else None
        if leftmost and leftmost[2] is not None and leftmost[3]:
            candidate, reader = leftmost[3][0], leftmost[2]
            origin_place = origin(candidate) if isinstance(candidate, str) and candidate.startswith("link:") else None
            if origin_place in margin and origin_place not in lines:
                rails = [f"rail:{origin_place}#{number}" for number in range(1, row + 1)]
                for number, rail in enumerate(rails, start=1):
                    nodes[rail], width[rail] = None, 1
                    (places if number == row else rows[number]).insert(0, rail)
                kind = next(segment.kind for segment in segments if segment.source == candidate)
                segments[:] = [segment for segment in segments if segment.source != candidate]
                chain = [origin_place, *rails]
                segments += [Segment(upper, lower, kind, origin_place) for upper, lower in zip(chain, chain[1:])]
                segments.append(Segment(rails[-1], reader, kind, origin_place))
                slot[segments[-1]] = stem[candidate]
                places.remove(candidate)
                del nodes[candidate]
                lines[origin_place] = rails
        rows.append(places)
        if ordered:
            rows.append(ordered)
        above = ordered
    edge_left = min(value for node, value in left.items() if nodes.get(node) is not None)
    for number, place in enumerate(margin):
        column = edge_left - 4 - SPACING * (len(margin) - 1 - number)
        left[place], width[place], stem[place] = column - 1, 3, column
        left |= {rail: column for rail in lines.get(place, [])}
        stem |= {rail: column for rail in lines.get(place, [])}
    rows[0][:0] = margin
    base = min(left.values())
    left = {node: value - base for node, value in left.items()}
    stem = {node: value - base for node, value in stem.items()}
    port = {segment: stem[segment.source] if segment.target.startswith("act:") else stem[segment.target] for segment in segments}
    port |= {segment: column - base for segment, column in slot.items()}
    return nodes, segments, rows, left, {node: left[node] + width[node] - 1 for node in left}, stem, port


def legend(identifiers, labels):
    short_form = lambda node: identifiers[node].strip(FILL).join(FILL * 2) if node.startswith("act:") else identifiers[node].replace(" ", "")
    return {node: (short_form(node), labels[node][1:-1]) for node in labels if node in identifiers}


def render(acts, notes=None):
    acts = order(acts)
    check_depths(acts)
    labels, edges = graph(acts)
    nodes, segments, rows, left, right, stem, port = deterministic(labels, edges, layering(labels, edges))
    identifiers = identify(rows, {node: right[node] - left[node] + 1 for node in labels}, FILL)
    cells, marks, first = draw(rows, nodes, identifiers, left, stem, route(rows, segments, stem, port), False)
    canvas = {cell: glyph(nets) for cell, nets in cells.items()} | marks
    breadth = max(column for _, column in canvas) + 1
    height = max(row for row, _ in canvas) + 1
    lines = ["".join(canvas.get((number, column), " ") for column in range(breadth)).rstrip() for number in range(height)]
    top = next(number for number, line in enumerate(lines) if line)
    lines = lines[top:]
    entries = legend(identifiers, labels)
    beside, cursor = {}, -1
    for node in sorted(entries, key=first.get):
        cursor = max(first[node][0] - top, cursor + 1)
        beside[cursor] = " ".join(entries[node])
    if any(node.startswith("link:") for node in nodes):
        beside[cursor + 1] = "{x} link to (x)"
    lines += [""] * (max(beside, default=0) + 1 - len(lines))
    lines = [f"{drawing:<{breadth + 3}}{beside.get(number, '')}".rstrip() for number, drawing in enumerate(lines)]
    widest = max(map(len, lines))
    if widest > WIDTH:
        print(f"render-dag: {widest} columns, more than {WIDTH}", file=sys.stderr)
    if notes is None:
        return "\n".join(lines)
    listing = [f"- `{entries[node][0]}` [{entries[node][1]}]({notes[node]}.md)" for node in sorted(entries, key=first.get) if node in notes]
    return "\n".join([START, "", "```text", *lines, "```", "", *listing, "", END])


def main():
    flags = [argument for argument in sys.argv[1:] if argument.startswith("--")]
    arguments = [argument for argument in sys.argv[1:] if not argument.startswith("--")]
    if len(arguments) != 1 or set(flags) - {"--block"}:
        sys.exit("usage: render-dag.py [--block] <factor-note.md | spec-file | ->")
    source = arguments[0]
    if source.endswith(".md"):
        acts, notes = parse_factor(Path(source))
    else:
        acts, notes = parse_spec(sys.stdin.read() if source == "-" else Path(source).read_text(encoding="utf-8")), {}
    if not acts:
        sys.exit(f"render-dag: {source} has no acts")
    print(render(acts, notes if "--block" in flags else None))


if __name__ == "__main__":
    main()
