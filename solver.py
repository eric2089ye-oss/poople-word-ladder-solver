#!/usr/bin/env python3
"""Deterministic four-letter word-ladder solver.

Shortest paths are relative to the bundled dictionary, not an official game.
The dictionary is a versioned SCOWL-derived practice list; see data/.
"""
import argparse
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORDS_FILE = ROOT / "data" / "words.json"


def normalize_word(value):
    """Return a normalized four-letter ASCII word, or an empty string."""
    if not isinstance(value, str):
        return ""
    word = value.strip().lower()
    return word if re.fullmatch(r"[a-z]{4}", word) else ""


def load_words(path=WORDS_FILE):
    return {word for value in json.loads(Path(path).read_text())["words"]
            if (word := normalize_word(value))}


def build_adj(words):
    words = sorted({word for value in words if (word := normalize_word(value))})
    buckets = defaultdict(list)
    for w in words:
        for i in range(4):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)
    adj = {word: set() for word in words}
    for group in buckets.values():
        for a in group:
            adj[a].update(x for x in group if x != a)
    return {word: tuple(sorted(neighbors)) for word, neighbors in adj.items()}


def is_valid_step(start, end, words):
    start, end = normalize_word(start), normalize_word(end)
    return (bool(start and end) and start in words and end in words
            and sum(a != b for a, b in zip(start, end)) == 1)


def shortest_path(start, end="poop", adj=None, words=None):
    """Single BFS shortest path (list, inclusive). None if unreachable."""
    start, end = normalize_word(start), normalize_word(end)
    if not start or not end:
        return None
    if adj is None:
        adj = build_adj(load_words() if words is None else words)
    if start not in adj or end not in adj:
        return None
    prev = {start: None}
    q = deque([start])
    while q:
        n = q.popleft()
        if n == end:
            path = []
            while n is not None:
                path.append(n)
                n = prev[n]
            return path[::-1]
        for m in sorted(adj[n]):
            if m not in prev:
                prev[m] = n
                q.append(m)
    return None


def par(start, adj=None, words=None):
    p = shortest_path(start, adj=adj, words=words)
    return None if p is None else len(p) - 1


def all_shortest_paths(start, end="poop", adj=None, words=None, cap=6):
    """All shortest paths via multi-parent BFS (capped)."""
    start, end = normalize_word(start), normalize_word(end)
    if not start or not end or not isinstance(cap, int) or cap <= 0:
        return []
    if adj is None:
        adj = build_adj(load_words() if words is None else words)
    if start not in adj or end not in adj:
        return []
    dist = {start: 0}
    parents = defaultdict(list)
    q = deque([start])
    while q:
        n = q.popleft()
        if dist[n] >= dist.get(end, float("inf")):
            continue
        for m in sorted(adj[n]):
            if m not in dist:
                dist[m] = dist[n] + 1
                parents[m].append(n)
                q.append(m)
            elif dist[m] == dist[n] + 1:
                parents[m].append(n)
    if end not in dist:
        return []
    out = []

    def back(node, trail):
        if len(out) >= cap:
            return
        if node == start:
            out.append([start] + trail[::-1])
            return
        for parent in sorted(parents[node]):
            back(parent, trail + [node])

    back(end, [])
    return out[:cap]


def hints_for(start, path):
    """Progressive hints: par -> positional tip -> first bridge word."""
    if not path:
        return None
    if len(path) == 1:
        return {"par": 0, "position_hint": "You are already at the target.",
                "bridge_word": None}
    changes = [i for i in range(4) if path[0][i] != path[1][i]]
    first_pos = changes[0] if changes else 0
    return {
        "par": len(path) - 1,
        "position_hint": (f"One shortest route changes letter {first_pos + 1} "
                          f"(the {path[0][first_pos].upper()!r}) next."),
        "bridge_word": path[1],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Four-letter word-ladder solver (local dictionary).")
    parser.add_argument("start", help="four-letter starting word")
    parser.add_argument("--target", default="poop", help="four-letter target word (default: poop)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--alternatives", type=int, default=0,
                        help="include up to N alternative shortest paths")
    args = parser.parse_args(argv)
    words = load_words()
    adj = build_adj(words)
    start, target = normalize_word(args.start), normalize_word(args.target)
    if not start or not target:
        print("Both words must be four letters.", file=sys.stderr)
        return 2
    path = shortest_path(start, target, adj=adj)
    if not path:
        result = {"start": start, "target": target, "path": None, "par": None,
                  "reason": "no connection in this dictionary version"}
        print(json.dumps(result, indent=2) if args.json else
              f"{start.upper()}: no path to {target.upper()} in this dictionary")
        return 1
    hints = hints_for(start, path)
    result = {"start": start, "target": target, "path": path, "par": len(path) - 1,
              "hint": hints,
              "alternatives": all_shortest_paths(start, target, adj=adj, cap=args.alternatives)
              if args.alternatives else []}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{start.upper()}: par={len(path) - 1}")
        print("path=" + " -> ".join(word.upper() for word in path))
        print("hint=" + hints["position_hint"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
